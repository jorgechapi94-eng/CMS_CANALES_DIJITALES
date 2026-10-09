<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useApi } from '@/composables/useApi'
import type { Newspaper, PaginatedResponse } from '@/types'

const api = useApi()
const newspapers = ref<Newspaper[]>([])
const loading = ref(true)
const pagination = ref({ page: 1, total: 0, pages: 1 })

const fetchNewspapers = async () => {
  loading.value = true
  try {
    const { data } = await api.get<PaginatedResponse<Newspaper>>(`/api/newspapers?page=${pagination.value.page}&per_page=12`)
    newspapers.value = data.items
    pagination.value.total = data.total
    pagination.value.pages = data.pages
  } catch (error) {
    console.error('Error fetching newspapers', error)
  } finally {
    loading.value = false
  }
}

const nextPage = () => {
  if (pagination.value.page < pagination.value.pages) {
    pagination.value.page++
    fetchNewspapers()
  }
}

const prevPage = () => {
  if (pagination.value.page > 1) {
    pagination.value.page--
    fetchNewspapers()
  }
}

const formatSize = (bytes: number | null) => {
  if (!bytes) return 'Desconocido'
  const mb = bytes / (1024 * 1024)
  return mb.toFixed(2) + ' MB'
}

onMounted(() => {
  fetchNewspapers()
})
</script>

<template>
  <div class="bg-gray-50 min-h-screen py-12">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-12">
        <h1 class="text-4xl font-extrabold text-gray-900 mb-4">Periódicos Digitales</h1>
        <p class="text-lg text-gray-600 max-w-2xl mx-auto">Consulta y descarga nuestras ediciones impresas en formato digital.</p>
      </div>

      <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        <div v-for="i in 8" :key="i" class="card h-80 animate-pulse bg-gray-200"></div>
      </div>

      <div v-else-if="newspapers.length === 0" class="text-center py-20 bg-white rounded-xl shadow-sm border border-gray-100">
        <p class="text-gray-500">No hay periódicos disponibles.</p>
      </div>

      <div v-else>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 mb-12">
          <div v-for="paper in newspapers" :key="paper.id" class="card group flex flex-col h-full">
            <div class="relative h-64 bg-gray-100 border-b border-gray-200 overflow-hidden flex items-center justify-center">
              <img v-if="paper.cover_thumbnail_url" :src="paper.cover_thumbnail_url" :alt="paper.title" class="w-full h-full object-contain" />
              <svg v-else class="w-20 h-20 text-gray-400" fill="currentColor" viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V5h14v14z"/><path d="M7 12h10v2H7zm0-4h10v2H7zm0 8h7v2H7z"/></svg>
            </div>
            <div class="p-4 flex flex-col flex-grow">
              <h3 class="font-bold text-gray-900 line-clamp-2 mb-2 group-hover:text-upec-green">{{ paper.title }}</h3>
              <p class="text-sm text-gray-500 mb-1">Publicado: {{ paper.publication_date || 'N/A' }}</p>
              <p class="text-xs text-gray-400 mb-4">Tamaño: {{ formatSize(paper.file_size_bytes) }}</p>
              
              <div class="mt-auto flex gap-2">
                <a :href="paper.pdf_url" target="_blank" class="flex-1 btn-outline py-1.5 text-center text-sm flex justify-center items-center">
                  Ver PDF
                </a>
                <a :href="paper.pdf_url" download class="flex-1 btn-primary py-1.5 text-center text-sm flex justify-center items-center">
                  Descargar
                </a>
              </div>
            </div>
          </div>
        </div>

        <div v-if="pagination.pages > 1" class="flex justify-center items-center space-x-4">
          <button @click="prevPage" :disabled="pagination.page === 1" class="px-4 py-2 border border-gray-300 rounded-md bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50">Anterior</button>
          <span class="text-sm text-gray-700">Página <span class="font-medium">{{ pagination.page }}</span> de <span class="font-medium">{{ pagination.pages }}</span></span>
          <button @click="nextPage" :disabled="pagination.page === pagination.pages" class="px-4 py-2 border border-gray-300 rounded-md bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50">Siguiente</button>
        </div>
      </div>
    </div>
  </div>
</template>
