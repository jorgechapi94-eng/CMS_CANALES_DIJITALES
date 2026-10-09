<script setup lang="ts">
import { ref, computed } from 'vue'
import { useMediaInterlock } from '@/composables/useMediaInterlock'

const props = defineProps<{
  videoUrl?: string
  videoId?: string
}>()

const emit = defineEmits<{
  (e: 'play'): void
  (e: 'pause'): void
}>()

const isPlaying = ref(false)
const hasStarted = ref(false)

const { onTVPlay, onTVPause } = useMediaInterlock(isPlaying)

const playVideo = () => {
  hasStarted.value = true
  isPlaying.value = true
  emit('play')
}

// For generic video events if it's not YouTube
const onGenericPlay = () => {
  isPlaying.value = true
  emit('play')
}

const onGenericPause = () => {
  isPlaying.value = false
  emit('pause')
}

const ytUrl = computed(() => {
  if (!props.videoId) return ''
  // autoplay=1 starts it when the iframe loads
  return `https://www.youtube.com/embed/${props.videoId}?autoplay=1&enablejsapi=1`
})
</script>

<template>
  <div class="relative w-full aspect-video bg-black rounded-xl overflow-hidden shadow-lg group">
    <template v-if="videoId">
      <div v-if="!hasStarted" class="absolute inset-0 flex items-center justify-center bg-gray-900 cursor-pointer" @click="playVideo">
        <img :src="`https://img.youtube.com/vi/${videoId}/maxresdefault.jpg`" class="absolute inset-0 w-full h-full object-cover opacity-60" alt="Video thumbnail" />
        <button class="relative z-10 w-20 h-20 bg-red-600 rounded-full flex items-center justify-center hover:bg-red-700 transition-transform transform hover:scale-110">
          <svg class="w-10 h-10 text-white ml-2" fill="currentColor" viewBox="0 0 24 24">
            <path d="M8 5v14l11-7z" />
          </svg>
        </button>
      </div>
      <iframe 
        v-else 
        :src="ytUrl" 
        class="w-full h-full border-0" 
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen
      ></iframe>
    </template>
    
    <template v-else-if="videoUrl">
      <video 
        class="w-full h-full"
        controls
        @play="onGenericPlay"
        @pause="onGenericPause"
        :src="videoUrl"
      ></video>
    </template>
    
    <div v-else class="flex flex-col items-center justify-center h-full text-gray-500">
      <svg class="w-16 h-16 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
      </svg>
      <p>Señal de TV no disponible</p>
    </div>
  </div>
</template>
