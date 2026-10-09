<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import AdminSidebar from '@/components/layout/AdminSidebar.vue'
import BaseModal from '@/components/ui/BaseModal.vue'
import ConfirmDialog from '@/components/ui/ConfirmDialog.vue'
import { useApi } from '@/composables/useApi'
import type { Program, PaginatedResponse, ProgramTeacher, ProgramStudent, ProgramProject } from '@/types'

const api = useApi()
const programs = ref<Program[]>([])
const loading = ref(true)

const showModal = ref(false)
const showDeleteConfirm = ref(false)
const itemToDelete = ref<number | null>(null)
const isEditing = ref(false)
const saving = ref(false)

const formData = reactive({
  id: null as number | null,
  title: '',
  description: '',
  modality: 'presencial',
  level: 'grado',
  is_active: true,
  teachers: [] as ProgramTeacher[],
  students: [] as ProgramStudent[],
  projects: [] as ProgramProject[]
})

const fetchPrograms = async () => {
  loading.value = true
  try {
    const { data } = await api.get<PaginatedResponse<Program>>('/api/programs?per_page=50')
    programs.value = data.items
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const openModal = () => {
  isEditing.value = false
  Object.assign(formData, {
    id: null, title: '', description: '', modality: 'presencial', level: 'grado', is_active: true,
    teachers: [], students: [], projects: []
  })
  showModal.value = true
}

const openEditModal = async (item: Program) => {
  isEditing.value = true
  // Need to fetch full detail to get relations
  try {
    const { data } = await api.get(`/api/programs/${item.id}`)
    Object.assign(formData, {
      id: data.id, title: data.title, description: data.description || '', modality: data.modality, level: data.level, is_active: data.is_active,
      teachers: data.teachers || [], students: data.students || [], projects: data.projects || []
    })
    showModal.value = true
  } catch (e) {
    console.error(e)
  }
}

const saveProgram = async () => {
  saving.value = true
  try {
    const payload = { ...formData }
    if (isEditing.value && formData.id) {
      await api.put(`/api/programs/${formData.id}`, payload)
    } else {
      await api.post('/api/programs', payload)
    }
    showModal.value = false
    fetchPrograms()
  } catch (e) {
    console.error(e)
    alert('Error al guardar el programa')
  } finally {
    saving.value = false
  }
}

const confirmDelete = (id: number) => {
  itemToDelete.value = id
  showDeleteConfirm.value = true
}

const handleDelete = async () => {
  if (!itemToDelete.value) return
  try {
    await api.del(`/api/programs/${itemToDelete.value}`)
    fetchPrograms()
  } catch (e) {
    console.error(e)
  } finally {
    showDeleteConfirm.value = false
    itemToDelete.value = null
  }
}

// Sub-arrays management
const addTeacher = () => formData.teachers.push({ full_name: '', title_degree: '', email: '', photo_url: null })
const removeTeacher = (index: number) => formData.teachers.splice(index, 1)

const addStudent = () => formData.students.push({ full_name: '', enrollment_year: new Date().getFullYear().toString() })
const removeStudent = (index: number) => formData.students.splice(index, 1)

const addProject = () => formData.projects.push({ title: '', description: '', link_url: null })
const removeProject = (index: number) => formData.projects.splice(index, 1)

onMounted(() => fetchPrograms())
</script>

<template>
  <div class="flex min-h-screen bg-gray-50">
    <AdminSidebar />
    <div class="flex-1 p-8 overflow-y-auto">
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-bold text-gray-900">Gestión de Programas (Oferta Académica)</h1>
        <button @click="openModal" class="btn-primary">Nuevo Programa</button>
      </div>

      <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Título</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nivel</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Modalidad</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Acciones</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-if="loading"><td colspan="5" class="px-6 py-10 text-center">Cargando...</td></tr>
            <tr v-else-if="programs.length === 0"><td colspan="5" class="px-6 py-10 text-center">No hay programas.</td></tr>
            <tr v-else v-for="item in programs" :key="item.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 text-sm font-medium text-gray-900">{{ item.title }}</td>
              <td class="px-6 py-4 text-sm text-gray-500 capitalize">{{ item.level }}</td>
              <td class="px-6 py-4 text-sm text-gray-500 capitalize">{{ item.modality }}</td>
              <td class="px-6 py-4 text-sm">
                <span :class="item.is_active ? 'badge-green' : 'bg-red-100 text-red-800'" class="px-2 py-1 rounded-full text-xs font-medium">
                  {{ item.is_active ? 'Activo' : 'Inactivo' }}
                </span>
              </td>
              <td class="px-6 py-4 text-right text-sm font-medium">
                <button @click="openEditModal(item)" class="text-upec-green hover:underline mr-3">Editar</button>
                <button @click="confirmDelete(item.id)" class="text-red-600 hover:underline">Eliminar</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Form Modal -->
      <BaseModal :is-open="showModal" :title="isEditing ? 'Editar Programa' : 'Nuevo Programa'" size="xl" @close="showModal = false">
        <form @submit.prevent="saveProgram" class="space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-1">Título *</label>
              <input v-model="formData.title" type="text" required class="input-field">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Nivel</label>
              <select v-model="formData.level" class="input-field">
                <option value="grado">Grado</option><option value="maestria">Maestría</option>
                <option value="doctorado">Doctorado</option><option value="tecnico">Técnico</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Modalidad</label>
              <select v-model="formData.modality" class="input-field">
                <option value="presencial">Presencial</option><option value="virtual">Virtual</option><option value="hibrido">Híbrido</option>
              </select>
            </div>
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-1">Descripción</label>
              <textarea v-model="formData.description" rows="3" class="input-field"></textarea>
            </div>
            <div class="md:col-span-2">
              <label class="flex items-center">
                <input type="checkbox" v-model="formData.is_active" class="rounded border-gray-300 text-upec-green focus:ring-upec-green mr-2">
                <span class="text-sm font-medium text-gray-700">Programa Activo (visible al público)</span>
              </label>
            </div>
          </div>

          <!-- Tabs logic inside modal for simplicity, using distinct sections -->
          <div class="space-y-6 border-t pt-4">
            
            <!-- Teachers -->
            <div class="bg-gray-50 p-4 rounded-lg border border-gray-200">
              <div class="flex justify-between items-center mb-3">
                <h4 class="font-bold text-gray-700">Docentes</h4>
                <button type="button" @click="addTeacher" class="text-sm btn-outline py-1 px-3">Añadir Docente</button>
              </div>
              <div v-for="(teacher, index) in formData.teachers" :key="index" class="flex gap-2 items-start mb-2 bg-white p-2 border rounded">
                <div class="flex-1 space-y-2">
                  <input v-model="teacher.full_name" placeholder="Nombre completo" required class="input-field py-1 text-sm">
                  <input v-model="teacher.title_degree" placeholder="Título/Grado" required class="input-field py-1 text-sm">
                  <input v-model="teacher.email" type="email" placeholder="Correo" required class="input-field py-1 text-sm">
                </div>
                <button type="button" @click="removeTeacher(index)" class="text-red-500 hover:bg-red-50 p-2 rounded">❌</button>
              </div>
            </div>

            <!-- Students -->
            <div class="bg-gray-50 p-4 rounded-lg border border-gray-200">
              <div class="flex justify-between items-center mb-3">
                <h4 class="font-bold text-gray-700">Estudiantes Destacados</h4>
                <button type="button" @click="addStudent" class="text-sm btn-outline py-1 px-3">Añadir Estudiante</button>
              </div>
              <div v-for="(student, index) in formData.students" :key="index" class="flex gap-2 items-center mb-2">
                <input v-model="student.full_name" placeholder="Nombre completo" required class="input-field py-1 text-sm flex-1">
                <input v-model="student.enrollment_year" placeholder="Año (ej. 2021)" required class="input-field py-1 text-sm w-32">
                <button type="button" @click="removeStudent(index)" class="text-red-500 hover:bg-red-50 p-2 rounded">❌</button>
              </div>
            </div>

            <!-- Projects -->
            <div class="bg-gray-50 p-4 rounded-lg border border-gray-200">
              <div class="flex justify-between items-center mb-3">
                <h4 class="font-bold text-gray-700">Proyectos</h4>
                <button type="button" @click="addProject" class="text-sm btn-outline py-1 px-3">Añadir Proyecto</button>
              </div>
              <div v-for="(project, index) in formData.projects" :key="index" class="flex gap-2 items-start mb-2 bg-white p-2 border rounded">
                <div class="flex-1 space-y-2">
                  <input v-model="project.title" placeholder="Título del proyecto" required class="input-field py-1 text-sm">
                  <textarea v-model="project.description" placeholder="Descripción breve" required rows="2" class="input-field py-1 text-sm"></textarea>
                  <input v-model="project.link_url" placeholder="URL (opcional)" class="input-field py-1 text-sm">
                </div>
                <button type="button" @click="removeProject(index)" class="text-red-500 hover:bg-red-50 p-2 rounded">❌</button>
              </div>
            </div>

          </div>

          <div class="flex justify-end gap-3 pt-4">
            <button type="button" @click="showModal = false" class="btn-outline px-4 py-2">Cancelar</button>
            <button type="submit" :disabled="saving" class="btn-primary px-6 py-2">{{ saving ? 'Guardando...' : 'Guardar' }}</button>
          </div>
        </form>
      </BaseModal>

      <ConfirmDialog :is-open="showDeleteConfirm" title="Eliminar Programa" message="¿Eliminar este programa y todo su contenido relacionado?" @confirm="handleDelete" @cancel="showDeleteConfirm = false" />
    </div>
  </div>
</template>
