<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useApi } from '@/composables/useApi'
import TVPlayer from '@/components/player/TVPlayer.vue'
import type { YouTubeVideo } from '@/types'

const api = useApi()
const recentVideos = ref<YouTubeVideo[]>([])
const loading = ref(true)
const tvStreamUrl = ref('https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8') // Placeholder HLS stream

const fetchRecentVideos = async () => {
  try {
    const { data } = await api.get('/api/youtube/latest?limit=8')
    recentVideos.value = data
  } catch (error) {
    console.error('Error fetching videos', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => fetchRecentVideos())
</script>

<template>
  <div class="bg-gray-900 min-h-screen pb-16 text-white">
    <div class="bg-black py-8 border-b border-gray-800">
      <div class="max-w-5xl mx-auto px-4 text-center">
        <h1 class="text-4xl md:text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-upec-yellow to-upec-green-light inline-block mb-4">UPEC TV</h1>
        <div class="flex items-center justify-center space-x-2 text-red-500 font-bold mb-8">
          <span class="animate-pulse h-3 w-3 bg-red-600 rounded-full inline-block"></span>
          <span>Transmisión en Vivo</span>
        </div>
        
        <div class="max-w-4xl mx-auto shadow-2xl shadow-upec-green/20 rounded-xl overflow-hidden ring-1 ring-gray-800">
          <TVPlayer :video-url="tvStreamUrl" />
        </div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-16">
      <h2 class="text-2xl font-bold mb-8 border-l-4 border-upec-yellow pl-3">Videos Recientes</h2>
      
      <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        <div v-for="i in 4" :key="i" class="aspect-video bg-gray-800 animate-pulse rounded-xl"></div>
      </div>
      
      <div v-else-if="recentVideos.length === 0" class="text-gray-500 py-10 text-center">
        No hay videos recientes disponibles.
      </div>

      <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        <a v-for="video in recentVideos" :key="video.id" :href="video.youtubeUrl" target="_blank" class="group block">
          <div class="relative aspect-video bg-gray-800 rounded-xl overflow-hidden mb-3 border border-gray-700 group-hover:border-upec-yellow transition-colors">
            <img :src="video.thumbnails.medium?.url" :alt="video.title" class="w-full h-full object-cover transform group-hover:scale-105 transition-transform duration-300" />
            <div class="absolute inset-0 bg-black/20 group-hover:bg-black/10 transition-colors flex items-center justify-center">
              <div class="w-12 h-12 rounded-full bg-red-600 flex items-center justify-center opacity-90 group-hover:scale-110 transition-transform">
                <svg class="w-6 h-6 text-white ml-1" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
              </div>
            </div>
          </div>
          <h3 class="font-medium text-sm line-clamp-2 group-hover:text-upec-yellow transition-colors">{{ video.title }}</h3>
          <p class="text-xs text-gray-400 mt-1">{{ new Date(video.publishedAt).toLocaleDateString() }}</p>
        </a>
      </div>
    </div>
  </div>
</template>
