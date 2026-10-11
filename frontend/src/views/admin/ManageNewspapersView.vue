<script setup lang="ts">
import { ref, onMounted, reactive, computed } from 'vue'
import AdminSidebar from '@/components/layout/AdminSidebar.vue'
import BaseModal from '@/components/ui/BaseModal.vue'
import ConfirmDialog from '@/components/ui/ConfirmDialog.vue'
import { useApi } from '@/composables/useApi'
import type { Newspaper } from '@/types'

const api = useApi()

const newspapers = ref<Newspaper[]>([])
const loading = ref(true)
const searchQuery = ref('')
const pagination = ref({ page: 1, total: 0, pages: 1 })

const showModal = ref(false)
const showDeleteConfirm = ref(false)
const showPreviewModal = ref(false)
const itemToDelete = ref<number | null>(null)
const previewItem = ref<Newspaper | null>(null)
const saving = ref(false)
const uploadProgress = ref(0)
const isEditing = ref(false)

const toastMessage = ref('')
const toastType = ref<'success' | 'error'>('success')
const showToast = ref(false)

const pdfError = ref('')
const coverError = ref('')
const isDragging = ref(false)

const formData = reactive({
  id: null as number | null,
  title: '',
  publication_date: new Date().toISOString().split('T')[0],
  pdf_file: null as File | null,
  cover_file: null as File | null
})

const pdfInput = ref<HTMLInputElement | null>(null)
const coverInput = ref<HTMLInputElement | null>(null)
const coverPreview = ref<string | null>(null)

const MAX_PDF_SIZE_MB = 20
const ALLOWED_COVER_EXTENSIONS = ['jpg', 'jpeg', 'png']

const formValid = computed(() => {
  if (isEditing.value) {
    return formData.title.trim().length > 0
  }
  return formData.title.trim().length > 0 && formData.pdf_file !== null
})

const toast = (msg: string, type: 'success' | 'error' = 'success') => {
  toastMessage.value = msg
  toastType.value = type
  showToast.value = true
  setTimeout(() => { showToast.value = false }, 4000)
}

const fetchNewspapers = async () => {
  loading.value = true
  try {
    let url = `/api/newspapers?page=${pagination.value.page}&per_page=10`
    if (searchQuery.value) url += `&search=${encodeURIComponent(searchQuery.value)}`
    const { data } = await api.get(url)
    newspapers.value = data.items
    pagination.value.total = data.total
    pagination.value.pages = data.pages
  } catch (e) {
    console.error(e)
    toast('Error al cargar los periódicos', 'error')
  } finally {
    loading.value = false
  }
}

const applyFilter = () => {
  pagination.value.page = 1
  fetchNewspapers()
}

const openCreateModal = () => {
  isEditing.value = false
  formData.id = null
  formData.title = ''
  formData.publication_date = new Date().toISOString().split('T')[0]
  formData.pdf_file = null
  formData.cover_file = null
  coverPreview.value = null
  pdfError.value = ''
  coverError.value = ''
  uploadProgress.value = 0
  if (pdfInput.value) pdfInput.value.value = ''
  if (coverInput.value) coverInput.value.value = ''
  showModal.value = true
}

const openEditModal = (item: Newspaper) => {
  isEditing.value = true
  formData.id = item.id
  formData.title = item.title
  formData.publication_date = item.publication_date || ''
  formData.pdf_file = null
  formData.cover_file = null
  coverPreview.value = item.cover_thumbnail_url || null
  pdfError.value = ''
  coverError.value = ''
  uploadProgress.value = 0
  if (pdfInput.value) pdfInput.value.value = ''
  if (coverInput.value) coverInput.value.value = ''
  showModal.value = true
}

const openPreview = (item: Newspaper) => {
  previewItem.value = item
  showPreviewModal.value = true
}

const validatePdf = (file: File): boolean => {
  pdfError.value = ''
  const ext = file.name.split('.').pop()?.toLowerCase() || ''
  if (ext !== 'pdf') {
    pdfError.value = 'Solo se permiten archivos con extensión .pdf'
    return false
  }
  const sizeMB = file.size / (1024 * 1024)
  if (sizeMB > MAX_PDF_SIZE_MB) {
    pdfError.value = `El archivo excede el peso máximo de ${MAX_PDF_SIZE_MB}MB. Tamaño actual: ${sizeMB.toFixed(2)}MB`
    return false
  }
  return true
}

const validateCover = (file: File): boolean => {
  coverError.value = ''
  const ext = file.name.split('.').pop()?.toLowerCase() || ''
  if (!ALLOWED_COVER_EXTENSIONS.includes(ext)) {
    coverError.value = `Solo se aceptan formatos: ${ALLOWED_COVER_EXTENSIONS.join(', ')}`
    return false
  }
  return true
}

const handlePdfChange = (e: Event) => {
  const target = e.target as HTMLInputElement
  if (target.files && target.files[0]) {
    const file = target.files[0]
    if (!validatePdf(file)) {
      target.value = ''
      formData.pdf_file = null
      return
    }
    formData.pdf_file = file
  }
}

const handlePdfDrop = (e: DragEvent) => {
  e.preventDefault()
  isDragging.value = false
  const file = e.dataTransfer?.files[0]
  if (file) {
    if (!validatePdf(file)) return
    formData.pdf_file = file
  }
}

const handleCoverChange = (e: Event) => {
  const target = e.target as HTMLInputElement
  if (target.files && target.files[0]) {
    const file = target.files[0]
    if (!validateCover(file)) {
      target.value = ''
      formData.cover_file = null
      return
    }
    formData.cover_file = file
    const reader = new FileReader()
    reader.onload = (ev) => { coverPreview.value = ev.target?.result as string }
    reader.readAsDataURL(file)
  }
}

const removePdf = () => {
  formData.pdf_file = null
  pdfError.value = ''
  if (pdfInput.value) pdfInput.value.value = ''
}

const removeCover = () => {
  formData.cover_file = null
  coverPreview.value = null
  coverError.value = ''
  if (coverInput.value) coverInput.value.value = ''
}

const saveNewspaper = async () => {
  if (!formValid.value) return
  saving.value = true
  uploadProgress.value = 5

  try {
    const form = new FormData()
    form.append('title', formData.title)
    if (formData.publication_date) form.append('publication_date', formData.publication_date)
    if (formData.pdf_file) form.append('file', formData.pdf_file)
    if (formData.cover_file) form.append('cover', formData.cover_file)

    const config = {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: (progressEvent: any) => {
        if (progressEvent.total) {
          uploadProgress.value = Math.round((progressEvent.loaded * 100) / progressEvent.total)
        }
      }
    }

    if (isEditing.value && formData.id) {
      await api.put(`/api/newspapers/${formData.id}`, form, config)
      toast('Periódico actualizado correctamente')
    } else {
      await api.post('/api/newspapers', form, config)
      toast('Periódico subido correctamente')
    }

    showModal.value = false
    fetchNewspapers()
  } catch (e: any) {
    const msg = e.response?.data?.error || 'Error al guardar el periódico'
    toast(msg, 'error')
  } finally {
    saving.value = false
    uploadProgress.value = 0
  }
}

const confirmDelete = (id: number) => {
  itemToDelete.value = id
  showDeleteConfirm.value = true
}

const handleDelete = async () => {
  if (!itemToDelete.value) return
  try {
    await api.del(`/api/newspapers/${itemToDelete.value}`)
    toast('Periódico eliminado correctamente')
    fetchNewspapers()
  } catch (e) {
    console.error(e)
    toast('Error al eliminar el periódico', 'error')
  } finally {
    showDeleteConfirm.value = false
    itemToDelete.value = null
  }
}

const formatFileSize = (bytes: number | null) => {
  if (!bytes) return 'N/A'
  const mb = bytes / (1024 * 1024)
  return mb >= 1 ? `${mb.toFixed(2)} MB` : `${(bytes / 1024).toFixed(0)} KB`
}

const formatDate = (dateStr: string | null) => {
  if (!dateStr) return '—'
  return new Date(dateStr + 'T00:00:00').toLocaleDateString('es-EC', { year: 'numeric', month: 'long', day: 'numeric' })
}

onMounted(() => fetchNewspapers())
</script>

<template>
  <div class="flex min-h-screen bg-gray-50">
    <AdminSidebar />
    <div class="flex-1 overflow-y-auto">
      <!-- Header gradient -->
      <div class="bg-gradient-to-r from-upec-yellow-dark via-upec-yellow to-upec-yellow-light px-8 pt-8 pb-20">
        <div class="flex justify-between items-center">
          <div>
            <h1 class="text-3xl font-bold text-upec-green-dark tracking-tight">Periódicos Digitales</h1>
            <p class="text-upec-green-dark/70 mt-1">Sube y gestiona documentos digitalizados en formato PDF</p>
          </div>
          <button @click="openCreateModal" id="btn-upload-newspaper" class="inline-flex items-center gap-2 bg-upec-green-dark/15 backdrop-blur-sm text-upec-green-dark px-5 py-2.5 rounded-xl font-medium hover:bg-upec-green-dark/25 transition-all duration-200 border border-upec-green-dark/20 shadow-lg hover:shadow-xl hover:-translate-y-0.5">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"/></svg>
            Subir Periódico
          </button>
        </div>
      </div>

      <div class="px-8 -mt-12">
        <!-- Search bar -->
        <div class="bg-white p-5 rounded-2xl shadow-lg border border-gray-100 mb-6 flex gap-4 items-end">
          <div class="flex-1">
            <label class="block text-xs font-medium text-gray-500 uppercase tracking-wider mb-1.5">Buscar periódico</label>
            <div class="relative">
              <svg class="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
              <input v-model="searchQuery" @keyup.enter="applyFilter" type="text" placeholder="Buscar por título..." id="input-search-newspapers" class="input-field pl-10 !rounded-xl !border-gray-200 bg-gray-50 focus:bg-white">
            </div>
          </div>
          <button @click="applyFilter" class="btn-secondary !rounded-xl !px-5 !py-2.5">Buscar</button>
        </div>

        <!-- Stats -->
        <div class="flex items-center gap-4 mb-4">
          <span class="text-sm text-gray-500"><span class="font-semibold">{{ pagination.total }}</span> periódicos en total</span>
          <div class="flex items-center gap-2 text-xs text-gray-400">
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            Solo archivos PDF — Máximo {{ MAX_PDF_SIZE_MB }}MB
          </div>
        </div>

        <!-- Cards Grid -->
        <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div v-for="i in 6" :key="i" class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden animate-pulse">
            <div class="h-40 bg-gray-100"></div>
            <div class="p-5 space-y-3">
              <div class="h-4 bg-gray-100 rounded w-3/4"></div>
              <div class="h-3 bg-gray-100 rounded w-1/2"></div>
            </div>
          </div>
        </div>

        <div v-else-if="newspapers.length === 0" class="bg-white rounded-2xl shadow-lg border border-gray-100 p-16 text-center">
          <div class="flex flex-col items-center gap-4">
            <div class="w-20 h-20 bg-upec-yellow-50 rounded-3xl flex items-center justify-center text-4xl">🗞️</div>
            <div>
              <p class="text-lg font-semibold text-gray-700">No hay periódicos todavía</p>
              <p class="text-gray-400 mt-1">Sube el primer periódico digitalizado con el botón de arriba</p>
            </div>
            <button @click="openCreateModal" class="btn-secondary mt-2 !rounded-xl">
              <svg class="w-4 h-4 inline mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
              Subir primer periódico
            </button>
          </div>
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6" id="grid-newspapers">
          <div v-for="item in newspapers" :key="item.id" class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-lg hover:-translate-y-1 transition-all duration-300 group">
            <!-- Card cover -->
            <div class="relative h-44 bg-gradient-to-br from-red-50 via-orange-50 to-amber-50 flex items-center justify-center overflow-hidden">
              <img v-if="item.cover_thumbnail_url" :src="item.cover_thumbnail_url" :alt="item.title" class="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
              <div v-else class="flex flex-col items-center gap-2 text-gray-300">
                <svg class="w-16 h-16" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
                <span class="text-xs font-medium">PDF</span>
              </div>
              <!-- Overlay actions -->
              <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-end justify-center pb-4 gap-2">
                <a :href="item.pdf_url" target="_blank" class="px-4 py-2 bg-white/95 text-gray-700 rounded-xl text-xs font-semibold hover:bg-white transition-colors shadow-lg flex items-center gap-1">
                  <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
                  Ver PDF
                </a>
                <button @click="openEditModal(item)" class="px-4 py-2 bg-upec-green/95 text-white rounded-xl text-xs font-semibold hover:bg-upec-green transition-colors shadow-lg flex items-center gap-1">
                  <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
                  Editar
                </button>
              </div>
              <!-- File size badge -->
              <div class="absolute top-3 right-3 px-2.5 py-1 bg-black/50 backdrop-blur-sm text-white rounded-lg text-xs font-medium">
                {{ formatFileSize(item.file_size_bytes) }}
              </div>
            </div>
            <!-- Card body -->
            <div class="p-5">
              <h3 class="font-semibold text-gray-900 text-sm line-clamp-2 mb-2" :title="item.title">{{ item.title }}</h3>
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-1.5 text-xs text-gray-400">
                  <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
                  {{ formatDate(item.publication_date) }}
                </div>
                <button @click="confirmDelete(item.id)" :id="'btn-delete-newspaper-' + item.id" class="p-1.5 text-gray-300 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors opacity-0 group-hover:opacity-100" title="Eliminar">
                  <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
                </button>
              </div>
              <div v-if="item.uploaded_by" class="mt-3 pt-3 border-t border-gray-100 flex items-center gap-2">
                <div class="w-6 h-6 rounded-full bg-upec-yellow-100 text-upec-yellow-dark flex items-center justify-center text-xs font-bold">
                  {{ item.uploaded_by?.username?.charAt(0).toUpperCase() }}
                </div>
                <span class="text-xs text-gray-400">{{ item.uploaded_by?.username }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="pagination.pages > 1" class="mt-6 flex items-center justify-between">
          <p class="text-sm text-gray-500">Página <span class="font-semibold">{{ pagination.page }}</span> de <span class="font-semibold">{{ pagination.pages }}</span></p>
          <div class="flex gap-2">
            <button @click="pagination.page--; fetchNewspapers()" :disabled="pagination.page === 1" class="inline-flex items-center gap-1 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-xl hover:bg-gray-50 disabled:opacity-40 disabled:cursor-not-allowed transition-colors">
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
              Anterior
            </button>
            <button @click="pagination.page++; fetchNewspapers()" :disabled="pagination.page === pagination.pages" class="inline-flex items-center gap-1 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-xl hover:bg-gray-50 disabled:opacity-40 disabled:cursor-not-allowed transition-colors">
              Siguiente
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
            </button>
          </div>
        </div>

        <div class="h-8"></div>
      </div>

      <!-- Upload / Edit Modal -->
      <BaseModal :is-open="showModal" :title="isEditing ? 'Editar Periódico' : 'Subir Nuevo Periódico'" size="lg" @close="showModal = false">
        <form @submit.prevent="saveNewspaper" class="space-y-6" id="form-newspaper-upload">
          <!-- Title -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-1.5">Título del Periódico <span class="text-red-500">*</span></label>
            <input v-model="formData.title" type="text" required id="input-newspaper-title" class="input-field !rounded-xl" placeholder="Ej: Periódico Institucional — Edición Enero 2024">
          </div>

          <!-- Date -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-1.5">Fecha de Publicación</label>
            <input v-model="formData.publication_date" type="date" id="input-newspaper-date" class="input-field !rounded-xl !w-auto">
          </div>

          <!-- PDF Upload -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-1.5">
              Archivo PDF
              <span v-if="!isEditing" class="text-red-500">*</span>
              <span v-else class="text-xs text-gray-400 font-normal ml-1">(opcional al editar)</span>
            </label>

            <div v-if="!formData.pdf_file" @dragover.prevent="isDragging = true" @dragleave="isDragging = false" @drop="handlePdfDrop" :class="[
              'relative border-2 border-dashed rounded-2xl p-10 transition-all duration-300 cursor-pointer',
              isDragging ? 'border-upec-green bg-upec-green-50/50 scale-[1.02]' : 'border-gray-300 hover:border-upec-yellow hover:bg-upec-yellow-50/30'
            ]" @click="pdfInput?.click()">
              <div class="flex flex-col items-center gap-4 text-center">
                <div :class="['w-16 h-16 rounded-2xl flex items-center justify-center transition-colors', isDragging ? 'bg-upec-green-100' : 'bg-red-50']">
                  <svg :class="['w-8 h-8 transition-colors', isDragging ? 'text-upec-green' : 'text-red-400']" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"/>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 11v6m0 0l-2-2m2 2l2-2"/>
                  </svg>
                </div>
                <div>
                  <p class="text-sm font-medium text-gray-600">
                    <span v-if="isDragging" class="text-upec-green">Suelta el archivo aquí</span>
                    <span v-else>Arrastra tu archivo PDF aquí o <span class="text-upec-green font-semibold">haz clic para seleccionar</span></span>
                  </p>
                  <p class="text-xs text-gray-400 mt-1.5">
                    <span class="inline-flex items-center gap-1 px-2 py-0.5 bg-red-50 text-red-500 rounded-full font-medium">PDF</span>
                    Extensión .pdf — Peso máximo {{ MAX_PDF_SIZE_MB }}MB
                  </p>
                </div>
              </div>
              <input type="file" ref="pdfInput" @change="handlePdfChange" accept=".pdf" class="hidden" id="input-pdf-file">
            </div>

            <!-- PDF file selected -->
            <div v-else class="flex items-center gap-4 p-4 bg-emerald-50 border border-emerald-200 rounded-2xl">
              <div class="w-12 h-12 bg-red-100 rounded-xl flex items-center justify-center flex-shrink-0">
                <svg class="w-6 h-6 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
              </div>
              <div class="flex-1 min-w-0">
                <p class="text-sm font-semibold text-gray-900 truncate">{{ formData.pdf_file.name }}</p>
                <p class="text-xs text-gray-500">{{ (formData.pdf_file.size / (1024 * 1024)).toFixed(2) }} MB</p>
              </div>
              <button type="button" @click="removePdf" class="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-xl transition-colors" title="Quitar archivo">
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
              </button>
            </div>

            <p v-if="pdfError" class="mt-2 text-sm text-red-600 flex items-center gap-1">
              <svg class="w-4 h-4 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/></svg>
              {{ pdfError }}
            </p>
          </div>

          <!-- Optional Cover -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-1.5">Portada del periódico <span class="text-xs text-gray-400 font-normal">(opcional)</span></label>
            <div v-if="!coverPreview" class="border-2 border-dashed border-gray-200 rounded-2xl p-5 hover:border-upec-yellow hover:bg-upec-yellow-50/20 transition-all duration-300 cursor-pointer text-center" @click="coverInput?.click()">
              <svg class="w-8 h-8 text-gray-300 mx-auto mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
              <p class="text-xs text-gray-400">Solo .jpg y .png</p>
              <input type="file" ref="coverInput" @change="handleCoverChange" accept=".jpg,.jpeg,.png" class="hidden" id="input-cover-file">
            </div>
            <div v-else class="relative rounded-2xl overflow-hidden border border-gray-200 group">
              <img :src="coverPreview" class="w-full h-32 object-cover" alt="Cover preview" />
              <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                <button type="button" @click="removeCover" class="px-4 py-2 bg-red-500/90 text-white rounded-xl text-sm font-medium hover:bg-red-600">Eliminar</button>
              </div>
              <input type="file" ref="coverInput" @change="handleCoverChange" accept=".jpg,.jpeg,.png" class="hidden">
            </div>
            <p v-if="coverError" class="mt-2 text-sm text-red-600 flex items-center gap-1">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/></svg>
              {{ coverError }}
            </p>
          </div>

          <!-- Upload progress -->
          <div v-if="saving" class="space-y-2">
            <div class="flex justify-between text-xs text-gray-500">
              <span>Subiendo archivo...</span>
              <span class="font-semibold">{{ uploadProgress }}%</span>
            </div>
            <div class="w-full bg-gray-100 rounded-full h-2.5 overflow-hidden">
              <div class="h-full rounded-full bg-gradient-to-r from-upec-green to-upec-green-light transition-all duration-300 ease-out" :style="`width: ${uploadProgress}%`"></div>
            </div>
          </div>

          <!-- Actions -->
          <div class="flex justify-end gap-3 pt-4 border-t border-gray-100">
            <button type="button" @click="showModal = false" :disabled="saving" class="px-5 py-2.5 text-sm font-medium text-gray-600 bg-gray-100 rounded-xl hover:bg-gray-200 transition-colors disabled:opacity-50">Cancelar</button>
            <button type="submit" :disabled="saving || !formValid" id="btn-save-newspaper" class="px-6 py-2.5 text-sm font-medium text-white bg-upec-green rounded-xl hover:bg-upec-green-dark disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 flex items-center gap-2 shadow-lg shadow-upec-green/25">
              <svg v-if="saving" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
              {{ saving ? 'Subiendo...' : (isEditing ? 'Actualizar' : 'Subir y Guardar') }}
            </button>
          </div>
        </form>
      </BaseModal>

      <ConfirmDialog
        :is-open="showDeleteConfirm"
        title="Eliminar Periódico"
        message="¿Estás seguro de que deseas eliminar este periódico? Esta acción no se puede deshacer y el archivo será eliminado permanentemente."
        confirm-text="Sí, eliminar"
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
