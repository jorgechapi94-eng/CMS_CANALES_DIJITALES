import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import router from '@/router'

const api = axios.create({
  baseURL: ''
})

api.interceptors.request.use((config) => {
  const authStore = useAuthStore()
  if (authStore.accessToken) {
    config.headers.Authorization = `Bearer ${authStore.accessToken}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const authStore = useAuthStore()
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      try {
        await authStore.refreshAccessToken()
        if (authStore.accessToken) {
          originalRequest.headers.Authorization = `Bearer ${authStore.accessToken}`
          return api(originalRequest)
        }
      } catch (e) {
        authStore.logout()
        router.push('/login')
      }
    }
    return Promise.reject(error)
  }
)

export const useApi = () => {
  return {
    get: (url: string, config = {}) => api.get(url, config),
    post: (url: string, data = {}, config = {}) => api.post(url, data, config),
    put: (url: string, data = {}, config = {}) => api.put(url, data, config),
    del: (url: string, config = {}) => api.delete(url, config),
  }
}
