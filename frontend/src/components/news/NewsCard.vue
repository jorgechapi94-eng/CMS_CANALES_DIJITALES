<script setup lang="ts">
import type { NewsItem } from '@/types'

defineProps<{
  news: NewsItem
}>()

const formatDate = (dateString: string | null) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('es-EC', { year: 'numeric', month: 'long', day: 'numeric' }).format(date)
}
</script>

<template>
  <div class="card flex flex-col h-full group hover:-translate-y-1 transition-transform duration-300">
    <div class="relative h-48 w-full overflow-hidden bg-gradient-to-br from-upec-green to-upec-green-dark">
      <img v-if="news.cover_image_url" :src="news.cover_image_url" :alt="news.title" class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105" />
      <div v-else class="w-full h-full flex items-center justify-center opacity-20">
        <span class="text-white font-bold text-4xl">UPEC</span>
      </div>
      <div class="absolute top-3 left-3 flex gap-2 flex-wrap">
        <span v-for="cat in news.categories" :key="cat.id" class="badge-yellow shadow-sm">{{ cat.name }}</span>
      </div>
    </div>
    
    <div class="p-5 flex flex-col flex-grow">
      <div class="text-xs text-gray-500 mb-2 flex items-center justify-between">
        <span>{{ formatDate(news.published_at || news.created_at) }}</span>
        <span v-if="news.author" class="font-medium">Por {{ news.author.username }}</span>
      </div>
      
      <h3 class="text-lg font-bold text-gray-900 mb-2 line-clamp-2 group-hover:text-upec-green transition-colors">
        <router-link :to="`/noticias/${news.slug}`" class="focus:outline-none">
          <span class="absolute inset-0" aria-hidden="true"></span>
          {{ news.title }}
        </router-link>
      </h3>
      
      <p class="text-sm text-gray-600 line-clamp-3 flex-grow">{{ news.excerpt }}</p>
      
      <div class="mt-4 flex items-center text-upec-green text-sm font-medium">
        Leer más
        <svg class="w-4 h-4 ml-1 transform group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
        </svg>
      </div>
    </div>
  </div>
</template>
