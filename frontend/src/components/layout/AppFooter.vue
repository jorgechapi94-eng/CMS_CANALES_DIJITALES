<script setup lang="ts">
const currentYear = new Date().getFullYear()
</script>

<template>
  <footer class="bg-upec-green-dark border-t-4 border-upec-yellow text-white">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div>
          <h2 class="text-2xl font-bold text-upec-yellow mb-4">UPEC</h2>
          <p class="text-gray-300">Universidad Politécnica Estatal del Carchi</p>
          <p class="text-gray-300 mt-2 text-sm">Formando profesionales de excelencia para el desarrollo de la sociedad.</p>
        </div>
        <div>
          <h3 class="text-lg font-semibold mb-4 border-b border-upec-green inline-block pb-1">Enlaces Rápidos</h3>
          <ul class="space-y-2">
            <li><router-link to="/noticias" class="text-gray-300 hover:text-upec-yellow transition-colors">Noticias</router-link></li>
            <li><router-link to="/programas" class="text-gray-300 hover:text-upec-yellow transition-colors">Oferta Académica</router-link></li>
            <li><router-link to="/periodicos" class="text-gray-300 hover:text-upec-yellow transition-colors">Periódicos Digitales</router-link></li>
          </ul>
        </div>
        <div>
          <h3 class="text-lg font-semibold mb-4 border-b border-upec-green inline-block pb-1">Medios Universitarios</h3>
          <ul class="space-y-2">
            <li><router-link to="/tv" class="text-gray-300 hover:text-upec-yellow transition-colors">UPEC TV</router-link></li>
            <li><router-link to="/radio" class="text-gray-300 hover:text-upec-yellow transition-colors">Radio Mindalae 102.3 FM</router-link></li>
          </ul>
        </div>
      </div>
      <div class="mt-8 pt-8 border-t border-upec-green text-center text-sm text-gray-400">
        <p>&copy; {{ currentYear }} Universidad Politécnica Estatal del Carchi. Todos los derechos reservados.</p>
      </div>
    </div>
  </footer>
</template>
