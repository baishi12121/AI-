<script setup lang="ts">
import { ref, watch, onBeforeUnmount } from 'vue'
import { ImagePlus, X, Image as ImageIcon, Loader2 } from 'lucide-vue-next'

const props = withDefaults(
  defineProps<{
    files: File[]
    loading?: boolean
    max?: number
    maxSizeMB?: number
  }>(),
  { max: 5, maxSizeMB: 10 },
)

const emit = defineEmits<{
  (e: 'update:files', files: File[]): void
}>()

const dragOver = ref(false)
const inputRef = ref<HTMLInputElement | null>(null)
const previewUrls = ref<string[]>([])

// 每次 files 变化，重新生成预览 URL，并释放旧 URL
watch(
  () => props.files,
  (newFiles) => {
    // 释放旧 URL
    previewUrls.value.forEach((u) => {
      try {
        URL.revokeObjectURL(u)
      } catch {
        /* noop */
      }
    })
    // 为每个有效 File 生成新 URL
    const urls: string[] = []
    for (const f of (newFiles || []) as File[]) {
      if (f && typeof f === 'object' && 'type' in f) {
        try {
          urls.push(URL.createObjectURL(f))
        } catch {
          urls.push('')
        }
      } else {
        urls.push('')
      }
    }
    previewUrls.value = urls
  },
  { immediate: true, deep: true },
)

// 组件卸载时释放所有 URL
onBeforeUnmount(() => {
  previewUrls.value.forEach((u) => {
    if (u) {
      try {
        URL.revokeObjectURL(u)
      } catch {
        /* noop */
      }
    }
  })
  previewUrls.value = []
})

function pickFiles() {
  inputRef.value?.click()
}

function handleSelect(e: Event) {
  const target = e.target as HTMLInputElement
  if (!target.files) return
  addFiles(Array.from(target.files))
  target.value = ''
}

function addFiles(list: File[]) {
  const valid: File[] = []
  for (const f of list) {
    if (!f) continue
    if (!/^image\//.test(f.type || '')) continue
    if (f.size > props.maxSizeMB * 1024 * 1024) continue
    valid.push(f)
  }
  const next = [...(props.files || []), ...valid].slice(0, props.max)
  emit('update:files', next)
}

function handleDrop(e: DragEvent) {
  e.preventDefault()
  dragOver.value = false
  if (!e.dataTransfer) return
  addFiles(Array.from(e.dataTransfer.files))
}

function remove(idx: number) {
  const next = (props.files || []).filter((_, i) => i !== idx)
  emit('update:files', next)
}
</script>

<template>
  <div>
    <div
      v-if="(files?.length || 0) < max"
      @click="pickFiles"
      @dragover.prevent="dragOver = true"
      @dragleave="dragOver = false"
      @drop="handleDrop"
      class="cursor-pointer rounded-2xl border-2 border-dashed transition-all duration-200 p-10 flex flex-col items-center justify-center gap-3 text-center"
      :class="dragOver
        ? 'border-brand-500 bg-brand-500/5'
        : 'border-[var(--border)] hover:border-brand-400 hover:bg-[var(--bg-card)]'"
    >
      <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-brand-500/10 to-accent-500/10 flex items-center justify-center">
        <ImagePlus v-if="!loading" :size="28" class="text-brand-500" />
        <Loader2 v-else :size="28" class="text-brand-500 animate-spin" />
      </div>
      <div>
        <div class="font-display font-semibold text-base">点击或拖拽上传聊天截图</div>
        <div class="text-sm text-[var(--fg-muted)] mt-1">
          支持 PNG / JPG / WebP，单张 ≤ {{ maxSizeMB }}MB，最多 {{ max }} 张
        </div>
      </div>
      <input
        ref="inputRef"
        type="file"
        accept="image/*"
        multiple
        class="hidden"
        @change="handleSelect"
      />
    </div>

    <div v-if="files?.length" class="mt-4 grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
      <div
        v-for="(f, i) in files"
        :key="i"
        class="relative group rounded-xl overflow-hidden border border-[var(--border)] aspect-square bg-[var(--bg-elevated)]"
      >
        <img
          v-if="previewUrls[i]"
          :src="previewUrls[i]"
          :alt="f?.name || `image-${i}`"
          class="w-full h-full object-cover"
        />
        <div
          v-else
          class="w-full h-full flex items-center justify-center text-[var(--fg-muted)]"
        >
          <ImageIcon :size="32" />
        </div>
        <button
          @click="remove(i)"
          class="absolute top-2 right-2 w-7 h-7 rounded-full bg-black/60 hover:bg-rose-500 text-white flex items-center justify-center opacity-0 group-hover:opacity-100 transition"
          title="移除"
        >
          <X :size="14" />
        </button>
        <div class="absolute bottom-0 inset-x-0 bg-gradient-to-t from-black/60 to-transparent px-2 py-1.5 text-[10px] text-white font-mono opacity-0 group-hover:opacity-100 transition truncate">
          {{ f?.name || `image-${i}` }}
        </div>
      </div>
    </div>
  </div>
</template>
