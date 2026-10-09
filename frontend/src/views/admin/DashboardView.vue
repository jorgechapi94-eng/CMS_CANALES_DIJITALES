<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import AdminSidebar from '@/components/layout/AdminSidebar.vue'
import { useApi } from '@/composables/useApi'

const authStore = useAuthStore()
const api = useApi()

const stats = ref({
  news: 0,
  newspapers: 0,
  programs: 0,
  users: 0
})
const recentActivity = ref<any[]>([])
const loading = ref(true)

const fetchDashboardData = async () => {
  try {
    // In a real app, this would be a single /api/admin/dashboard endpoint
    // For this mockup, we'll try to fetch counts individually
    const [newsRes, papersRes, progRes, usersRes] = await Promise.allSettled([
      api.get('/api/news?per_page=1'),
      api.get('/api/newspapers?per_page=1'),
      api.get('/api/programs?per_page=1'),
      authStore.isSuperAdmin ? api.get('/api/users?per_page=1') : Promise.resolve({ data: { total: 0 } })
    ])
    
    stats.value.news = newsRes.status === 'fulfilled' ? newsRes.value.data.total : 0
    stats.value.newspapers = papersRes.status === 'fulfilled' ? papersRes.value.data.total : 0
    stats.value.programs = progRes.status === 'fulfilled' ? progRes.value.data.total : 0
    stats.value.users = usersRes.status === 'fulfilled' ? usersRes.value.data.total : 0
    
    if (newsRes.status === 'fulfilled') {
      const { data } = await api.get('/api/news?per_page=5')
      recentActivity.value = data.items
    }
  } catch (error) {
    console.error('Error fetching dashboard data', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => fetchDashboardData())
</script>

<template>
  <div class="flex min-h-screen bg-gray-50">
    <AdminSidebar />
    <div class="flex-1 p-8 overflow-y-auto">
      <div class="flex justify-between items-center mb-8">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p class="text-gray-500 mt-1">Bienvenido, {{ authStore.user?.username }}</p>
        </div>
        <div class="flex space-x-3">
          <router-link v-if="authStore.hasRole('editor')" to="/admin/noticias" class="btn-primary py-2 text-sm">Nueva Noticia</router-link>
          <router-link v-if="authStore.hasRole('editor')" to="/admin/periodicos" class="btn-outline py-2 text-sm bg-white">Subir Periódico</router-link>
          <router-link v-if="authStore.hasRole('gestor_programas')" to="/admin/programas" class="btn-outline py-2 text-sm bg-white">Nuevo Programa</router-link>
        </div>
      </div>
      
      <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div v-for="i in 4" :key="i" class="bg-white rounded-xl shadow-sm p-6 animate-pulse h-32 border border-gray-100"></div>
      </div>
      
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div class="bg-white rounded-xl shadow-sm p-6 border-l-4 border-upec-green border-y border-r border-gray-100">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-500 uppercase">Noticias</p>
              <p class="text-3xl font-bold text-gray-900 mt-1">{{ stats.news }}</p>
            </div>
            <div class="w-12 h-12 bg-green-50 rounded-full flex items-center justify-center text-upec-green text-xl">📰</div>
          </div>
        </div>
        <div class="bg-white rounded-xl shadow-sm p-6 border-l-4 border-upec-yellow border-y border-r border-gray-100">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-500 uppercase">Periódicos</p>
              <p class="text-3xl font-bold text-gray-900 mt-1">{{ stats.newspapers }}</p>
            </div>
            <div class="w-12 h-12 bg-yellow-50 rounded-full flex items-center justify-center text-upec-yellow-dark text-xl">🗞️</div>
          </div>
        </div>
        <div class="bg-white rounded-xl shadow-sm p-6 border-l-4 border-blue-500 border-y border-r border-gray-100">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-500 uppercase">Programas</p>
              <p class="text-3xl font-bold text-gray-900 mt-1">{{ stats.programs }}</p>
            </div>
            <div class="w-12 h-12 bg-blue-50 rounded-full flex items-center justify-center text-blue-500 text-xl">🎓</div>
          </div>
        </div>
        <div v-if="authStore.isSuperAdmin" class="bg-white rounded-xl shadow-sm p-6 border-l-4 border-purple-500 border-y border-r border-gray-100">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-500 uppercase">Usuarios</p>
              <p class="text-3xl font-bold text-gray-900 mt-1">{{ stats.users }}</p>
            </div>
            <div class="w-12 h-12 bg-purple-50 rounded-full flex items-center justify-center text-purple-500 text-xl">👥</div>
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <h2 class="text-lg font-bold text-gray-900 mb-4 border-b pb-2">Actividad Reciente (Noticias)</h2>
        <div v-if="loading" class="animate-pulse space-y-4">
          <div v-for="i in 3" :key="i" class="h-12 bg-gray-100 rounded"></div>
        </div>
        <div v-else-if="recentActivity.length === 0" class="text-gray-500 text-center py-4">
          No hay actividad reciente.
        </div>
        <ul v-else class="divide-y divide-gray-100">
          <li v-for="item in recentActivity" :key="item.id" class="py-3 flex justify-between items-center hover:bg-gray-50 px-2 rounded transition-colors">
            <div>
              <p class="text-sm font-medium text-gray-900 line-clamp-1">{{ item.title }}</p>
              <p class="text-xs text-gray-500">{{ new Date(item.created_at).toLocaleDateString() }} - Por {{ item.author?.username }}</p>
            </div>
            <span :class="{
              'badge-green': item.status === 'published',
              'bg-gray-100 text-gray-800': item.status === 'draft',
              'bg-red-100 text-red-800': item.status === 'archived'
            }" class="px-2 py-1 rounded-full text-xs font-medium">
              {{ item.status }}
            </span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>
