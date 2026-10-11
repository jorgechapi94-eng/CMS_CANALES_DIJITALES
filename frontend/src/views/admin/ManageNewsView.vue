<script setup lang="ts">
import { ref, onMounted, reactive, computed } from 'vue'
import AdminSidebar from '@/components/layout/AdminSidebar.vue'
import BaseModal from '@/components/ui/BaseModal.vue'
import ConfirmDialog from '@/components/ui/ConfirmDialog.vue'
import NewsEditor from '@/components/news/NewsEditor.vue'
import { useApi } from '@/composables/useApi'
import type { NewsItem, Category } from '@/types'

const api = useApi()

const news = ref<NewsItem[]>([])
const categories = ref<Category[]>([])
const loading = ref(true)
const searchQuery = ref('')
const statusFilter = ref('')
const pagination = ref({ page: 1, total: 0, pages: 1 })

const showModal = ref(false)
const showDeleteConfirm = ref(false)
const itemToDelete = ref<number | null>(null)
const isEditing = ref(false)
const saving = ref(false)
const toastMessage = ref('')
const toastType = ref<'success' | 'error'>('success')
const showToast = ref(false)
const imagePreview = ref<string | null>(null)
const imageError = ref('')

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
const ALLOWED_IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png']
const MAX_IMAGE_SIZE_MB = 5

const formValid = computed(() => {
  return formData.title.trim().length > 0 && formData.content_html.trim().length > 0
})

const toast = (msg: string, type: 'success' | 'error' = 'success') => {
  toastMessage.value = msg
  toastType.value = type
  showToast.value = true
  setTimeout(() => { showToast.value = false }, 4000)
}

const fetchCategories = async () => {
  try {
    const { data } = await api.get('/api/categories')
    categories.value = data
  } catch {
    // Categories might not exist yet
  }
}

const fetchNews = async () => {
  loading.value = true
  try {
    let url = `/api/news/admin?page=${pagination.value.page}&per_page=10`
    if (searchQuery.value) url += `&search=${encodeURIComponent(searchQuery.value)}`
    if (statusFilter.value) url += `&status=${statusFilter.value}`
    const { data } = await api.get(url)
    news.value = data.items
    pagination.value.total = data.total
    pagination.value.pages = data.pages
  } catch (e) {
    console.error(e)
    toast('Error al cargar noticias', 'error')
  } finally {
    loading.value = false
  }
}

const applyFilter = () => {
  pagination.value.page = 1
  fetchNews()
}

const resetFilters = () => {
  searchQuery.value = ''
  statusFilter.value = ''
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
  imagePreview.value = null
  imageError.value = ''
  if (fileInput.value) fileInput.value.value = ''
  showModal.value = true
}

const openEditModal = async (item: NewsItem) => {
  isEditing.value = true
  // Fetch full content if not already loaded
  try {
    const { data } = await api.get(`/api/news/${item.id}`)
    formData.id = data.id
    formData.title = data.title
    formData.excerpt = data.excerpt || ''
    formData.content_html = data.content_html || ''
    formData.status = data.status
    formData.category_ids = data.categories?.map((c: Category) => c.id) || []
    formData.cover_image_file = null
    formData.cover_image_url = data.cover_image_url
    imagePreview.value = data.cover_image_url || null
    imageError.value = ''
    if (fileInput.value) fileInput.value.value = ''
    showModal.value = true
  } catch (e) {
    toast('Error al cargar la noticia', 'error')
  }
}

const confirmDelete = (id: number) => {
  itemToDelete.value = id
  showDeleteConfirm.value = true
}

const handleDelete = async () => {
  if (!itemToDelete.value) return
  try {
    await api.del(`/api/news/${itemToDelete.value}`)
    toast('Noticia archivada correctamente')
    fetchNews()
  } catch (e) {
    console.error(e)
    toast('Error al archivar la noticia', 'error')
  } finally {
    showDeleteConfirm.value = false
    itemToDelete.value = null
  }
}

const validateImageFile = (file: File): boolean => {
  imageError.value = ''
  const ext = file.name.split('.').pop()?.toLowerCase() || ''
  if (!ALLOWED_IMAGE_EXTENSIONS.includes(ext)) {
    imageError.value = `Formato no permitido. Solo se aceptan: ${ALLOWED_IMAGE_EXTENSIONS.join(', ')}`
    return false
  }
  const sizeMB = file.size / (1024 * 1024)
  if (sizeMB > MAX_IMAGE_SIZE_MB) {
    imageError.value = `La imagen excede ${MAX_IMAGE_SIZE_MB}MB. Tamaño actual: ${sizeMB.toFixed(2)}MB`
    return false
  }
  return true
}

const handleFileChange = (e: Event) => {
  const target = e.target as HTMLInputElement
  if (target.files && target.files[0]) {
    const file = target.files[0]
    if (!validateImageFile(file)) {
      target.value = ''
      formData.cover_image_file = null
      imagePreview.value = formData.cover_image_url || null
      return
    }
    formData.cover_image_file = file
    // Generate preview
    const reader = new FileReader()
    reader.onload = (ev) => {
      imagePreview.value = ev.target?.result as string
    }
    reader.readAsDataURL(file)
  }
}

const handleDrop = (e: DragEvent) => {
  e.preventDefault()
  const file = e.dataTransfer?.files[0]
  if (file && file.type.startsWith('image/')) {
    if (!validateImageFile(file)) return
    formData.cover_image_file = file
    const reader = new FileReader()
    reader.onload = (ev) => {
      imagePreview.value = ev.target?.result as string
    }
    reader.readAsDataURL(file)
  }
}

const removeImage = () => {
  formData.cover_image_file = null
  formData.cover_image_url = null
  imagePreview.value = null
  imageError.value = ''
  if (fileInput.value) fileInput.value.value = ''
}

const saveNews = async () => {
  if (!formValid.value) return
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
      toast('Noticia actualizada correctamente')
    } else {
      await api.post('/api/news', payload)
      toast('Noticia creada correctamente')
    }

    showModal.value = false
    fetchNews()
  } catch (e: any) {
    const msg = e.response?.data?.error || 'Error al guardar la noticia'
    toast(msg, 'error')
  } finally {
    saving.value = false
  }
}

const getStatusLabel = (status: string) => {
  const labels: Record<string, string> = { published: 'Publicado', draft: 'Borrador', archived: 'Archivado' }
  return labels[status] || status
}

const getStatusClasses = (status: string) => {
  const classes: Record<string, string> = {
    published: 'bg-emerald-50 text-emerald-700 ring-emerald-600/20',
    draft: 'bg-amber-50 text-amber-700 ring-amber-600/20',
    archived: 'bg-red-50 text-red-700 ring-red-600/20'
  }
  return classes[status] || 'bg-gray-50 text-gray-700 ring-gray-600/20'
}

const formatDate = (dateStr: string | null) => {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleDateString('es-EC', { year: 'numeric', month: 'short', day: 'numeric' })
}

onMounted(() => {
  fetchCategories()
  fetchNews()
})
</script>

<template>
  <div class="flex min-h-screen bg-gray-50">
    <AdminSidebar />
    <div class="flex-1 overflow-y-auto">
      <!-- Header gradient -->
      <div class="bg-gradient-to-r from-upec-green-dark via-upec-green to-upec-green-light px-8 pt-8 pb-20">
        <div class="flex justify-between items-center">
          <div>
            <h1 class="text-3xl font-bold text-white tracking-tight">Gestión de Noticias</h1>
            <p class="text-green-100 mt-1">Crea, edita y publica noticias del portal institucional</p>
          </div>
          <button @click="openCreateModal" id="btn-create-news" class="inline-flex items-center gap-2 bg-white/15 backdrop-blur-sm text-white px-5 py-2.5 rounded-xl font-medium hover:bg-white/25 transition-all duration-200 border border-white/20 shadow-lg hover:shadow-xl hover:-translate-y-0.5">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
            Nueva Noticia
          </button>
        </div>
      </div>

      <div class="px-8 -mt-12">
        <!-- Filter card -->
        <div class="bg-white p-5 rounded-2xl shadow-lg border border-gray-100 mb-6 flex flex-wrap gap-4 items-end">
          <div class="flex-1 min-w-[200px]">
            <label class="block text-xs font-medium text-gray-500 uppercase tracking-wider mb-1.5">Buscar</label>
            <div class="relative">
              <svg class="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
              <input v-model="searchQuery" @keyup.enter="applyFilter" type="text" placeholder="Buscar por título..." id="input-search-news" class="input-field pl-10 !rounded-xl !border-gray-200 bg-gray-50 focus:bg-white">
            </div>
          </div>
          <div class="w-44">
            <label class="block text-xs font-medium text-gray-500 uppercase tracking-wider mb-1.5">Estado</label>
            <select v-model="statusFilter" @change="applyFilter" id="select-status-filter" class="input-field !rounded-xl !border-gray-200 bg-gray-50 focus:bg-white">
              <option value="">Todos</option>
              <option value="published">Publicados</option>
              <option value="draft">Borradores</option>
              <option value="archived">Archivados</option>
            </select>
          </div>
          <div class="flex gap-2">
            <button @click="applyFilter" class="btn-primary !rounded-xl !px-5 !py-2.5">
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
            </button>
            <button @click="resetFilters" class="btn-outline !rounded-xl !px-4 !py-2.5 !border-gray-200 !text-gray-500 hover:!text-gray-700 hover:!bg-gray-50 hover:!border-gray-300" title="Limpiar filtros">
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
            </button>
          </div>
        </div>

        <!-- Stats row -->
        <div class="flex items-center gap-2 mb-4 text-sm text-gray-500">
          <span class="font-medium">{{ pagination.total }}</span> noticias encontradas
          <span v-if="statusFilter" class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-upec-green-50 text-upec-green text-xs font-medium">
            {{ getStatusLabel(statusFilter) }}
            <button @click="statusFilter = ''; applyFilter()" class="hover:text-upec-green-dark">&times;</button>
          </span>
        </div>

        <!-- Table -->
        <div class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden">
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200" id="table-news-list">
              <thead>
                <tr class="bg-gradient-to-r from-gray-50 to-gray-50/50">
                  <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Noticia</th>
                  <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Estado</th>
                  <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Autor</th>
                  <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Fecha</th>
                  <th class="px-6 py-4 text-right text-xs font-semibold text-gray-500 uppercase tracking-wider">Acciones</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100">
                <tr v-if="loading">
                  <td colspan="5" class="px-6 py-16 text-center">
                    <div class="flex flex-col items-center gap-3">
                      <div class="w-8 h-8 border-3 border-upec-green border-t-transparent rounded-full animate-spin"></div>
                      <span class="text-gray-400 text-sm">Cargando noticias...</span>
                    </div>
                  </td>
                </tr>
                <tr v-else-if="news.length === 0">
                  <td colspan="5" class="px-6 py-16 text-center">
                    <div class="flex flex-col items-center gap-3">
                      <div class="w-16 h-16 bg-gray-100 rounded-2xl flex items-center justify-center text-3xl">📰</div>
                      <p class="text-gray-500 font-medium">No se encontraron noticias</p>
                      <p class="text-gray-400 text-sm">Crea la primera noticia con el botón de arriba</p>
                    </div>
                  </td>
                </tr>
                <tr v-else v-for="item in news" :key="item.id" class="hover:bg-upec-green-50/30 transition-colors duration-150 group">
                  <td class="px-6 py-4">
                    <div class="flex items-center gap-3">
                      <div v-if="item.cover_image_url" class="w-12 h-12 rounded-xl overflow-hidden flex-shrink-0 ring-1 ring-gray-200">
                        <img :src="item.cover_image_url" :alt="item.title" class="w-full h-full object-cover">
                      </div>
                      <div v-else class="w-12 h-12 rounded-xl bg-gradient-to-br from-upec-green-50 to-upec-green-100 flex items-center justify-center flex-shrink-0">
                        <span class="text-upec-green text-lg">📰</span>
                      </div>
                      <div class="min-w-0">
                        <p class="text-sm font-semibold text-gray-900 truncate max-w-xs" :title="item.title">{{ item.title }}</p>
                        <p class="text-xs text-gray-400 truncate max-w-xs">{{ item.excerpt || 'Sin extracto' }}</p>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span :class="getStatusClasses(item.status)" class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold ring-1 ring-inset">
                      {{ getStatusLabel(item.status) }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center gap-2">
                      <div class="w-7 h-7 rounded-full bg-upec-green-100 text-upec-green flex items-center justify-center text-xs font-bold">
                        {{ item.author?.username?.charAt(0).toUpperCase() }}
                      </div>
                      <span class="text-sm text-gray-600">{{ item.author?.username }}</span>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ formatDate(item.created_at) }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-right">
                    <div class="flex items-center justify-end gap-1 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                      <button @click="openEditModal(item)" :id="'btn-edit-news-' + item.id" class="inline-flex items-center gap-1 px-3 py-1.5 text-xs font-medium text-upec-green bg-upec-green-50 rounded-lg hover:bg-upec-green-100 transition-colors" title="Editar">
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
                        Editar
                      </button>
                      <button @click="confirmDelete(item.id)" :id="'btn-delete-news-' + item.id" class="inline-flex items-center gap-1 px-3 py-1.5 text-xs font-medium text-red-600 bg-red-50 rounded-lg hover:bg-red-100 transition-colors" title="Archivar">
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4"/></svg>
                        Archivar
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Pagination -->
          <div v-if="pagination.pages > 1" class="bg-gray-50/50 px-6 py-4 border-t border-gray-100 flex items-center justify-between">
            <p class="text-sm text-gray-500">Mostrando página <span class="font-semibold">{{ pagination.page }}</span> de <span class="font-semibold">{{ pagination.pages }}</span></p>
            <div class="flex gap-2">
              <button @click="pagination.page--; fetchNews()" :disabled="pagination.page === 1" class="inline-flex items-center gap-1 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-xl hover:bg-gray-50 disabled:opacity-40 disabled:cursor-not-allowed transition-colors">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
                Anterior
              </button>
              <button @click="pagination.page++; fetchNews()" :disabled="pagination.page === pagination.pages" class="inline-flex items-center gap-1 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-xl hover:bg-gray-50 disabled:opacity-40 disabled:cursor-not-allowed transition-colors">
                Siguiente
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Form Modal -->
      <BaseModal :is-open="showModal" :title="isEditing ? 'Editar Noticia' : 'Nueva Noticia'" size="xl" @close="showModal = false">
        <form @submit.prevent="saveNews" class="space-y-6" id="form-news-editor">
          <!-- Title -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-1.5">Título <span class="text-red-500">*</span></label>
            <input v-model="formData.title" type="text" required id="input-news-title" class="input-field !rounded-xl text-lg font-medium" placeholder="Ej: UPEC inaugura nuevo laboratorio de investigación">
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Status -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1.5">Estado de Publicación</label>
              <div class="grid grid-cols-3 gap-2">
                <button type="button" @click="formData.status = 'draft'" :class="formData.status === 'draft' ? 'bg-amber-50 border-amber-300 text-amber-700 ring-1 ring-amber-200' : 'bg-gray-50 border-gray-200 text-gray-500 hover:bg-gray-100'" class="px-3 py-2.5 rounded-xl border text-sm font-medium transition-all duration-200 text-center">
                  📝 Borrador
                </button>
                <button type="button" @click="formData.status = 'published'" :class="formData.status === 'published' ? 'bg-emerald-50 border-emerald-300 text-emerald-700 ring-1 ring-emerald-200' : 'bg-gray-50 border-gray-200 text-gray-500 hover:bg-gray-100'" class="px-3 py-2.5 rounded-xl border text-sm font-medium transition-all duration-200 text-center">
                  ✅ Publicar
                </button>
                <button type="button" @click="formData.status = 'archived'" :class="formData.status === 'archived' ? 'bg-red-50 border-red-300 text-red-700 ring-1 ring-red-200' : 'bg-gray-50 border-gray-200 text-gray-500 hover:bg-gray-100'" class="px-3 py-2.5 rounded-xl border text-sm font-medium transition-all duration-200 text-center">
                  📦 Archivar
                </button>
              </div>
            </div>
            <!-- Categories -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1.5">Categorías</label>
              <div class="flex flex-wrap gap-2">
                <button v-for="cat in categories" :key="cat.id" type="button" @click="formData.category_ids.includes(cat.id) ? formData.category_ids = formData.category_ids.filter(c => c !== cat.id) : formData.category_ids.push(cat.id)" :class="formData.category_ids.includes(cat.id) ? 'bg-upec-green text-white border-upec-green' : 'bg-gray-50 text-gray-600 border-gray-200 hover:border-upec-green-200 hover:bg-upec-green-50'" class="px-3 py-1.5 rounded-full border text-sm font-medium transition-all duration-200">
                  {{ cat.name }}
                </button>
                <p v-if="categories.length === 0" class="text-xs text-gray-400 italic py-1.5">No hay categorías disponibles</p>
              </div>
            </div>
          </div>

          <!-- Cover Image -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-1.5">Imagen de Portada</label>
            <div v-if="!imagePreview" @dragover.prevent @drop="handleDrop" class="relative border-2 border-dashed border-gray-300 rounded-2xl p-8 hover:border-upec-green hover:bg-upec-green-50/30 transition-all duration-300 cursor-pointer group" @click="fileInput?.click()">
              <div class="flex flex-col items-center gap-3 text-center">
                <div class="w-14 h-14 bg-gray-100 rounded-2xl flex items-center justify-center group-hover:bg-upec-green-100 transition-colors">
                  <svg class="w-7 h-7 text-gray-400 group-hover:text-upec-green transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
                </div>
                <div>
                  <p class="text-sm font-medium text-gray-600">Arrastra una imagen aquí o <span class="text-upec-green font-semibold">haz clic para seleccionar</span></p>
                  <p class="text-xs text-gray-400 mt-1">Solo formatos .jpg y .png — Máximo {{ MAX_IMAGE_SIZE_MB }}MB</p>
                </div>
              </div>
              <input type="file" ref="fileInput" @change="handleFileChange" accept=".jpg,.jpeg,.png" class="hidden" id="input-cover-image">
            </div>
            <!-- Image Preview -->
            <div v-else class="relative rounded-2xl overflow-hidden border border-gray-200 group">
              <img :src="imagePreview" class="w-full h-48 object-cover" alt="Preview de portada" />
              <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity duration-200 flex items-center justify-center gap-3">
                <button type="button" @click="fileInput?.click()" class="px-4 py-2 bg-white/90 text-gray-700 rounded-xl text-sm font-medium hover:bg-white transition-colors">Cambiar</button>
                <button type="button" @click="removeImage" class="px-4 py-2 bg-red-500/90 text-white rounded-xl text-sm font-medium hover:bg-red-600 transition-colors">Eliminar</button>
              </div>
              <input type="file" ref="fileInput" @change="handleFileChange" accept=".jpg,.jpeg,.png" class="hidden">
            </div>
            <p v-if="imageError" class="mt-2 text-sm text-red-600 flex items-center gap-1">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/></svg>
              {{ imageError }}
            </p>
          </div>

          <!-- Excerpt -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-1.5">Extracto (Resumen)</label>
            <textarea v-model="formData.excerpt" rows="2" id="input-news-excerpt" class="input-field !rounded-xl resize-none" placeholder="Breve descripción que aparecerá en la tarjeta de la noticia..."></textarea>
            <p class="text-xs text-gray-400 mt-1">{{ formData.excerpt.length }}/500 caracteres</p>
          </div>

          <!-- Rich Text Editor -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-1.5">Contenido <span class="text-red-500">*</span></label>
            <div class="rounded-2xl overflow-hidden border border-gray-200">
              <NewsEditor v-model="formData.content_html" />
            </div>
          </div>

          <!-- Action buttons -->
          <div class="flex justify-between items-center pt-4 border-t border-gray-100">
            <p class="text-xs text-gray-400" v-if="isEditing">ID: {{ formData.id }}</p>
            <span v-else></span>
            <div class="flex gap-3">
              <button type="button" @click="showModal = false" class="px-5 py-2.5 text-sm font-medium text-gray-600 bg-gray-100 rounded-xl hover:bg-gray-200 transition-colors">Cancelar</button>
              <button type="submit" :disabled="saving || !formValid" id="btn-save-news" class="px-6 py-2.5 text-sm font-medium text-white bg-upec-green rounded-xl hover:bg-upec-green-dark disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 flex items-center gap-2 shadow-lg shadow-upec-green/25">
                <svg v-if="saving" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
                {{ saving ? 'Guardando...' : (isEditing ? 'Actualizar Noticia' : 'Crear Noticia') }}
              </button>
            </div>
          </div>
        </form>
      </BaseModal>

      <ConfirmDialog
        :is-open="showDeleteConfirm"
        title="Archivar Noticia"
        message="¿Estás seguro de que deseas archivar esta noticia? Podrás restaurarla más tarde cambiando su estado."
        confirm-text="Sí, archivar"
        @confirm="handleDelete"
        @cancel="showDeleteConfirm = false"
      />

      <!-- Toast notification -->
      <Teleport to="body">
        <transition name="toast">
          <div v-if="showToast" class="fixed bottom-6 right-6 z-[9999] max-w-sm">
            <div :class="[
              'flex items-center gap-3 px-5 py-3.5 rounded-2xl shadow-2xl border backdrop-blur-sm',
              toastType === 'success' ? 'bg-emerald-50/95 border-emerald-200 text-emerald-800' : 'bg-red-50/95 border-red-200 text-red-800'
            ]">
              <div :class="[
                'w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0',
                toastType === 'success' ? 'bg-emerald-100' : 'bg-red-100'
              ]">
                <svg v-if="toastType === 'success'" class="w-5 h-5 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
                <svg v-else class="w-5 h-5 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
              </div>
              <p class="text-sm font-medium">{{ toastMessage }}</p>
              <button @click="showToast = false" class="text-gray-400 hover:text-gray-600 ml-2">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
              </button>
            </div>
          </div>
        </transition>
      </Teleport>
    </div>
  </div>
</template>

<style scoped>
.toast-enter-active {
  animation: toast-in 0.4s ease;
}
.toast-leave-active {
  animation: toast-out 0.3s ease;
}
@keyframes toast-in {
  from { opacity: 0; transform: translateY(20px) scale(0.95); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}
@keyframes toast-out {
  from { opacity: 1; transform: translateY(0) scale(1); }
  to { opacity: 0; transform: translateY(10px) scale(0.95); }
}
</style>
