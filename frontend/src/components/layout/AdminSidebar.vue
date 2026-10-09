<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { useUiStore } from '@/stores/ui'
import { useRoute } from 'vue-router'

const authStore = useAuthStore()
const uiStore = useUiStore()
const route = useRoute()

const navItems = [
  { name: 'Dashboard', path: '/admin', icon: '📊', alwaysShow: true },
  { name: 'Noticias', path: '/admin/noticias', icon: '📰', roles: ['editor', 'superadmin'] },
  { name: 'Periódicos', path: '/admin/periodicos', icon: '🗞️', roles: ['editor', 'superadmin'] },
  { name: 'Programas', path: '/admin/programas', icon: '🎓', roles: ['gestor_programas', 'superadmin'] },
  { name: 'Usuarios', path: '/admin/usuarios', icon: '👥', roles: ['superadmin'] },
]

const visibleNavItems = navItems.filter(item => 
  item.alwaysShow || (item.roles && item.roles.some(r => authStore.hasRole(r)))
)
</script>

<template>
  <aside 
    :class="[ 
      'bg-upec-green-dark text-white flex flex-col transition-all duration-300',
      uiStore.sidebarOpen ? 'w-64' : 'w-20'
    ]"
  >
    <div class="p-4 flex items-center justify-between border-b border-upec-green">
      <span v-if="uiStore.sidebarOpen" class="font-bold text-lg text-upec-yellow">Admin Panel</span>
      <button @click="uiStore.toggleSidebar" class="p-2 rounded hover:bg-upec-green focus:outline-none">
        <span v-if="uiStore.sidebarOpen">◀</span>
        <span v-else>▶</span>
      </button>
    </div>
    
    <nav class="flex-1 py-4 space-y-1">
      <router-link
        v-for="item in visibleNavItems"
        :key="item.path"
        :to="item.path"
        :class="[ 
          'flex items-center px-4 py-3 mx-2 rounded-lg transition-colors duration-200',
          route.path === item.path ? 'bg-upec-green text-upec-yellow' : 'hover:bg-upec-green/50 text-gray-300 hover:text-white'
        ]"
      >
        <span class="text-xl">{{ item.icon }}</span>
        <span v-if="uiStore.sidebarOpen" class="ml-3 font-medium">{{ item.name }}</span>
      </router-link>
    </nav>
    
    <div class="p-4 border-t border-upec-green">
      <div v-if="uiStore.sidebarOpen" class="flex items-center">
        <div class="h-8 w-8 rounded-full bg-upec-yellow text-upec-green-dark flex items-center justify-center font-bold">
          {{ authStore.user?.username?.charAt(0).toUpperCase() }}
        </div>
        <div class="ml-3 overflow-hidden">
          <p class="text-sm font-medium truncate">{{ authStore.user?.username }}</p>
          <p class="text-xs text-upec-yellow truncate">{{ authStore.userRoles[0] }}</p>
        </div>
      </div>
      <div v-else class="flex justify-center">
        <div class="h-8 w-8 rounded-full bg-upec-yellow text-upec-green-dark flex items-center justify-center font-bold">
          {{ authStore.user?.username?.charAt(0).toUpperCase() }}
        </div>
      </div>
    </div>
  </aside>
</template>
