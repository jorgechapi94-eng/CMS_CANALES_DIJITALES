import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/public/HomeView.vue')
    },
    {
      path: '/noticias',
      name: 'news-list',
      component: () => import('@/views/public/NewsListView.vue')
    },
    {
      path: '/noticias/:slug',
      name: 'news-detail',
      component: () => import('@/views/public/NewsDetailView.vue')
    },
    {
      path: '/periodicos',
      name: 'newspapers',
      component: () => import('@/views/public/NewspapersView.vue')
    },
    {
      path: '/programas',
      name: 'programs',
      component: () => import('@/views/public/ProgramsView.vue')
    },
    {
      path: '/programas/:id',
      name: 'program-detail',
      component: () => import('@/views/public/ProgramDetailView.vue')
    },
    {
      path: '/tv',
      name: 'tv',
      component: () => import('@/views/public/TVView.vue')
    },
    {
      path: '/radio',
      name: 'radio',
      component: () => import('@/views/public/RadioView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue')
    },
    {
      path: '/admin',
      component: () => import('@/views/admin/DashboardView.vue'), // Wrap with a shell in App or Sidebar logic
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          name: 'admin-dashboard',
          component: () => import('@/views/admin/DashboardView.vue')
        },
        {
          path: 'noticias',
          name: 'manage-news',
          component: () => import('@/views/admin/ManageNewsView.vue'),
          meta: { roles: ['editor', 'superadmin'] }
        },
        {
          path: 'periodicos',
          name: 'manage-newspapers',
          component: () => import('@/views/admin/ManageNewspapersView.vue'),
          meta: { roles: ['editor', 'superadmin'] }
        },
        {
          path: 'programas',
          name: 'manage-programs',
          component: () => import('@/views/admin/ManageProgramsView.vue'),
          meta: { roles: ['gestor_programas', 'superadmin'] }
        },
        {
          path: 'usuarios',
          name: 'manage-users',
          component: () => import('@/views/admin/ManageUsersView.vue'),
          meta: { roles: ['superadmin'] }
        }
      ]
    }
  ]
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
    return
  }

  if (to.meta.roles) {
    const hasRequiredRole = (to.meta.roles as string[]).some(role => authStore.hasRole(role))
    if (!hasRequiredRole) {
      next('/admin')
      return
    }
  }

  next()
})

export default router
