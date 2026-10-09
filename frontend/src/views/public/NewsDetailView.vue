<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useApi } from '@/composables/useApi'
import type { NewsItem } from '@/types'
import DOMPurify from 'dompurify'

const route = useRoute()
const router = useRouter()
const api = useApi()

const news = ref<NewsItem | null>(null)
const loading = ref(true)
const error = ref(false)

const fetchNewsDetail = async () => {
  const slug = route.params.slug as string
  loading.value = true
  try {
    const { data } = await api.get(`/api/news/${slug}`)
    if (data.content_html) {
      data.content_html = DOMPurify.sanitize(data.content_html, { ADD_TAGS: ['iframe'], ADD_ATTR: ['allow', 'allowfullscreen', 'frameborder', 'scrolling'] })
    }
    news.value = data
  } catch (e) {
    console.error('Error fetching news detail', e)
    error.value = true
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString: string | undefined | null) => {
  if (!dateString) return ''
  return new Intl.DateTimeFormat('es-EC', { 
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' 
  }).format(new Date(dateString))
}

onMounted(() => {
  fetchNewsDetail()
})
</script>

<template>
  <div class="bg-white min-h-screen pb-16">
    <div v-if="loading" class="animate-pulse">
      <div class="w-full h-64 md:h-96 bg-gray-200"></div>
      <div class="max-w-4xl mx-auto px-4 mt-8 space-y-4">
        <div class="h-10 bg-gray-200 rounded w-3/4"></div>
        <div class="h-4 bg-gray-200 rounded w-1/4"></div>
        <div class="space-y-2 mt-8">
          <div class="h-4 bg-gray-200 rounded w-full"></div>
          <div class="h-4 bg-gray-200 rounded w-full"></div>
          <div class="h-4 bg-gray-200 rounded w-5/6"></div>
        </div>
      </div>
    </div>

    <div v-else-if="error || !news" class="max-w-4xl mx-auto px-4 py-20 text-center">
      <h2 class="text-3xl font-bold text-gray-900 mb-4">Noticia no encontrada</h2>
      <p class="text-gray-600 mb-8">La noticia que buscas no existe o ha sido eliminada.</p>
      <router-link to="/noticias" class="btn-primary">Volver a Noticias</router-link>
    </div>

    <article v-else>
      <!-- Hero Banner -->
      <div class="relative w-full h-64 md:h-[28rem] bg-upec-green-dark">
        <img v-if="news.cover_image_url" :src="news.cover_image_url" :alt="news.title" class="w-full h-full object-cover opacity-90" />
        <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent"></div>
        <div class="absolute bottom-0 left-0 w-full p-6 md:p-12 max-w-4xl mx-auto left-0 right-0">
          <div class="flex flex-wrap gap-2 mb-4">
            <span v-for="cat in news.categories" :key="cat.id" class="badge-yellow text-sm">{{ cat.name }}</span>
          </div>
          <h1 class="text-3xl md:text-5xl font-bold text-white mb-4 leading-tight shadow-sm">{{ news.title }}</h1>
        </div>
      </div>

      <div class="max-w-4xl mx-auto px-4 sm:px-6 mt-8">
        <!-- Meta Info -->
        <div class="flex flex-col sm:flex-row sm:items-center justify-between border-b border-gray-200 pb-6 mb-8 text-gray-600 text-sm">
          <div class="flex items-center mb-4 sm:mb-0">
            <div class="h-10 w-10 rounded-full bg-upec-green text-white flex items-center justify-center font-bold text-lg mr-3">
              {{ news.author?.username.charAt(0).toUpperCase() || 'U' }}
            </div>
            <div>
              <p class="font-medium text-gray-900">Por {{ news.author?.username || 'UPEC' }}</p>
              <p>{{ formatDate(news.published_at || news.created_at) }}</p>
            </div>
          </div>
          <router-link to="/noticias" class="text-upec-green hover:underline flex items-center">
            <svg class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" /></svg>
            Volver
          </router-link>
        </div>

        <!-- Excerpt -->
        <p v-if="news.excerpt" class="text-xl text-gray-600 italic mb-8 border-l-4 border-upec-yellow pl-4">
          {{ news.excerpt }}
        </p>

        <!-- Content -->
        <div class="prose-upec prose-lg max-w-none text-gray-800" v-html="news.content_html"></div>
      </div>
    </article>
  </div>
</template>
