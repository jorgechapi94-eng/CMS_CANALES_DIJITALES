<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useApi } from '@/composables/useApi'
import NewsCard from '@/components/news/NewsCard.vue'
import type { NewsItem, PaginatedResponse, Category } from '@/types'

const api = useApi()

const news = ref<NewsItem[]>([])
const categories = ref<Category[]>([])
const loading = ref(true)
const searchQuery = ref('')
const selectedCategory = ref<number | null>(null)

const pagination = ref({
  page: 1,
  total: 0,
  pages: 1
})

const fetchCategories = async () => {
  try {
    const { data } = await api.get('/api/categories')
    categories.value = data
  } catch (e) {
    console.error('Error fetching categories', e)
  }
}

const fetchNews = async () => {
  loading.value = true
  try {
    let url = `/api/news?page=${pagination.value.page}&per_page=9&status=published`
    if (searchQuery.value) url += `&search=${encodeURIComponent(searchQuery.value)}`
    if (selectedCategory.value) url += `&category_id=${selectedCategory.value}`
    
    const { data } = await api.get<PaginatedResponse<NewsItem>>(url)
    news.value = data.items
    pagination.value.total = data.total
    pagination.value.pages = data.pages
  } catch (e) {
    console.error('Error fetching news', e)
  } finally {
    loading.value = false
  }
}

const applyFilter = () => {
  pagination.value.page = 1
  fetchNews()
}

const setCategory = (catId: number | null) => {
  selectedCategory.value = catId
  applyFilter()
}

const nextPage = () => {
  if (pagination.value.page < pagination.value.pages) {
    pagination.value.page++
    fetchNews()
    window.scrollTo(0, 0)
  }
}

const prevPage = () => {
  if (pagination.value.page > 1) {
    pagination.value.page--
    fetchNews()
    window.scrollTo(0, 0)
  }
}

onMounted(() => {
  fetchCategories()
  fetchNews()
})
</script>

<template>
  <div class="bg-gray-50 min-h-screen py-12">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <div class="text-center mb-12">
        <h1 class="text-4xl font-extrabold text-gray-900 mb-4">Noticias UPEC</h1>
        <p class="text-lg text-gray-600 max-w-2xl mx-auto">Mantente informado sobre los últimos acontecimientos, investigaciones y eventos de nuestra comunidad universitaria.</p>
      </div>

      <!-- Filters -->
      <div class="bg-white p-4 rounded-xl shadow-sm border border-gray-100 mb-8 flex flex-col md:flex-row gap-4 items-center justify-between">
        <div class="w-full md:w-1/3 relative">
          <input 
            v-model="searchQuery" 
            @keyup.enter="applyFilter"
            type="text" 
            placeholder="Buscar noticias..." 
            class="input-field pl-10"
          >
          <svg class="w-5 h-5 text-gray-400 absolute left-3 top-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        
        <div class="flex flex-wrap gap-2 justify-center w-full md:w-auto">
          <button 
            @click="setCategory(null)" 
            :class="selectedCategory === null ? 'bg-upec-green text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
            class="px-4 py-2 rounded-full text-sm font-medium transition-colors"
          >
            Todas
          </button>
          <button 
            v-for="cat in categories" 
            :key="cat.id"
            @click="setCategory(cat.id)"
            :class="selectedCategory === cat.id ? 'bg-upec-green text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
            class="px-4 py-2 rounded-full text-sm font-medium transition-colors"
          >
            {{ cat.name }}
          </button>
        </div>
      </div>

      <!-- Content -->
      <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div v-for="i in 6" :key="i" class="card h-96 animate-pulse bg-gray-200"></div>
      </div>
      
      <div v-else-if="news.length === 0" class="text-center py-20 bg-white rounded-xl shadow-sm border border-gray-100">
        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9.5L17.5 4.5" />
        </svg>
        <h3 class="mt-2 text-sm font-medium text-gray-900">No se encontraron noticias</h3>
        <p class="mt-1 text-sm text-gray-500">Intenta cambiar los filtros de búsqueda.</p>
        <div class="mt-6">
          <button @click="searchQuery = ''; selectedCategory = null; applyFilter()" class="btn-outline">Limpiar filtros</button>
        </div>
      </div>
      
      <div v-else>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-12">
          <NewsCard v-for="item in news" :key="item.id" :news="item" />
        </div>
        
        <!-- Pagination -->
        <div v-if="pagination.pages > 1" class="flex justify-center items-center space-x-4">
          <button 
            @click="prevPage" 
            :disabled="pagination.page === 1"
            class="px-4 py-2 border border-gray-300 rounded-md bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Anterior
          </button>
          <span class="text-sm text-gray-700">
            Página <span class="font-medium">{{ pagination.page }}</span> de <span class="font-medium">{{ pagination.pages }}</span>
          </span>
          <button 
            @click="nextPage" 
            :disabled="pagination.page === pagination.pages"
            class="px-4 py-2 border border-gray-300 rounded-md bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Siguiente
          </button>
        </div>
      </div>

    </div>
  </div>
</template>
