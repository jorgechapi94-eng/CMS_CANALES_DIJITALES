<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useApi } from '@/composables/useApi'
import ProgramCard from '@/components/programs/ProgramCard.vue'
import type { Program, PaginatedResponse } from '@/types'

const api = useApi()
const programs = ref<Program[]>([])
const loading = ref(true)

const selectedLevel = ref<string>('')
const selectedModality = ref<string>('')

const levels = [
  { value: '', label: 'Todos los niveles' },
  { value: 'grado', label: 'Grado' },
  { value: 'maestria', label: 'Maestría' },
  { value: 'doctorado', label: 'Doctorado' },
  { value: 'tecnico', label: 'Técnico' }
]

const modalities = [
  { value: '', label: 'Todas las modalidades' },
  { value: 'presencial', label: 'Presencial' },
  { value: 'virtual', label: 'Virtual' },
  { value: 'hibrido', label: 'Híbrido' }
]

const pagination = ref({ page: 1, total: 0, pages: 1 })

const fetchPrograms = async () => {
  loading.value = true
  try {
    let url = `/api/programs?page=${pagination.value.page}&per_page=12&is_active=true`
    if (selectedLevel.value) url += `&level=${selectedLevel.value}`
    if (selectedModality.value) url += `&modality=${selectedModality.value}`
    
    const { data } = await api.get<PaginatedResponse<Program>>(url)
    programs.value = data.items
    pagination.value.total = data.total
    pagination.value.pages = data.pages
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const applyFilters = () => {
  pagination.value.page = 1
  fetchPrograms()
}

onMounted(() => fetchPrograms())
</script>

<template>
  <div class="bg-white min-h-screen py-12">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-12">
        <h1 class="text-4xl font-extrabold text-gray-900 mb-4">Oferta Académica</h1>
        <p class="text-lg text-gray-600 max-w-2xl mx-auto">Construye tu futuro profesional con nuestros programas de educación superior.</p>
      </div>

      <div class="bg-gray-50 p-6 rounded-xl border border-gray-200 mb-10 flex flex-col md:flex-row gap-4 justify-center">
        <div class="w-full md:w-64">
          <label class="block text-sm font-medium text-gray-700 mb-1">Nivel Académico</label>
          <select v-model="selectedLevel" @change="applyFilters" class="input-field">
            <option v-for="lvl in levels" :key="lvl.value" :value="lvl.value">{{ lvl.label }}</option>
          </select>
        </div>
        <div class="w-full md:w-64">
          <label class="block text-sm font-medium text-gray-700 mb-1">Modalidad</label>
          <select v-model="selectedModality" @change="applyFilters" class="input-field">
            <option v-for="mod in modalities" :key="mod.value" :value="mod.value">{{ mod.label }}</option>
          </select>
        </div>
      </div>

      <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div v-for="i in 6" :key="i" class="card h-64 animate-pulse bg-gray-200"></div>
      </div>

      <div v-else-if="programs.length === 0" class="text-center py-16">
        <p class="text-gray-500 text-lg">No se encontraron programas que coincidan con los filtros.</p>
      </div>

      <div v-else>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-12">
          <ProgramCard v-for="prog in programs" :key="prog.id" :program="prog" />
        </div>
        
        <div v-if="pagination.pages > 1" class="flex justify-center items-center space-x-4">
          <button @click="pagination.page--; fetchPrograms()" :disabled="pagination.page === 1" class="btn-outline px-4 py-2">Anterior</button>
          <span class="text-gray-600">Página {{ pagination.page }} de {{ pagination.pages }}</span>
          <button @click="pagination.page++; fetchPrograms()" :disabled="pagination.page === pagination.pages" class="btn-outline px-4 py-2">Siguiente</button>
        </div>
      </div>
    </div>
  </div>
</template>
