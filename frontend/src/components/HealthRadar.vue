<script setup lang="ts">
defineProps<{
  report: {
    naturalness: number
    engagement: number
    silence_risk: number
    reply_quality: number
  }
  advice: string[]
}>()

const items: Array<{
  key: 'naturalness' | 'engagement' | 'silence_risk' | 'reply_quality'
  label: string
  icon: string
  inverse?: true
}> = [
  { key: 'naturalness', label: '自然度', icon: '✨' },
  { key: 'engagement', label: '互动度', icon: '🔥' },
  { key: 'silence_risk', label: '冷场风险', icon: '🥶', inverse: true },
  { key: 'reply_quality', label: '回复质量', icon: '🎯' },
]

function color(v: number) {
  if (v >= 80) return 'from-emerald-500 to-emerald-400'
  if (v >= 60) return 'from-brand-500 to-brand-400'
  if (v >= 40) return 'from-amber-500 to-amber-400'
  return 'from-rose-500 to-rose-400'
}
</script>

<template>
  <div class="rounded-2xl border border-[var(--border)] bg-[var(--bg-card)] p-6">
    <div class="flex items-center justify-between mb-5">
      <h3 class="font-display font-semibold text-lg flex items-center gap-2">
        <span>📊</span>
        <span>聊天体检报告</span>
      </h3>
      <span class="text-xs text-[var(--fg-muted)] font-mono">AI 量化评估</span>
    </div>

    <div class="space-y-4">
      <div v-for="item in items" :key="item.key" class="space-y-1.5">
        <div class="flex items-center justify-between text-sm">
          <span class="flex items-center gap-2 text-[var(--fg-secondary)]">
            <span>{{ item.icon }}</span>
            <span>{{ item.label }}</span>
          </span>
          <span class="font-mono font-semibold tabular-nums">
            {{ report[item.key] }}
            <span class="text-[var(--fg-muted)] text-xs">{{ item.inverse ? '%' : '' }}</span>
          </span>
        </div>
        <div class="h-2 rounded-full bg-[var(--bg-elevated)] overflow-hidden">
          <div
            class="h-full rounded-full bg-gradient-to-r transition-all duration-700"
            :class="color(item.inverse ? 100 - report[item.key] : report[item.key])"
            :style="{ width: report[item.key] + '%' }"
          />
        </div>
      </div>
    </div>

    <div v-if="advice.length" class="mt-6 pt-5 border-t border-[var(--border)]">
      <div class="text-[11px] font-mono text-[var(--fg-muted)] mb-2 uppercase tracking-wider">
        改进建议
      </div>
      <ul class="space-y-1.5 text-sm text-[var(--fg-secondary)]">
        <li v-for="(a, i) in advice" :key="i" class="flex gap-2">
          <span class="text-brand-500">→</span>
          <span>{{ a }}</span>
        </li>
      </ul>
    </div>
  </div>
</template>
