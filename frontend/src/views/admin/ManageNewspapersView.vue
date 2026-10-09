<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import AdminSidebar from '@/components/layout/AdminSidebar.vue'
import BaseModal from '@/components/ui/BaseModal.vue'
import ConfirmDialog from '@/components/ui/ConfirmDialog.vue'
import { useApi } from '@/composables/useApi'
import type { Newspaper, PaginatedResponse } from '@/types'

const api = useApi()

const newspapers = ref<Newspaper[]>([])
const loading = ref(true)
const pagination = ref({ page: 1, total: 0, pages: 1 })

const showModal = ref(false)
const showDeleteConfirm = ref(false)
const itemToDelete = ref<number | null>(null)
const saving = ref(false)
const uploadProgress = ref(0)

const formData = reactive({
  id: null as number | null,
  title: '',
  publication_date: '',
  pdf_file: null as File | null
})
const fileInput = ref<HTMLInputElement | null>(null)

const fetchNewspapers = async () => {
  loading.value = true
  try {
    const { data } = await api.get<PaginatedResponse<Newspaper>>(`/api/newspapers?page=${pagination.value.page}&per_page=10`)
    newspapers.value = data.items
    pagination.value.total = data.total
    pagination.value.pages = data.pages
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const openModal = () => {
  formData.id = null
  formData.title = ''
  formData.publication_date = new Date().toISOString().split('T')[0]
  formData.pdf_file = null
  if (fileInput.value) fileInput.value.value = ''
  uploadProgress.value = 0
  showModal.value = true
}

const handleFileChange = (e: Event) => {
  const target = e.target as HTMLInputElement
  if (target.files && target.files[0]) {
    formData.pdf_file = target.files[0]
  }
}

const saveNewspaper = async () => {
  if (!formData.pdf_file && !formData.id) {
    alert('Debe seleccionar un archivo PDF')
    return
  }
  
  saving.value = true
  uploadProgress.value = 10
  
  try {
    const form = new FormData()
    form.append('title', formData.title)
    if (formData.publication_date) form.append('publication_date', formData.publication_date)
    if (formData.pdf_file) form.append('file', formData.pdf_file)

    await api.post('/api/newspapers', form, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: (progressEvent) => {
        if (progressEvent.total) {
          uploadProgress.value = Math.round((progressEvent.loaded * 100) / progressEvent.total)
        }
      }
    })
    
    showModal.value = false
    fetchNewspapers()
  } catch (e) {
    console.error(e)
    alert('Error al subir el periódico')
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
    fetchNewspapers()
  } catch (e) {
    console.error(e)
  } finally {
    showDeleteConfirm.value = false
    itemToDelete.value = null
  }
}

onMounted(() => fetchNewspapers())
</script>

<template>
  <div class="flex min-h-screen bg-gray-50">
    <AdminSidebar />
    <div class="flex-1 p-8 overflow-y-auto">
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-bold text-gray-900">Periódicos Digitales</h1>
        <button @click="openModal" class="btn-primary">Subir Periódico</button>
      </div>

      <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Título</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Fecha Pub.</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tamaño</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Acciones</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-if="loading">
              <td colspan="4" class="px-6 py-10 text-center text-gray-500">Cargando...</td>
            </tr>
            <tr v-else-if="newspapers.length === 0">
              <td colspan="4" class="px-6 py-10 text-center text-gray-500">No hay periódicos.</td>
            </tr>
            <tr v-else v-for="item in newspapers" :key="item.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 font-medium text-sm text-gray-900">{{ item.title }}</td>
              <td class="px-6 py-4 text-sm text-gray-500">{{ item.publication_date }}</td>
              <td class="px-6 py-4 text-sm text-gray-500">{{ item.file_size_bytes ? (item.file_size_bytes / 1024 / 1024).toFixed(2) + ' MB' : 'N/A' }}</td>
              <td class="px-6 py-4 text-right text-sm font-medium">
                <a :href="item.pdf_url" target="_blank" class="text-blue-600 hover:text-blue-900 mr-3">Ver PDF</a>
                <button @click="confirmDelete(item.id)" class="text-red-600 hover:text-red-900">Eliminar</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Upload Modal -->
      <BaseModal :is-open="showModal" title="Subir Periódico PDF" size="md" @close="showModal = false">
        <form @submit.prevent="saveNewspaper" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Título *</label>
            <input v-model="formData.title" type="text" required class="input-field" placeholder="Ej: Edición Enero 2024">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Fecha de Publicación</label>
            <input v-model="formData.publication_date" type="date" class="input-field">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Archivo PDF *</label>
            <div class="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md hover:border-upec-green transition-colors bg-gray-50">
              <div class="space-y-1 text-center">
                <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48"><path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" /></svg>
                <div class="flex text-sm text-gray-600 justify-center">
                  <label for="file-upload" class="relative cursor-pointer bg-white rounded-md font-medium text-upec-green hover:text-upec-green-dark focus-within:outline-none">
                    <span>Seleccionar un archivo</span>
                    <input id="file-upload" ref="fileInput" name="file-upload" type="file" class="sr-only" accept="application/pdf" @change="handleFileChange">
                  </label>
                </div>
                <p class="text-xs text-gray-500">{{ formData.pdf_file ? formData.pdf_file.name : 'Solo archivos PDF' }}</p>
              </div>
            </div>
          </div>
          
          <div v-if="saving" class="w-full bg-gray-200 rounded-full h-2.5 mt-4">
            <div class="bg-upec-green h-2.5 rounded-full transition-all duration-300" :style="`width: ${uploadProgress}%`"></div>
            <p class="text-xs text-center mt-1">{{ uploadProgress }}%</p>
          </div>

          <div class="flex justify-end gap-3 pt-4 border-t border-gray-200 mt-6">
            <button type="button" @click="showModal = false" :disabled="saving" class="btn-outline px-4 py-2">Cancelar</button>
            <button type="submit" :disabled="saving || !formData.title || !formData.pdf_file" class="btn-primary px-6 py-2">
              {{ saving ? 'Subiendo...' : 'Subir y Guardar' }}
            </button>
          </div>
        </form>
      </BaseModal>

      <ConfirmDialog :is-open="showDeleteConfirm" title="Eliminar Periódico" message="¿Estás seguro de que deseas eliminar este periódico?" @confirm="handleDelete" @cancel="showDeleteConfirm = false" />
    </div>
  </div>
</template>
