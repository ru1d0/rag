<script setup>
import { ref } from 'vue'
import { onMounted } from 'vue'
import { marked } from 'marked'

const mensajes = ref([
  {
    role: 'assistant',
    content: 'Hola, soy Pabloxan 👋'
  }
])

marked.setOptions({
  breaks: true,
  gfm: true
})

const pregunta = ref('')
const loading = ref(false)
const pdfs = ref([])
const archive = ref(null)

function renderMarkdown(text) {
  return marked.parse(text)
}

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
      <input 
        id="input-pdf" 
        type="file" 
        accept="application/pdf" 
        @change="seleccionarArchivo" 
      />
      <label for="input-pdf" class="btn-anadir">
        <span>añadir archivo</span>
        <span class="plus-icon">+</span>
      </label>    
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
      <p v-if="mensaje.content" :class="mensaje.role + '-span'" v-html="renderMarkdown(mensaje.content)">
      </p>
      <div v-if="mensaje.role === 'assistant' && loading && index === mensajes.length - 1" class="typing-indicator">
        <span></span>
        <span></span>
        <span></span>
      </div>
      <img class="avatar-user" v-if="mensaje.role === 'user'" src="/assets/img/user.png" alt="Avatar" />
      </div>

    </div>

    <div class="input-area">
      <div class="input-box">
        <input
          v-model="pregunta"
          @keyup.enter="enviarMensaje"
          placeholder="Escribe tu pregunta..."
        />
        <button @click="enviarMensaje" class="btn-send">
          <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="22" y1="2" x2="11" y2="13"></line>
            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
          </svg>
        </button>
      </div>
    </div>
  </div>

</template>

<style>

.pdf-header h3 {
  font: Kokonor;
  font-weight: 400;
  font-style: regular;
  font-size: 24px;

}

body{
  margin:0;
  font-family:Arial, sans-serif;
  overflow-y: hidden;
  background-color: #141224;
}

#input-pdf {
  display: none;
}

.btn-anadir {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #1a2332;
  color: #a0aab8;           
  padding: 10px 20px;
  border-radius: 25px;      
  cursor: pointer;
  font-size: 16px;
  user-select: none;
  transition: background-color 0.2s ease;
  width: 100%;              
  box-sizing: border-box;
  margin: 54px 0px;
}

.btn-anadir:hover {
  background-color: #232e42;
  color: #ffffff;
}

.plus-icon {
  color: #ffffff;
  font-size: 22px;
  font-weight: bold;
  line-height: 1;
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
  filter: blur(120px);
  opacity: 0.6;
  z-index: -1;
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
  font-size: 16px;
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
  font-size: 16px;
  line-height: 19px;
}

.user {
  display: flex;
  justify-content: flex-end;
  text-align:right;
  margin: 10px 10px 20px 10px;
  align-items: center
}

.assistant {
  text-align:left;
  margin: 10px 10px 20px 10px;
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

.input-area {
  width: 100%;
}

/* La cápsula/píldora oscura contenedora */
.input-box {
  display: flex;
  align-items: center;
  width: 100%;
  background-color: #171725; /* Tono oscuro del diseño */
  border-radius: 50px;       /* Forma ovalada */
  padding: 6px 16px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

/* Quitar bordes y fondo al input nativo */
.input-box input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  color: #ffffff;
  font-size: 16px;
  padding: 10px;
}

.input-box input::placeholder {
  color: #6c727f;
}

/* Quitar bordes y fondo al botón para mostrar solo el icono */
.btn-send {
  background: transparent;
  border: none;
  color: #ffffff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 6px;
  transition: transform 0.2s ease, opacity 0.2s ease;
}

.btn-send:hover {
  opacity: 0.8;
  transform: scale(1.05);
}

button {
  padding:10px 20px;
}
/* Indicador de escritura (Typing Indicator) */
.typing-indicator {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 2px;
}

.typing-indicator span {
  width: 6px;
  height: 6px;
  background-color: #ffffff;
  border-radius: 50%;
  display: inline-block;
  opacity: 0.4;
  animation: typingBounce 1.4s infinite ease-in-out both;
}

/* Retrasos para generar el efecto en ola/cascada */
.typing-indicator span:nth-child(1) {
  animation-delay: 0s;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

/* Keyframes de la animación */
@keyframes typingBounce {
  0%, 80%, 100% {
    transform: scale(0.6);
    opacity: 0.4;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

</style>
