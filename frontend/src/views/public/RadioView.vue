<script setup lang="ts">
import { useAudioPlayerStore } from '@/stores/audioPlayer'

const store = useAudioPlayerStore()

const togglePlay = () => {
  const audioEl = document.querySelector('audio')
  if (!audioEl) return
  
  if (store.isPlaying) {
    audioEl.pause()
    audioEl.src = ''
    audioEl.load()
    store.setPlaying(false)
  } else {
    store.setBuffering(true)
    audioEl.src = store.streamUrl
    audioEl.load()
    audioEl.play()
      .then(() => store.setPlaying(true))
      .catch(() => { store.hasError = true })
      .finally(() => store.setBuffering(false))
  }
}
</script>

<template>
  <div class="bg-gray-50 min-h-screen py-12">
    <div class="max-w-4xl mx-auto px-4">
      <div class="bg-white rounded-3xl shadow-xl overflow-hidden border border-gray-100">
        <!-- Visualizer Hero -->
        <div class="bg-upec-green-dark h-64 relative flex items-center justify-center overflow-hidden">
          <div class="absolute inset-0 bg-gradient-to-br from-upec-green to-upec-green-dark opacity-90"></div>
          
          <!-- Decorative Waveform -->
          <div class="absolute bottom-0 w-full flex items-end justify-center space-x-1 sm:space-x-2 px-4 h-32 opacity-30">
            <div v-for="i in 30" :key="i" 
                 class="w-2 sm:w-4 bg-upec-yellow rounded-t-sm" 
                 :class="{ 'animate-pulse': store.isPlaying }"
                 :style="{ height: store.isPlaying ? `${Math.random() * 80 + 20}%` : '10%' }">
            </div>
          </div>

          <div class="relative z-10 text-center">
            <h1 class="text-4xl md:text-5xl font-extrabold text-white mb-2 tracking-tight">Mindalae</h1>
            <p class="text-xl text-upec-yellow font-bold tracking-widest">102.3 FM</p>
          </div>
        </div>

        <div class="p-8 md:p-12 text-center">
          <div class="mb-8">
            <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-red-100 text-red-800 mb-4">
              <span class="w-2 h-2 rounded-full bg-red-600 mr-2" :class="{'animate-ping': store.isPlaying}"></span>
              Transmisión en Vivo
            </span>
            <h2 class="text-2xl font-bold text-gray-900 mb-2">{{ store.currentTrack }}</h2>
            <p class="text-gray-500">{{ store.stationName }}</p>
          </div>

          <button 
            @click="togglePlay"
            class="w-24 h-24 rounded-full bg-upec-green hover:bg-upec-green-dark shadow-lg shadow-upec-green/30 text-white flex items-center justify-center mx-auto transition-transform hover:scale-105 focus:outline-none ring-4 ring-upec-green/20"
          >
            <svg v-if="store.isBuffering" class="animate-spin h-10 w-10" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <svg v-else-if="!store.isPlaying" class="h-12 w-12 ml-2" fill="currentColor" viewBox="0 0 24 24">
              <path d="M8 5v14l11-7z"/>
            </svg>
            <svg v-else class="h-10 w-10" fill="currentColor" viewBox="0 0 24 24">
              <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>
            </svg>
          </button>

          <div class="mt-8 flex justify-center space-x-8 text-sm text-gray-500">
            <div class="flex flex-col items-center">
              <svg class="w-6 h-6 mb-1" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" /></svg>
              <span>{{ store.listenersCount }} Oyentes</span>
            </div>
            <div class="flex flex-col items-center">
              <svg class="w-6 h-6 mb-1" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3" /></svg>
              <span>Calidad 128kbps</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
