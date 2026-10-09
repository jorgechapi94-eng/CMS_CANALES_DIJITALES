<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useApi } from '@/composables/useApi'
import type { Program } from '@/types'

const route = useRoute()
const api = useApi()
const program = ref<Program | null>(null)
const loading = ref(true)
const activeTab = ref('docentes')

const fetchProgram = async () => {
  loading.value = true
  try {
    const { data } = await api.get(`/api/programs/${route.params.id}`)
    program.value = data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

onMounted(() => fetchProgram())
</script>

<template>
  <div class="bg-gray-50 min-h-screen py-10">
    <div v-if="loading" class="max-w-7xl mx-auto px-4">
      <div class="h-40 bg-gray-200 animate-pulse rounded-xl mb-8"></div>
    </div>
    
    <div v-else-if="!program" class="text-center py-20">
      <h2 class="text-2xl font-bold text-gray-900">Programa no encontrado</h2>
      <router-link to="/programas" class="text-upec-green hover:underline mt-4 inline-block">Volver a programas</router-link>
    </div>

    <div v-else class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <router-link to="/programas" class="inline-flex items-center text-upec-green hover:underline mb-6">
        <svg class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" /></svg>
        Volver a Oferta Académica
      </router-link>

      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden mb-8">
        <div class="bg-upec-green-dark p-8 md:p-12 text-white relative overflow-hidden">
          <div class="absolute right-0 top-0 opacity-10 transform translate-x-1/4 -translate-y-1/4">
            <svg class="w-64 h-64" fill="currentColor" viewBox="0 0 24 24"><path d="M12 3L1 9l4 2.18v6L12 21l7-3.82v-6l2-1.09V17h2V9L12 3zm6.82 6L12 12.72 5.18 9 12 5.28 18.82 9zM17 15.99l-5 2.73-5-2.73v-3.72L12 15l5-2.73v3.72z"/></svg>
          </div>
          <div class="relative z-10">
            <div class="flex gap-3 mb-4">
              <span class="bg-white/20 px-3 py-1 rounded-full text-sm font-medium capitalize backdrop-blur-sm">{{ program.level }}</span>
              <span class="bg-upec-yellow text-upec-green-dark px-3 py-1 rounded-full text-sm font-bold capitalize">{{ program.modality }}</span>
            </div>
            <h1 class="text-3xl md:text-5xl font-extrabold mb-4">{{ program.title }}</h1>
            <p class="text-lg text-gray-100 max-w-3xl">{{ program.description }}</p>
          </div>
        </div>

        <!-- Tabs -->
        <div class="border-b border-gray-200">
          <nav class="flex -mb-px px-6">
            <button @click="activeTab = 'docentes'" :class="['py-4 px-6 text-center border-b-2 font-medium text-sm', activeTab === 'docentes' ? 'border-upec-green text-upec-green' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300']">
              Planta Docente ({{ program.teachers?.length || 0 }})
            </button>
            <button @click="activeTab = 'estudiantes'" :class="['py-4 px-6 text-center border-b-2 font-medium text-sm', activeTab === 'estudiantes' ? 'border-upec-green text-upec-green' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300']">
              Estudiantes Destacados ({{ program.students?.length || 0 }})
            </button>
            <button @click="activeTab = 'proyectos'" :class="['py-4 px-6 text-center border-b-2 font-medium text-sm', activeTab === 'proyectos' ? 'border-upec-green text-upec-green' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300']">
              Proyectos ({{ program.projects?.length || 0 }})
            </button>
          </nav>
        </div>

        <div class="p-6 md:p-8 min-h-[400px]">
          <!-- Docentes -->
          <div v-if="activeTab === 'docentes'">
            <div v-if="!program.teachers?.length" class="text-gray-500 text-center py-10">No hay docentes registrados.</div>
            <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              <div v-for="teacher in program.teachers" :key="teacher.id" class="flex items-center p-4 border border-gray-100 rounded-xl bg-gray-50">
                <img v-if="teacher.photo_url" :src="teacher.photo_url" class="w-16 h-16 rounded-full object-cover mr-4 shadow-sm" />
                <div v-else class="w-16 h-16 rounded-full bg-upec-green-100 text-upec-green flex items-center justify-center font-bold text-xl mr-4">{{ teacher.full_name.charAt(0) }}</div>
                <div>
                  <h4 class="font-bold text-gray-900">{{ teacher.full_name }}</h4>
                  <p class="text-sm text-upec-green font-medium">{{ teacher.title_degree }}</p>
                  <p class="text-xs text-gray-500 mt-1">{{ teacher.email }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Estudiantes -->
          <div v-if="activeTab === 'estudiantes'">
            <div v-if="!program.students?.length" class="text-gray-500 text-center py-10">No hay estudiantes registrados.</div>
            <div v-else class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nombre del Estudiante</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Año de Ingreso</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-for="student in program.students" :key="student.id">
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ student.full_name }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ student.enrollment_year }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Proyectos -->
          <div v-if="activeTab === 'proyectos'">
            <div v-if="!program.projects?.length" class="text-gray-500 text-center py-10">No hay proyectos registrados.</div>
            <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div v-for="project in program.projects" :key="project.id" class="p-6 border border-gray-200 rounded-xl hover:shadow-md transition-shadow bg-white">
                <h4 class="text-lg font-bold text-gray-900 mb-2">{{ project.title }}</h4>
                <p class="text-gray-600 text-sm mb-4">{{ project.description }}</p>
                <a v-if="project.link_url" :href="project.link_url" target="_blank" class="text-upec-green hover:underline text-sm font-medium flex items-center">
                  Ver proyecto <svg class="w-4 h-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" /></svg>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
