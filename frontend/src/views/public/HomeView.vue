<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useApi } from '@/composables/useApi'
import NewsCard from '@/components/news/NewsCard.vue'
import ProgramCard from '@/components/programs/ProgramCard.vue'
import type { NewsItem, Program, YouTubeVideo } from '@/types'

const api = useApi()

const latestNews = ref<NewsItem[]>([])
const latestVideos = ref<YouTubeVideo[]>([])
const featuredPrograms = ref<Program[]>([])
const loading = ref(true)

const fetchHomeData = async () => {
  try {
    loading.value = true
    const [newsRes, ytRes, progRes] = await Promise.all([
      api.get('/api/news?per_page=6&status=published'),
      api.get('/api/youtube/latest?limit=4').catch(() => ({ data: [] })),
      api.get('/api/programs?limit=3&is_active=true')
    ])
    
    latestNews.value = newsRes.data.items || []
    latestVideos.value = ytRes.data || []
    featuredPrograms.value = progRes.data.items?.slice(0, 3) || []
  } catch (error) {
    console.error('Error fetching home data:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchHomeData()
})
</script>

<template>
  <div>
    <!-- Hero Section -->
    <section class="relative bg-upec-green-dark text-white overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-r from-upec-green to-transparent opacity-90 z-10"></div>
      <!-- Placeholder background image -->
      <img src="https://images.unsplash.com/photo-1541339907198-e08756dedf3f?ixlib=rb-1.2.1&auto=format&fit=crop&w=1920&q=80" alt="Campus UPEC" class="absolute inset-0 w-full h-full object-cover" />
      
      <div class="relative z-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-32 lg:py-48">
        <div class="md:w-2/3">
          <h1 class="text-4xl md:text-5xl lg:text-6xl font-extrabold tracking-tight mb-4">
            Universidad Politécnica Estatal del Carchi
          </h1>
          <p class="text-xl md:text-2xl font-light mb-8 text-gray-100">
            Formando profesionales de excelencia para el desarrollo de la sociedad ecuatoriana.
          </p>
          <div class="flex flex-wrap gap-4">
            <router-link to="/programas" class="btn-secondary text-lg">Explorar Programas</router-link>
            <router-link to="/noticias" class="bg-white/20 hover:bg-white/30 text-white px-6 py-2.5 rounded-lg font-medium backdrop-blur-sm transition-colors duration-200">Últimas Noticias</router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Latest News -->
    <section class="py-16 bg-gray-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-end mb-8">
          <div>
            <h2 class="text-3xl font-bold text-gray-900 border-l-4 border-upec-green pl-3">Últimas Noticias</h2>
            <p class="mt-2 text-gray-600">Entérate de los acontecimientos más importantes de nuestra comunidad.</p>
          </div>
          <router-link to="/noticias" class="text-upec-green font-medium hover:underline hidden sm:block">Ver todas las noticias &rarr;</router-link>
        </div>
        
        <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div v-for="i in 3" :key="i" class="card h-96 animate-pulse bg-gray-200"></div>
        </div>
        <div v-else-if="latestNews.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <NewsCard v-for="news in latestNews" :key="news.id" :news="news" />
        </div>
        <div v-else class="text-center py-12 text-gray-500">
          No hay noticias recientes para mostrar.
        </div>
        <div class="mt-8 text-center sm:hidden">
          <router-link to="/noticias" class="btn-outline inline-block">Ver todas las noticias</router-link>
        </div>
      </div>
    </section>

    <!-- UPEC TV Preview -->
    <section class="py-16 bg-white" v-if="latestVideos.length > 0">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-end mb-8">
          <div>
            <h2 class="text-3xl font-bold text-gray-900 border-l-4 border-upec-yellow pl-3">UPEC TV</h2>
            <p class="mt-2 text-gray-600">Disfruta de nuestra producción audiovisual institucional.</p>
          </div>
          <router-link to="/tv" class="text-upec-green font-medium hover:underline hidden sm:block">Ir a UPEC TV &rarr;</router-link>
        </div>
        
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <a v-for="video in latestVideos" :key="video.id" :href="video.youtubeUrl" target="_blank" class="group relative aspect-video bg-gray-100 rounded-xl overflow-hidden shadow-sm block">
            <img :src="video.thumbnails.medium?.url || video.thumbnails.default?.url" :alt="video.title" class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105" />
            <div class="absolute inset-0 bg-black/40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
              <svg class="w-12 h-12 text-white" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
            </div>
            <div class="absolute bottom-0 left-0 right-0 p-3 bg-gradient-to-t from-black/80 to-transparent">
              <h4 class="text-white text-sm font-medium line-clamp-2">{{ video.title }}</h4>
            </div>
          </a>
        </div>
      </div>
    </section>

    <!-- Featured Programs -->
    <section class="py-16 bg-gray-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-end mb-8">
          <div>
            <h2 class="text-3xl font-bold text-gray-900 border-l-4 border-upec-green pl-3">Oferta Académica</h2>
            <p class="mt-2 text-gray-600">Descubre los programas que tenemos para ti.</p>
          </div>
          <router-link to="/programas" class="text-upec-green font-medium hover:underline hidden sm:block">Ver todos los programas &rarr;</router-link>
        </div>
        
        <div v-if="loading" class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div v-for="i in 3" :key="i" class="card h-64 animate-pulse bg-gray-200"></div>
        </div>
        <div v-else-if="featuredPrograms.length > 0" class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <ProgramCard v-for="prog in featuredPrograms" :key="prog.id" :program="prog" />
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-20 bg-upec-yellow">
      <div class="max-w-4xl mx-auto px-4 text-center">
        <h2 class="text-3xl md:text-4xl font-bold text-upec-green-dark mb-6">Sé parte de la familia UPEC</h2>
        <p class="text-lg text-upec-green-dark/80 mb-8 font-medium">Únete a nuestra comunidad universitaria y construye tu futuro con nosotros.</p>
        <router-link to="/programas" class="inline-block bg-upec-green text-white px-8 py-3 rounded-lg font-bold text-lg hover:bg-upec-green-dark shadow-lg transition-all hover:-translate-y-1">
          Conoce nuestra oferta
        </router-link>
      </div>
    </section>
  </div>
</template>
