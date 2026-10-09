<script setup lang="ts">
import type { Program } from '@/types'

defineProps<{
  program: Program
}>()
</script>

<template>
  <div class="card p-6 border-l-4 border-upec-green hover:border-upec-yellow transition-colors flex flex-col h-full group">
    <div class="flex justify-between items-start mb-4">
      <h3 class="text-xl font-bold text-gray-900 group-hover:text-upec-green transition-colors line-clamp-2">
        {{ program.title }}
      </h3>
    </div>
    
    <div class="flex flex-wrap gap-2 mb-4">
      <span class="badge-green capitalize">{{ program.level }}</span>
      <span class="badge-yellow capitalize">{{ program.modality }}</span>
    </div>
    
    <p class="text-gray-600 text-sm line-clamp-3 mb-6 flex-grow">
      {{ program.description || 'Sin descripción disponible.' }}
    </p>
    
    <div class="grid grid-cols-3 gap-2 border-t border-gray-100 pt-4 mb-4">
      <div class="text-center">
        <p class="text-2xl font-bold text-upec-green">{{ program.teachers_count }}</p>
        <p class="text-xs text-gray-500 uppercase tracking-wider">Docentes</p>
      </div>
      <div class="text-center border-l border-r border-gray-100">
        <p class="text-2xl font-bold text-upec-green">{{ program.students_count }}</p>
        <p class="text-xs text-gray-500 uppercase tracking-wider">Estudiantes</p>
      </div>
      <div class="text-center">
        <p class="text-2xl font-bold text-upec-green">{{ program.projects_count }}</p>
        <p class="text-xs text-gray-500 uppercase tracking-wider">Proyectos</p>
      </div>
    </div>
    
    <router-link :to="`/programas/${program.id}`" class="btn-outline w-full text-center py-2 text-sm">
      Ver Detalles
    </router-link>
  </div>
</template>
