<script setup>
import { ref } from 'vue'

const mensajes = ref([
  {
    role: 'assistant',
    content: 'Hola, soy Pabloxan 👋'
  }
])

const pregunta = ref('')

function enviarMensaje() {

  if (!pregunta.value.trim()) {
    return
  }

  mensajes.value.push({
    role: 'user',
    content: pregunta.value
  })

  mensajes.value.push({
    role: 'assistant',
    content: 'Respuesta de prueba'
  })

  pregunta.value = ''
}
</script>

<template>

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

.chat{
  max-width:900px;
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