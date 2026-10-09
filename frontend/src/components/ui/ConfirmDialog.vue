<script setup lang="ts">
import BaseModal from './BaseModal.vue'

withDefaults(defineProps<{
  isOpen: boolean
  title: string
  message: string
  confirmText?: string
  cancelText?: string
  variant?: 'danger' | 'warning' | 'primary'
}>(), {
  confirmText: 'Confirmar',
  cancelText: 'Cancelar',
  variant: 'danger'
})

const emit = defineEmits<{
  (e: 'confirm'): void
  (e: 'cancel'): void
}>()
</script>

<template>
  <BaseModal :is-open="isOpen" :title="title" size="sm" @close="emit('cancel')">
    <div class="mt-2">
      <p class="text-sm text-gray-500">{{ message }}</p>
    </div>
    
    <template #footer>
      <button 
        type="button" 
        :class="[
          'w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 text-base font-medium text-white focus:outline-none focus:ring-2 focus:ring-offset-2 sm:ml-3 sm:w-auto sm:text-sm',
          variant === 'danger' ? 'bg-red-600 hover:bg-red-700 focus:ring-red-500' : 
          variant === 'warning' ? 'bg-yellow-600 hover:bg-yellow-700 focus:ring-yellow-500' :
          'bg-upec-green hover:bg-upec-green-dark focus:ring-upec-green'
        ]"
        @click="emit('confirm')"
      >
        {{ confirmText }}
      </button>
      <button 
        type="button" 
        class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-upec-green sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
        @click="emit('cancel')"
      >
        {{ cancelText }}
      </button>
    </template>
  </BaseModal>
</template>
