<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Sun, Moon, History, Sparkles } from 'lucide-vue-next'

const router = useRouter()
const isDark = ref(false)

onMounted(() => {
  isDark.value = document.documentElement.classList.contains('dark')
})

function toggleTheme() {
  const root = document.documentElement
  root.classList.toggle('dark')
  isDark.value = root.classList.contains('dark')
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
}
</script>

<template>
  <header class="sticky top-0 z-30 backdrop-blur-md bg-[var(--bg-base)]/80 border-b border-[var(--border)]">
    <div class="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
      <button
        @click="router.push('/')"
        class="flex items-center gap-2 group"
      >
        <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-brand-500 to-accent-500 flex items-center justify-center shadow-glow">
          <Sparkles :size="18" class="text-white" />
        </div>
        <div class="font-display font-semibold text-lg tracking-tight">
          AI 社恐聊天外挂
        </div>
      </button>

      <div class="flex items-center gap-1">
        <button
          @click="router.push('/history')"
          class="w-9 h-9 rounded-lg flex items-center justify-center hover:bg-[var(--bg-elevated)] text-[var(--fg-secondary)] hover:text-[var(--fg-primary)] transition"
          title="历史记录"
        >
          <History :size="18" />
        </button>
        <button
          @click="toggleTheme"
          class="w-9 h-9 rounded-lg flex items-center justify-center hover:bg-[var(--bg-elevated)] text-[var(--fg-secondary)] hover:text-[var(--fg-primary)] transition"
          title="切换主题"
        >
          <Sun v-if="isDark" :size="18" />
          <Moon v-else :size="18" />
        </button>
      </div>
    </div>
  </header>
</template>
