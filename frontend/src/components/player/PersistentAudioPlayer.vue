<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useAudioPlayerStore } from '@/stores/audioPlayer'

const store = useAudioPlayerStore()
const audioRef = ref<HTMLAudioElement | null>(null)
let pollInterval: ReturnType<typeof setInterval> | null = null

const togglePlay = async () => {
  if (!audioRef.value) return
  
  if (store.isPlaying) {
    audioRef.value.pause()
    audioRef.value.src = ''
    audioRef.value.load() // purge buffer
    store.setPlaying(false)
  } else {
    store.setBuffering(true)
    audioRef.value.src = store.streamUrl
    audioRef.value.load()
    try {
      await audioRef.value.play()
      store.setPlaying(true)
    } catch (e) {
      store.hasError = true
    } finally {
      store.setBuffering(false)
    }
  }
}

const onVolumeChange = (e: Event) => {
  const val = parseFloat((e.target as HTMLInputElement).value)
  store.setVolume(val)
}

watch(() => store.volume, (newVol) => {
  if (audioRef.value) audioRef.value.volume = newVol
})

watch(() => store.isMuted, (muted) => {
  if (audioRef.value) audioRef.value.muted = muted
})

const onAudioWaiting = () => store.setBuffering(true)
const onAudioPlaying = () => {
  store.setBuffering(false)
  store.hasError = false
}
const onAudioError = () => {
  store.hasError = true
  store.setBuffering(false)
  store.setPlaying(false)
}

onMounted(() => {
  if (audioRef.value) {
    audioRef.value.volume = store.volume
    audioRef.value.muted = store.isMuted
  }
  
  if ('mediaSession' in navigator) {
    navigator.mediaSession.setActionHandler('play', togglePlay)
    navigator.mediaSession.setActionHandler('pause', togglePlay)
    navigator.mediaSession.setActionHandler('stop', togglePlay)
  }

  pollInterval = setInterval(() => {
    store.updateMetadata()
  }, 15000)
  store.updateMetadata()
})

onUnmounted(() => {
  if (pollInterval) clearInterval(pollInterval)
})
</script>

<template>
  <div class="fixed bottom-0 left-0 w-full bg-slate-900 border-t border-slate-800 text-white z-50 h-20 shadow-lg">
    <audio 
      ref="audioRef"
      @waiting="onAudioWaiting"
      @playing="onAudioPlaying"
      @stalled="onAudioWaiting"
      @error="onAudioError"
      class="hidden"
    ></audio>

    <div class="max-w-7xl mx-auto px-4 h-full flex items-center justify-between">
      <!-- Left: Station Info -->
      <div class="flex items-center space-x-4 flex-1 overflow-hidden">
        <div class="flex items-center space-x-2">
          <span class="relative flex h-3 w-3">
            <span v-if="store.isPlaying" class="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-3 w-3" :class="store.isPlaying ? 'bg-red-500' : 'bg-gray-500'"></span>
          </span>
          <span class="text-xs font-bold tracking-wider text-gray-400">EN VIVO</span>
        </div>
        <div class="truncate hidden sm:block">
          <h4 class="font-semibold text-sm truncate">{{ store.currentTrack }}</h4>
          <p class="text-xs text-gray-400 truncate">{{ store.stationName }}</p>
        </div>
      </div>

      <!-- Center: Controls -->
      <div class="flex-1 flex justify-center items-center">
        <button 
          @click="togglePlay"
          class="h-12 w-12 rounded-full bg-red-600 hover:bg-red-700 flex items-center justify-center transition-transform hover:scale-105 focus:outline-none"
          :class="{ 'opacity-50 cursor-not-allowed': store.hasError }"
        >
          <svg v-if="store.isBuffering" class="animate-spin h-6 w-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <svg v-else-if="!store.isPlaying" class="h-6 w-6 ml-1" fill="currentColor" viewBox="0 0 24 24">
            <path d="M8 5v14l11-7z"/>
          </svg>
          <svg v-else class="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
            <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>
          </svg>
        </button>
      </div>

      <!-- Right: Volume -->
      <div class="flex-1 flex justify-end items-center space-x-3 hidden sm:flex">
        <button @click="store.toggleMute" class="text-gray-400 hover:text-white focus:outline-none">
          <svg v-if="store.isMuted || store.volume === 0" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" clip-rule="evenodd" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2" />
          </svg>
          <svg v-else class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
          </svg>
        </button>
        <input 
          type="range" 
          min="0" 
          max="1" 
          step="0.01" 
          :value="store.volume"
          @input="onVolumeChange"
          class="w-24 h-1 bg-gray-600 rounded-lg appearance-none cursor-pointer accent-upec-yellow"
        />
      </div>
    </div>
  </div>
</template>
