import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User, LoginCredentials, AuthResponse } from '@/types'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const accessToken = ref<string | null>(null)
  const refreshToken = ref<string | null>(null)
  const isLoading = ref(false)

  const isAuthenticated = computed(() => !!accessToken.value)
  const userRoles = computed(() => user.value?.roles || [])
  const isSuperAdmin = computed(() => userRoles.value.includes('superadmin'))
  const isEditor = computed(() => userRoles.value.includes('editor'))
  const isGestorProgramas = computed(() => userRoles.value.includes('gestor_programas'))

  function hasRole(role: string): boolean {
    return userRoles.value.includes(role) || isSuperAdmin.value
  }

  async function login(credentials: LoginCredentials) {
    isLoading.value = true
    try {
      const { data } = await axios.post<AuthResponse>('/api/auth/login', credentials)
      setSession(data.access_token, data.refresh_token, data.user)
    } finally {
      isLoading.value = false
    }
  }

  function logout() {
    user.value = null
    accessToken.value = null
    refreshToken.value = null
    localStorage.removeItem('auth_access')
    localStorage.removeItem('auth_refresh')
    localStorage.removeItem('auth_user')
  }

  async function refreshAccessToken() {
    if (!refreshToken.value) throw new Error('No refresh token')
    try {
      const { data } = await axios.post<{access_token: string}>('/api/auth/refresh', {}, {
        headers: { Authorization: `Bearer ${refreshToken.value}` }
      })
      accessToken.value = data.access_token
      localStorage.setItem('auth_access', data.access_token)
    } catch (error) {
      logout()
      throw error
    }
  }

  function setSession(access: string, refresh: string, userData: User) {
    accessToken.value = access
    refreshToken.value = refresh
    user.value = userData
    localStorage.setItem('auth_access', access)
    localStorage.setItem('auth_refresh', refresh)
    localStorage.setItem('auth_user', JSON.stringify(userData))
  }

  function loadFromStorage() {
    const access = localStorage.getItem('auth_access')
    const refresh = localStorage.getItem('auth_refresh')
    const userStr = localStorage.getItem('auth_user')

    if (access && refresh && userStr) {
      accessToken.value = access
      refreshToken.value = refresh
      user.value = JSON.parse(userStr)
    }
  }

  return {
    user,
    accessToken,
    refreshToken,
    isLoading,
    isAuthenticated,
    userRoles,
    isSuperAdmin,
    isEditor,
    isGestorProgramas,
    hasRole,
    login,
    logout,
    refreshAccessToken,
    loadFromStorage
  }
})
