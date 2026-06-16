<script setup lang="ts">
defineProps<{
  emoji?: string
  label: string
  value?: string | number
  variant?: 'default' | 'brand' | 'accent' | 'danger' | 'success' | 'warning'
}>()
</script>

<template>
  <span
    class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium font-mono"
    :class="{
      'bg-[var(--bg-elevated)] text-[var(--fg-secondary)]': !variant || variant === 'default',
      'bg-brand-500/10 text-brand-600 dark:text-brand-400 border border-brand-500/20': variant === 'brand',
      'bg-accent-500/10 text-accent-600 dark:text-accent-400 border border-accent-500/20': variant === 'accent',
      'bg-rose-500/10 text-rose-600 dark:text-rose-400 border border-rose-500/20': variant === 'danger',
      'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20': variant === 'success',
      'bg-amber-500/10 text-amber-600 dark:text-amber-400 border border-amber-500/20': variant === 'warning',
    }"
  >
    <span v-if="emoji">{{ emoji }}</span>
    <span>{{ label }}</span>
    <span v-if="value !== undefined" class="opacity-70">·</span>
    <span v-if="value !== undefined">{{ value }}</span>
  </span>
</template>
