<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { useUiStore } from '@/stores/ui'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const uiStore = useUiStore()
const router = useRouter()

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <header class="bg-upec-green shadow-md sticky top-0 z-40">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex items-center">
          <router-link to="/" class="flex-shrink-0 flex items-center">
            <span class="text-upec-yellow font-bold text-2xl tracking-wider">UPEC</span>
          </router-link>
          <nav class="hidden md:ml-10 md:flex md:space-x-8">
            <router-link to="/" class="text-white hover:text-upec-yellow px-3 py-2 rounded-md font-medium">Inicio</router-link>
            <router-link to="/noticias" class="text-white hover:text-upec-yellow px-3 py-2 rounded-md font-medium">Noticias</router-link>
            <router-link to="/periodicos" class="text-white hover:text-upec-yellow px-3 py-2 rounded-md font-medium">Periódicos</router-link>
            <router-link to="/programas" class="text-white hover:text-upec-yellow px-3 py-2 rounded-md font-medium">Programas</router-link>
            <router-link to="/tv" class="text-white hover:text-upec-yellow px-3 py-2 rounded-md font-medium">TV</router-link>
            <router-link to="/radio" class="text-white hover:text-upec-yellow px-3 py-2 rounded-md font-medium">Radio</router-link>
          </nav>
        </div>
        
        <div class="hidden md:flex items-center space-x-4">
          <template v-if="authStore.isAuthenticated">
            <div class="text-white text-sm flex items-center gap-2">
              <span>{{ authStore.user?.username }}</span>
              <span class="badge-yellow">{{ authStore.userRoles[0] || 'User' }}</span>
            </div>
            <router-link to="/admin" class="text-white hover:text-upec-yellow font-medium">Panel Admin</router-link>
            <button @click="logout" class="text-sm bg-upec-green-dark text-white px-3 py-1.5 rounded hover:bg-red-600 transition-colors">Salir</button>
          </template>
          <template v-else>
            <router-link to="/login" class="text-white hover:text-upec-yellow font-medium">Iniciar Sesión</router-link>
          </template>
        </div>

        <div class="flex items-center md:hidden">
          <button @click="uiStore.toggleMobileMenu" class="text-white hover:text-upec-yellow focus:outline-none">
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path v-if="!uiStore.mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </div>
    
    <!-- Mobile Menu -->
    <div v-if="uiStore.mobileMenuOpen" class="md:hidden bg-upec-green-dark pb-4">
      <div class="px-2 pt-2 pb-3 space-y-1 sm:px-3">
        <router-link to="/" class="block text-white hover:text-upec-yellow px-3 py-2 rounded-md font-medium" @click="uiStore.closeMobileMenu">Inicio</router-link>
        <router-link to="/noticias" class="block text-white hover:text-upec-yellow px-3 py-2 rounded-md font-medium" @click="uiStore.closeMobileMenu">Noticias</router-link>
        <router-link to="/periodicos" class="block text-white hover:text-upec-yellow px-3 py-2 rounded-md font-medium" @click="uiStore.closeMobileMenu">Periódicos</router-link>
        <router-link to="/programas" class="block text-white hover:text-upec-yellow px-3 py-2 rounded-md font-medium" @click="uiStore.closeMobileMenu">Programas</router-link>
        <router-link to="/tv" class="block text-white hover:text-upec-yellow px-3 py-2 rounded-md font-medium" @click="uiStore.closeMobileMenu">TV</router-link>
        <router-link to="/radio" class="block text-white hover:text-upec-yellow px-3 py-2 rounded-md font-medium" @click="uiStore.closeMobileMenu">Radio</router-link>
        
        <div class="border-t border-upec-green pt-4 pb-2 mt-4">
          <template v-if="authStore.isAuthenticated">
            <div class="px-3 mb-2 flex items-center gap-2">
              <span class="text-white">{{ authStore.user?.username }}</span>
              <span class="badge-yellow">{{ authStore.userRoles[0] }}</span>
            </div>
            <router-link to="/admin" class="block text-white hover:text-upec-yellow px-3 py-2 rounded-md font-medium" @click="uiStore.closeMobileMenu">Panel Admin</router-link>
            <button @click="() => { logout(); uiStore.closeMobileMenu(); }" class="w-full text-left text-white hover:text-red-400 px-3 py-2 rounded-md font-medium">Salir</button>
          </template>
          <template v-else>
            <router-link to="/login" class="block text-white hover:text-upec-yellow px-3 py-2 rounded-md font-medium" @click="uiStore.closeMobileMenu">Iniciar Sesión</router-link>
          </template>
        </div>
      </div>
    </div>
  </header>
</template>
