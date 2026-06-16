<script setup lang="ts">
import { Copy, Check, ThumbsUp, ThumbsDown } from 'lucide-vue-next'
import { ref } from 'vue'
import { styleLabel, styleEmoji } from '@/utils/format'
import { submitFeedback } from '@/api/client'

const props = defineProps<{
  index: number
  analysisId: string
  replyStyle: 'high_eq' | 'humor' | 'formal' | 'flirty' | 'concise'
  content: string
  reason: string
  expected: string[]
}>()

const copied = ref(false)
const feedback = ref<'up' | 'down' | null>(null)

async function copy() {
  try {
    await navigator.clipboard.writeText(props.content)
    copied.value = true
    setTimeout(() => (copied.value = false), 1500)
  } catch {
    /* noop */
  }
}

async function vote(useful: boolean) {
  feedback.value = useful ? 'up' : 'down'
  try {
    await submitFeedback({
      analysis_id: props.analysisId,
      reply_index: props.index,
      useful,
    })
  } catch {
    /* ignore */
  }
}
</script>

<template>
  <div class="rounded-2xl border border-[var(--border)] bg-[var(--bg-card)] p-6 shadow-card hover:shadow-glow transition-all duration-300">
    <div class="flex items-center justify-between mb-3">
      <div class="flex items-center gap-2">
        <span class="text-2xl">{{ styleEmoji[replyStyle] }}</span>
        <span class="font-display font-semibold text-base">{{ styleLabel[replyStyle] }}</span>
      </div>
      <button
        @click="copy"
        class="text-xs px-3 py-1.5 rounded-lg border border-[var(--border)] hover:bg-[var(--bg-elevated)] transition flex items-center gap-1.5 font-mono"
      >
        <Check v-if="copied" :size="14" class="text-emerald-500" />
        <Copy v-else :size="14" />
        {{ copied ? '已复制' : '复制' }}
      </button>
    </div>

    <p class="text-[15px] leading-relaxed text-[var(--fg-primary)] whitespace-pre-wrap mb-4">
      {{ content }}
    </p>

    <div class="rounded-xl bg-[var(--bg-elevated)] p-3 mb-3">
      <div class="text-[11px] font-mono text-[var(--fg-muted)] mb-1 uppercase tracking-wider">
        推荐理由
      </div>
      <p class="text-sm text-[var(--fg-secondary)] leading-relaxed">
        {{ reason }}
      </p>
    </div>

    <div v-if="expected.length" class="mb-3">
      <div class="text-[11px] font-mono text-[var(--fg-muted)] mb-1.5 uppercase tracking-wider">
        预期对方回复
      </div>
      <div class="flex flex-wrap gap-1.5">
        <span
          v-for="(e, i) in expected"
          :key="i"
          class="text-xs px-2.5 py-1 rounded-md bg-[var(--bg-elevated)] text-[var(--fg-secondary)]"
        >
          {{ e }}
        </span>
      </div>
    </div>

    <div class="flex items-center gap-2 pt-3 border-t border-[var(--border)]">
      <span class="text-[11px] text-[var(--fg-muted)] font-mono">这条有用吗？</span>
      <button
        @click="vote(true)"
        :class="[
          'w-7 h-7 rounded-md flex items-center justify-center transition',
          feedback === 'up'
            ? 'bg-emerald-500 text-white'
            : 'hover:bg-emerald-500/10 text-[var(--fg-muted)] hover:text-emerald-500',
        ]"
      >
        <ThumbsUp :size="14" />
      </button>
      <button
        @click="vote(false)"
        :class="[
          'w-7 h-7 rounded-md flex items-center justify-center transition',
          feedback === 'down'
            ? 'bg-rose-500 text-white'
            : 'hover:bg-rose-500/10 text-[var(--fg-muted)] hover:text-rose-500',
        ]"
      >
        <ThumbsDown :size="14" />
      </button>
    </div>
  </div>
</template>
