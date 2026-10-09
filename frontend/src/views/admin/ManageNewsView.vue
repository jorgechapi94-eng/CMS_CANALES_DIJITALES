<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import AdminSidebar from '@/components/layout/AdminSidebar.vue'
import BaseModal from '@/components/ui/BaseModal.vue'
import ConfirmDialog from '@/components/ui/ConfirmDialog.vue'
import NewsEditor from '@/components/news/NewsEditor.vue'
import { useApi } from '@/composables/useApi'
import type { NewsItem, Category, PaginatedResponse } from '@/types'

const api = useApi()

const news = ref<NewsItem[]>([])
const categories = ref<Category[]>([])
const loading = ref(true)
const searchQuery = ref('')
const pagination = ref({ page: 1, total: 0, pages: 1 })

const showModal = ref(false)
const showDeleteConfirm = ref(false)
const itemToDelete = ref<number | null>(null)
const isEditing = ref(false)
const saving = ref(false)

const formData = reactive({
  id: null as number | null,
  title: '',
  excerpt: '',
  content_html: '',
  status: 'draft' as 'draft' | 'published' | 'archived',
  category_ids: [] as number[],
  cover_image_file: null as File | null,
  cover_image_url: '' as string | null
})

const fileInput = ref<HTMLInputElement | null>(null)

const fetchCategories = async () => {
  const { data } = await api.get('/api/categories')
  categories.value = data
}

const fetchNews = async () => {
  loading.value = true
  try {
    let url = `/api/news?page=${pagination.value.page}&per_page=10`
    if (searchQuery.value) url += `&search=${encodeURIComponent(searchQuery.value)}`
    const { data } = await api.get<PaginatedResponse<NewsItem>>(url)
    news.value = data.items
    pagination.value.total = data.total
    pagination.value.pages = data.pages
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const applyFilter = () => {
  pagination.value.page = 1
  fetchNews()
}

const openCreateModal = () => {
  isEditing.value = false
  formData.id = null
  formData.title = ''
  formData.excerpt = ''
  formData.content_html = ''
  formData.status = 'draft'
  formData.category_ids = []
  formData.cover_image_file = null
  formData.cover_image_url = null
  if (fileInput.value) fileInput.value.value = ''
  showModal.value = true
}

const openEditModal = (item: NewsItem) => {
  isEditing.value = true
  formData.id = item.id
  formData.title = item.title
  formData.excerpt = item.excerpt || ''
  formData.content_html = item.content_html || ''
  formData.status = item.status
  formData.category_ids = item.categories.map(c => c.id)
  formData.cover_image_file = null
  formData.cover_image_url = item.cover_image_url
  if (fileInput.value) fileInput.value.value = ''
  showModal.value = true
}

const confirmDelete = (id: number) => {
  itemToDelete.value = id
  showDeleteConfirm.value = true
}

const handleDelete = async () => {
  if (!itemToDelete.value) return
  try {
    await api.del(`/api/news/${itemToDelete.value}`)
    fetchNews()
  } catch (e) {
    console.error(e)
  } finally {
    showDeleteConfirm.value = false
    itemToDelete.value = null
  }
}

const handleFileChange = (e: Event) => {
  const target = e.target as HTMLInputElement
  if (target.files && target.files[0]) {
    formData.cover_image_file = target.files[0]
    // Simple preview could be added here
  }
}

const saveNews = async () => {
  saving.value = true
  try {
    let imageUrl = formData.cover_image_url
    
    // Upload image first if there's a new one
    if (formData.cover_image_file) {
      const form = new FormData()
      form.append('file', formData.cover_image_file)
      const { data } = await api.post('/api/uploads/image', form, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      imageUrl = data.url
    }

    const payload = {
      title: formData.title,
      excerpt: formData.excerpt,
      content_html: formData.content_html,
      status: formData.status,
      category_ids: formData.category_ids,
      cover_image_url: imageUrl
    }

    if (isEditing.value && formData.id) {
      await api.put(`/api/news/${formData.id}`, payload)
    } else {
      await api.post('/api/news', payload)
    }
    
    showModal.value = false
    fetchNews()
  } catch (e) {
    console.error('Error saving news', e)
    alert('Error al guardar la noticia')
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  fetchCategories()
  fetchNews()
})
</script>

<template>
  <div class="flex min-h-screen bg-gray-50">
    <AdminSidebar />
    <div class="flex-1 p-8 overflow-y-auto">
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-bold text-gray-900">Gestión de Noticias</h1>
        <button @click="openCreateModal" class="btn-primary">Nueva Noticia</button>
      </div>

      <div class="bg-white p-4 rounded-xl shadow-sm border border-gray-100 mb-6 flex gap-4">
        <div class="relative flex-1">
          <input v-model="searchQuery" @keyup.enter="applyFilter" type="text" placeholder="Buscar por título..." class="input-field pl-10">
          <svg class="w-5 h-5 text-gray-400 absolute left-3 top-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
        </div>
        <button @click="applyFilter" class="btn-secondary">Buscar</button>
      </div>

      <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Título</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Autor</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fecha</th>
                <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Acciones</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-if="loading">
                <td colspan="5" class="px-6 py-10 text-center text-gray-500">Cargando noticias...</td>
              </tr>
              <tr v-else-if="news.length === 0">
                <td colspan="5" class="px-6 py-10 text-center text-gray-500">No se encontraron noticias.</td>
              </tr>
              <tr v-else v-for="item in news" :key="item.id" class="hover:bg-gray-50">
                <td class="px-6 py-4">
                  <div class="text-sm font-medium text-gray-900 line-clamp-1" :title="item.title">{{ item.title }}</div>
                  <div class="text-xs text-gray-500">{{ item.categories.map(c => c.name).join(', ') }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span :class="{
                    'bg-green-100 text-green-800': item.status === 'published',
                    'bg-gray-100 text-gray-800': item.status === 'draft',
                    'bg-red-100 text-red-800': item.status === 'archived'
                  }" class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full">
                    {{ item.status === 'published' ? 'Publicado' : item.status === 'draft' ? 'Borrador' : 'Archivado' }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ item.author?.username }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ new Date(item.created_at!).toLocaleDateString() }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <button @click="openEditModal(item)" class="text-upec-green hover:text-upec-green-dark mr-3">Editar</button>
                  <button @click="confirmDelete(item.id)" class="text-red-600 hover:text-red-900">Eliminar</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <!-- Pagination -->
        <div v-if="pagination.pages > 1" class="bg-white px-4 py-3 border-t border-gray-200 flex items-center justify-between sm:px-6">
          <button @click="pagination.page--; fetchNews()" :disabled="pagination.page === 1" class="btn-outline px-3 py-1 text-sm">Anterior</button>
          <span class="text-sm text-gray-700">Página {{ pagination.page }} de {{ pagination.pages }}</span>
          <button @click="pagination.page++; fetchNews()" :disabled="pagination.page === pagination.pages" class="btn-outline px-3 py-1 text-sm">Siguiente</button>
        </div>
      </div>

      <!-- Form Modal -->
      <BaseModal :is-open="showModal" :title="isEditing ? 'Editar Noticia' : 'Nueva Noticia'" size="xl" @close="showModal = false">
        <form @submit.prevent="saveNews" class="space-y-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Título *</label>
            <input v-model="formData.title" type="text" required class="input-field">
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Estado</label>
              <select v-model="formData.status" class="input-field">
                <option value="draft">Borrador</option>
                <option value="published">Publicado</option>
                <option value="archived">Archivado</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Categorías</label>
              <select v-model="formData.category_ids" multiple class="input-field h-24">
                <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
              </select>
              <p class="text-xs text-gray-500 mt-1">Mantén presionado Ctrl (o Cmd) para seleccionar varias.</p>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Imagen de Portada</label>
            <input type="file" ref="fileInput" @change="handleFileChange" accept="image/*" class="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-upec-green-50 file:text-upec-green hover:file:bg-upec-green-100 cursor-pointer">
            <img v-if="formData.cover_image_url && !formData.cover_image_file" :src="formData.cover_image_url" class="mt-2 h-32 object-cover rounded" />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Extracto (Resumen)</label>
            <textarea v-model="formData.excerpt" rows="2" class="input-field" placeholder="Breve descripción para la tarjeta de noticia..."></textarea>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Contenido *</label>
            <NewsEditor v-model="formData.content_html" />
          </div>

          <div class="flex justify-end gap-3 pt-4 border-t border-gray-200">
            <button type="button" @click="showModal = false" class="btn-outline px-4 py-2">Cancelar</button>
            <button type="submit" :disabled="saving" class="btn-primary px-6 py-2 flex items-center">
              <span v-if="saving" class="animate-spin mr-2">⏳</span>
              {{ saving ? 'Guardando...' : 'Guardar' }}
            </button>
          </div>
        </form>
      </BaseModal>

      <ConfirmDialog 
        :is-open="showDeleteConfirm" 
        title="Eliminar Noticia" 
        message="¿Estás seguro de que deseas eliminar esta noticia? Esta acción no se puede deshacer."
        @confirm="handleDelete" 
        @cancel="showDeleteConfirm = false" 
      />
    </div>
  </div>
</template>
