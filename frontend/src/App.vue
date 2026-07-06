<script setup>
import { ref } from 'vue'
import { onMounted } from 'vue'

const mensajes = ref([
  {
    role: 'assistant',
    content: 'Hola, soy Pabloxan 👋'
  }
])

const pregunta = ref('')
const loading = ref(false)
const pdfs = ref([])

async function enviarMensaje() {

  if (!pregunta.value.trim()) return

  const userMessage = pregunta.value

  // 1. Mostrar mensaje usuario
  mensajes.value.push({
    role: 'user',
    content: userMessage
  })

  pregunta.value = ''
  loading.value = true

  try {

    const res = await fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ 
              message: userMessage,
              history: mensajes.value
            })
    })

    const reader = res.body.getReader()
    const decoder = new TextDecoder()

    let texto = ""

    mensajes.value.push({
      role: 'assistant',
      content: ""
    })

    const index = mensajes.value.length - 1

    while (true) {
      const { value, done } = await reader.read()
      if (done) break

      texto += decoder.decode(value)

      mensajes.value[index].content = texto
    }

  } catch (error) {

    mensajes.value.push({
      role: 'assistant',
      content: 'Error conectando con el backend 😢'
    })

    console.error(error)

  } finally {
    loading.value = false
  }
}

function abrirPdf(pdf) {
  window.open(`http://localhost:8000/pdfs/${encodeURIComponent(pdf)}`, '_blank')
}

onMounted(async () => {
  const res = await fetch('http://localhost:8000/pdfs')
  pdfs.value = await res.json()
})

</script>

<template>
  <div>
    <aside>
      <h3>PDFs</h3>
      <div
        v-for="pdf in pdfs"
        :key="pdf"
        class="pdf-item"
        @click="abrirPdf(pdf)"
      >
        {{  pdf }}
      </div>
    </aside>
  </div>
  <div class="chat">

    <h1>Pabloxan</h1>

    <div class="mensajes">

      <div
        v-for="(mensaje,index) in mensajes"
        :key="index"
        :class="mensaje.role"
      >
        {{ mensaje.content }}
      </div>

    </div>

    <div class="input-area">

      <input
        v-model="pregunta"
        @keyup.enter="enviarMensaje"
        placeholder="Escribe tu pregunta..."
      />

      <button @click="enviarMensaje">
        Enviar
      </button>

    </div>

  </div>

</template>

<style>

body{
  margin:0;
  font-family:Arial, sans-serif;
}

aside {
  max-width: 300px;
}

#app {
    display: flex;
    padding-left: 44px;
    padding-right: 44px
}

.chat{
  max-width:900px;
  width: 100%;
  margin:auto;
  padding:20px;
}

.mensajes{
  height:70vh;
  overflow-y:auto;
  border:1px solid #ddd;
  padding:10px;
  margin-bottom:10px;
}

.user{
  text-align:right;
  margin:10px;
}

.assistant{
  text-align:left;
  margin:10px;
}

.input-area{
  display:flex;
  gap:10px;
}

input{
  flex:1;
  padding:10px;
}

button{
  padding:10px 20px;
}

</style>