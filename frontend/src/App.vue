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
const archive = ref(null)

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

    const res = await fetch('http://192.168.40.7:8000/chat', {
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
  window.open(`http://192.168.40.7:8000/pdfs/${encodeURIComponent(pdf)}`, '_blank')
}

function seleccionarArchivo(event) {
  archive.value = event.target.files[0]
}

onMounted(async () => {
  const res = await fetch('http://192.168.40.7:8000/pdfs')
  pdfs.value = await res.json()
})

async function subirPdf() {

  if (!archive.value) {
    alert('Por favor selecciona un archivo PDF primero.')
    return
  }
  console.log('Archivo seleccionado:', archive.value)
  const formData = new FormData()
  formData.append('pdf', archive.value)

  try {
    const res = await fetch('http://192.168.40.7:8000/upload', {
      method: 'POST',
      body: formData
    })

  } catch (error) {
      console.error('Error al subir el PDF:', error)
    }
}

</script>

<template>
  <div>
    <aside>
      <div class="pdf-header">
        <h3>FUENTES</h3>
        <input id="input-pdf" type="file" accept="application/pdf" @change="seleccionarArchivo"/>
        <button @click="subirPdf">Subir PDF</button>
      </div>
      <span
        v-for="pdf in pdfs"
        :key="pdf"
        class="pdf-item"
        @click="abrirPdf(pdf)"
      >
      <img src="/assets/img/pdf.png" class="pdf-icon"/>
        {{ pdf }}
      </span>
    </aside>
  </div>
  <div class="chat">

    <div class="mensajes">

      <div
        v-for="(mensaje,index) in mensajes"
        :key="index"
        :class="mensaje.role"
      >
      <img class="avatar-assistant" v-if="mensaje.role === 'assistant'" src="/assets/img/pablitoxat.png" alt="Avatar" />
      <p :class="mensaje.role + '-span'">
        {{ mensaje.content }}
      </p>
      <img class="avatar-user" v-if="mensaje.role === 'user'" src="/assets/img/user.png" alt="Avatar" />
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
  overflow-y: hidden;
  background-color: #141224;
}

.pdf-icon {
  width: 36px;
  height: 36px;
  margin-right: 8px;
}

aside {
  max-width: 319px;
  max-height: 100vh;
  overflow-y: auto;
  overflow-x: hidden;
  color: #FFFFFF;
}


#add-pdf {
  display: block;
  margin: auto;
}

#app {
    display: flex;
    padding-left: 44px;
    padding-right: 44px
}

.pdf-item {
  cursor: pointer;
  display: block;
  margin-bottom: 8px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.chat {
  max-width:900px;
  width: 100%;
  margin-left: auto;
  margin-right: auto;
  padding:20px;
}

.input-area::before {
  content: '';
  position: fixed;
  bottom: -100px;
  left: 50%;
  transform: translateX(-50%);
  width: 877px;
  height: 464px;
  background-color: #15688F;
  border-radius: 50%;
  filter: blur(120px); /* Desenfoque clave para el efecto glow */
  opacity: 0.6; /* Ajusta la intensidad de la luz si lo necesitas */
  z-index: -1; /* Para que quede detrás de todo el contenido */
  pointer-events: none;
}

.mensajes {
  height:80vh;
  overflow-y:auto;
  padding:10px;
  margin-bottom:10px;
  
}

.assistant-span {
  background-color:#3D395C;
  padding:12px;
  border-radius:8px;
  color: #FFFFFF;
  font: sans-serif;
  font-weight: 400px;
  font-size: 22px;
  line-height: 19px;
  width: fit-content;
}

.user-span {
  
  background-color:#6C6F8E;
  padding:12px;
  border-radius:8px;
  color: #FFFFFF;
  font: sans-serif;
  font-weight: 400px;
  font-size: 22px;
  line-height: 19px;
}

.user {
  display: flex;
  justify-content: flex-end;
  text-align:right;
  margin: 10px 10px 60px 10px;
  align-items: center
}

.assistant {
  text-align:left;
  margin: 10px 10px 60px 10px;
  display: flex;
  align-items: center;
}

.avatar-user {
  width: 60px;
  height: 56px;
  margin-left: 12px;
}

.avatar-assistant {
  width: 60px;
  height: 56px;
  margin-right: 12px;
}

.input-area {
  display:flex;
  gap:10px;
}

input {
  flex:1;
  padding:10px;
}

button {
  padding:10px 20px;
}

</style>
