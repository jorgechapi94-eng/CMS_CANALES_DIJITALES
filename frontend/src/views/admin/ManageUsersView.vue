<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import AdminSidebar from '@/components/layout/AdminSidebar.vue'
import BaseModal from '@/components/ui/BaseModal.vue'
import ConfirmDialog from '@/components/ui/ConfirmDialog.vue'
import { useApi } from '@/composables/useApi'
import type { User, PaginatedResponse } from '@/types'

const api = useApi()

const users = ref<User[]>([])
const loading = ref(true)

const showModal = ref(false)
const showDeleteConfirm = ref(false)
const itemToDelete = ref<number | null>(null)
const isEditing = ref(false)
const saving = ref(false)

const formData = reactive({
  id: null as number | null,
  username: '',
  email: '',
  password: '',
  is_active: true,
  roles: [] as string[]
})

const availableRoles = [
  { value: 'editor', label: 'Editor (Noticias y Periódicos)' },
  { value: 'gestor_programas', label: 'Gestor de Programas' },
  { value: 'superadmin', label: 'Super Administrador' }
]

const fetchUsers = async () => {
  loading.value = true
  try {
    const { data } = await api.get<PaginatedResponse<User>>('/api/users?per_page=50')
    users.value = data.items
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const openModal = () => {
  isEditing.value = false
  Object.assign(formData, { id: null, username: '', email: '', password: '', is_active: true, roles: ['editor'] })
  showModal.value = true
}

const openEditModal = (item: User) => {
  isEditing.value = true
  Object.assign(formData, { id: item.id, username: item.username, email: item.email, password: '', is_active: item.is_active, roles: [...item.roles] })
  showModal.value = true
}

const saveUser = async () => {
  if (!formData.email.endsWith('@upec.edu.ec')) {
    alert('El correo debe pertenecer al dominio @upec.edu.ec')
    return
  }
  
  saving.value = true
  try {
    const payload: any = {
      username: formData.username,
      email: formData.email,
      roles: formData.roles,
      is_active: formData.is_active
    }
    if (formData.password) payload.password = formData.password

    if (isEditing.value && formData.id) {
      await api.put(`/api/users/${formData.id}`, payload)
    } else {
      await api.post('/api/users', payload)
    }
    showModal.value = false
    fetchUsers()
  } catch (e: any) {
    console.error(e)
    alert(e.response?.data?.message || 'Error al guardar el usuario')
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
    // In many systems, we just deactivate instead of delete
    await api.del(`/api/users/${itemToDelete.value}`)
    fetchUsers()
  } catch (e) {
    console.error(e)
  } finally {
    showDeleteConfirm.value = false
    itemToDelete.value = null
  }
}

onMounted(() => fetchUsers())
</script>

<template>
  <div class="flex min-h-screen bg-gray-50">
    <AdminSidebar />
    <div class="flex-1 p-8 overflow-y-auto">
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-bold text-gray-900">Gestión de Usuarios</h1>
        <button @click="openModal" class="btn-primary">Nuevo Usuario</button>
      </div>

      <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Usuario</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Roles</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Acciones</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-if="loading"><td colspan="5" class="px-6 py-10 text-center">Cargando...</td></tr>
            <tr v-else-if="users.length === 0"><td colspan="5" class="px-6 py-10 text-center">No hay usuarios.</td></tr>
            <tr v-else v-for="item in users" :key="item.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 text-sm font-medium text-gray-900">{{ item.username }}</td>
              <td class="px-6 py-4 text-sm text-gray-500">{{ item.email }}</td>
              <td class="px-6 py-4 text-sm">
                <div class="flex flex-wrap gap-1">
                  <span v-for="role in item.roles" :key="role" class="badge-yellow text-[10px] uppercase">{{ role }}</span>
                </div>
              </td>
              <td class="px-6 py-4 text-sm">
                <span :class="item.is_active ? 'badge-green' : 'bg-gray-100 text-gray-800'" class="px-2 py-1 rounded-full text-xs font-medium">
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

      <BaseModal :is-open="showModal" :title="isEditing ? 'Editar Usuario' : 'Nuevo Usuario'" size="md" @close="showModal = false">
        <form @submit.prevent="saveUser" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Nombre de Usuario *</label>
            <input v-model="formData.username" type="text" required class="input-field" placeholder="ej. jdoe">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Email * (@upec.edu.ec)</label>
            <input v-model="formData.email" type="email" required pattern=".*@upec\.edu\.ec$" class="input-field" placeholder="usuario@upec.edu.ec">
            <p class="text-xs text-gray-500 mt-1">Solo se permiten correos institucionales.</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Contraseña {{ isEditing ? '(Dejar en blanco para mantener actual)' : '*' }}</label>
            <input v-model="formData.password" type="password" :required="!isEditing" class="input-field" minlength="6">
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Roles Asignados</label>
            <div class="space-y-2">
              <label v-for="role in availableRoles" :key="role.value" class="flex items-center">
                <input type="checkbox" :value="role.value" v-model="formData.roles" class="rounded border-gray-300 text-upec-green focus:ring-upec-green mr-2">
                <span class="text-sm text-gray-700">{{ role.label }}</span>
              </label>
            </div>
            <p v-if="formData.roles.length === 0" class="text-xs text-red-500 mt-1">Debe seleccionar al menos un rol.</p>
          </div>

          <div>
            <label class="flex items-center mt-4">
              <input type="checkbox" v-model="formData.is_active" class="rounded border-gray-300 text-upec-green focus:ring-upec-green mr-2">
              <span class="text-sm font-medium text-gray-700">Usuario Activo (puede iniciar sesión)</span>
            </label>
          </div>

          <div class="flex justify-end gap-3 pt-4 mt-6 border-t border-gray-200">
            <button type="button" @click="showModal = false" class="btn-outline px-4 py-2">Cancelar</button>
            <button type="submit" :disabled="saving || formData.roles.length === 0" class="btn-primary px-6 py-2">
              {{ saving ? 'Guardando...' : 'Guardar' }}
            </button>
          </div>
        </form>
      </BaseModal>

      <ConfirmDialog :is-open="showDeleteConfirm" title="Desactivar Usuario" message="¿Estás seguro de que deseas eliminar (o desactivar) este usuario? Perderá el acceso al sistema." @confirm="handleDelete" @cancel="showDeleteConfirm = false" />
    </div>
  </div>
</template>
