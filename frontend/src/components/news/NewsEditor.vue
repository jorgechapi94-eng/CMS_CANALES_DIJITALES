<script setup lang="ts">
import { useEditor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import Image from '@tiptap/extension-image'
import Link from '@tiptap/extension-link'
import Youtube from '@tiptap/extension-youtube'
import Table from '@tiptap/extension-table'
import TableRow from '@tiptap/extension-table-row'
import TableCell from '@tiptap/extension-table-cell'
import TableHeader from '@tiptap/extension-table-header'
import { watch, onBeforeUnmount } from 'vue'
import DOMPurify from 'dompurify'
import { useApi } from '@/composables/useApi'

const props = defineProps<{
  modelValue: string
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
}>()

const api = useApi()

const editor = useEditor({
  content: props.modelValue,
  extensions: [
    StarterKit,
    Image.configure({ inline: true }),
    Link.configure({ openOnClick: false }),
    Youtube,
    Table.configure({ resizable: true }),
    TableRow,
    TableHeader,
    TableCell
  ],
  onUpdate: ({ editor }) => {
    const rawHtml = editor.getHTML()
    const cleanHtml = DOMPurify.sanitize(rawHtml, { ADD_TAGS: ['iframe'], ADD_ATTR: ['allow', 'allowfullscreen', 'frameborder', 'scrolling'] })
    emit('update:modelValue', cleanHtml)
  },
  editorProps: {
    attributes: {
      class: 'prose prose-sm sm:prose lg:prose-lg xl:prose-2xl focus:outline-none min-h-[300px] p-4 border border-t-0 border-gray-300 rounded-b-lg'
    }
  }
})

watch(() => props.modelValue, (value) => {
  const isSame = editor.value?.getHTML() === value
  if (isSame || !editor.value) return
  editor.value.commands.setContent(value, false)
})

onBeforeUnmount(() => {
  editor.value?.destroy()
})

const addImage = async () => {
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'image/*'
  input.onchange = async () => {
    if (input.files && input.files[0]) {
      const file = input.files[0]
      const formData = new FormData()
      formData.append('file', file)
      try {
        const { data } = await api.post('/api/uploads/image', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
        editor.value?.chain().focus().setImage({ src: data.url }).run()
      } catch (e) {
        alert('Error al subir la imagen')
      }
    }
  }
  input.click()
}

const addYoutubeVideo = () => {
  const url = prompt('URL del video de YouTube:')
  if (url && editor.value) {
    editor.value.commands.setYoutubeVideo({ src: url })
  }
}

const setLink = () => {
  const previousUrl = editor.value?.getAttributes('link').href
  const url = window.prompt('URL', previousUrl)
  if (url === null) return
  if (url === '') {
    editor.value?.chain().focus().extendMarkRange('link').unsetLink().run()
    return
  }
  editor.value?.chain().focus().extendMarkRange('link').setLink({ href: url }).run()
}
</script>

<template>
  <div class="editor-wrapper bg-white">
    <div v-if="editor" class="toolbar border border-gray-300 rounded-t-lg bg-gray-50 p-2 flex flex-wrap gap-1 items-center">
      <button @click="editor.chain().focus().toggleBold().run()" :class="{ 'bg-upec-green text-white': editor.isActive('bold') }" class="p-1.5 rounded hover:bg-gray-200" title="Negrita" type="button"><b>B</b></button>
      <button @click="editor.chain().focus().toggleItalic().run()" :class="{ 'bg-upec-green text-white': editor.isActive('italic') }" class="p-1.5 rounded hover:bg-gray-200" title="Cursiva" type="button"><i>I</i></button>
      <span class="w-px h-5 bg-gray-300 mx-1"></span>
      <button @click="editor.chain().focus().toggleHeading({ level: 1 }).run()" :class="{ 'bg-upec-green text-white': editor.isActive('heading', { level: 1 }) }" class="p-1.5 rounded hover:bg-gray-200 font-bold" type="button">H1</button>
      <button @click="editor.chain().focus().toggleHeading({ level: 2 }).run()" :class="{ 'bg-upec-green text-white': editor.isActive('heading', { level: 2 }) }" class="p-1.5 rounded hover:bg-gray-200 font-bold" type="button">H2</button>
      <button @click="editor.chain().focus().toggleHeading({ level: 3 }).run()" :class="{ 'bg-upec-green text-white': editor.isActive('heading', { level: 3 }) }" class="p-1.5 rounded hover:bg-gray-200 font-bold" type="button">H3</button>
      <span class="w-px h-5 bg-gray-300 mx-1"></span>
      <button @click="editor.chain().focus().toggleBulletList().run()" :class="{ 'bg-upec-green text-white': editor.isActive('bulletList') }" class="p-1.5 rounded hover:bg-gray-200" type="button">• Lista</button>
      <button @click="editor.chain().focus().toggleOrderedList().run()" :class="{ 'bg-upec-green text-white': editor.isActive('orderedList') }" class="p-1.5 rounded hover:bg-gray-200" type="button">1. Lista</button>
      <button @click="editor.chain().focus().toggleBlockquote().run()" :class="{ 'bg-upec-green text-white': editor.isActive('blockquote') }" class="p-1.5 rounded hover:bg-gray-200" type="button">" Cita</button>
      <span class="w-px h-5 bg-gray-300 mx-1"></span>
      <button @click="setLink" :class="{ 'bg-upec-green text-white': editor.isActive('link') }" class="p-1.5 rounded hover:bg-gray-200 text-sm" type="button">Link</button>
      <button @click="addImage" class="p-1.5 rounded hover:bg-gray-200 text-sm" type="button">Img</button>
      <button @click="addYoutubeVideo" class="p-1.5 rounded hover:bg-gray-200 text-sm" type="button">YT</button>
      <span class="w-px h-5 bg-gray-300 mx-1"></span>
      <button @click="editor.chain().focus().insertTable({ rows: 3, cols: 3, withHeaderRow: true }).run()" class="p-1.5 rounded hover:bg-gray-200 text-sm" type="button">Tabla</button>
      <span class="w-px h-5 bg-gray-300 mx-1"></span>
      <button @click="editor.chain().focus().undo().run()" :disabled="!editor.can().undo()" class="p-1.5 rounded hover:bg-gray-200 text-sm disabled:opacity-50" type="button">Deshacer</button>
      <button @click="editor.chain().focus().redo().run()" :disabled="!editor.can().redo()" class="p-1.5 rounded hover:bg-gray-200 text-sm disabled:opacity-50" type="button">Rehacer</button>
    </div>
    <EditorContent :editor="editor" class="prose-upec" />
  </div>
</template>

<style>
.ProseMirror p.is-editor-empty:first-child::before {
  content: attr(data-placeholder);
  float: left;
  color: #adb5bd;
  pointer-events: none;
  height: 0;
}
.ProseMirror img {
  max-width: 100%;
  height: auto;
}
.ProseMirror iframe {
  width: 100%;
  aspect-ratio: 16 / 9;
}
</style>
