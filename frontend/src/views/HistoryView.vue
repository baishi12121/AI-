<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeft, Trash2, FileText, Image as ImageIcon } from 'lucide-vue-next'
import { useHistoryStore } from '@/stores/history'
import { formatTime } from '@/utils/format'

const router = useRouter()
const history = useHistoryStore()
const showConfirm = ref(false)

onMounted(() => {
  history.load()
})

async function clearAll() {
  await history.clear()
  showConfirm.value = false
}

function open(id: string) {
  router.push(`/result/${id}`)
}
</script>

<template>
  <div class="max-w-3xl mx-auto px-6 py-8 sm:py-12">
    <div class="flex items-center justify-between mb-6">
      <button
        @click="router.push('/')"
        class="flex items-center gap-1.5 text-sm text-[var(--fg-secondary)] hover:text-[var(--fg-primary)] transition"
      >
        <ArrowLeft :size="16" />
        返回
      </button>
      <button
        v-if="history.items.length"
        @click="showConfirm = true"
        class="text-sm text-rose-500 hover:text-rose-600 flex items-center gap-1.5"
      >
        <Trash2 :size="14" />
        清空
      </button>
    </div>

    <h1 class="font-display text-2xl font-bold mb-6">历史记录</h1>

    <div v-if="showConfirm" class="rounded-2xl bg-rose-500/10 border border-rose-500/20 p-4 mb-4 flex items-center justify-between">
      <span class="text-sm">确认清空所有历史记录？</span>
      <div class="flex gap-2">
        <button @click="showConfirm = false" class="text-sm px-3 py-1 rounded-md hover:bg-[var(--bg-elevated)]">取消</button>
        <button @click="clearAll" class="text-sm px-3 py-1 rounded-md bg-rose-500 text-white">确认</button>
      </div>
    </div>

    <div v-if="!history.items.length" class="text-center py-20 text-[var(--fg-muted)]">
      暂无历史记录
    </div>

    <div v-else class="space-y-2">
      <button
        v-for="it in history.items"
        :key="it.id"
        @click="open(it.id)"
        class="w-full text-left rounded-2xl bg-[var(--bg-card)] border border-[var(--border)] hover:border-brand-500 hover:shadow-glow transition p-4 flex items-center gap-4"
      >
        <div class="w-10 h-10 rounded-xl bg-[var(--bg-elevated)] flex items-center justify-center flex-shrink-0">
          <ImageIcon v-if="it.input_type === 'image'" :size="18" class="text-[var(--fg-secondary)]" />
          <FileText v-else :size="18" class="text-[var(--fg-secondary)]" />
        </div>
        <div class="flex-1 min-w-0">
          <div class="text-sm font-mono text-[var(--fg-muted)]">{{ formatTime(it.created_at) }}</div>
          <div class="text-sm text-[var(--fg-primary)] truncate mt-0.5">{{ it.preview }}</div>
        </div>
        <div class="text-xs text-brand-500 flex-shrink-0">查看 →</div>
      </button>
    </div>
  </div>
</template>
