<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft, RefreshCw, AlertCircle } from 'lucide-vue-next'
import Tag from '@/components/Tag.vue'
import ReplyCard from '@/components/ReplyCard.vue'
import HealthRadar from '@/components/HealthRadar.vue'
import { useHistoryStore, type HistoryItem } from '@/stores/history'
import {
  relationshipEmoji,
  stageEmoji,
  emotionEmoji,
  riskColor,
  riskLabel,
  formatTime,
} from '@/utils/format'

const route = useRoute()
const router = useRouter()
const history = useHistoryStore()

const item = ref<HistoryItem | null>(null)
const error = ref('')

onMounted(async () => {
  try {
    await history.load()
    const id = route.params.id as string
    const found = history.findById(id)
    if (found) {
      item.value = found
    } else {
      error.value = '未找到该分析记录，可能已被清理'
    }
  } catch (e: any) {
    error.value = e?.message || '加载失败'
  }
})

const r = computed(() => item.value?.result)
</script>

<template>
  <div class="bg-aurora min-h-[calc(100vh-4rem)]">
    <div class="max-w-5xl mx-auto px-6 py-8 sm:py-12">
      <!-- Error -->
      <div v-if="error" class="rounded-2xl bg-rose-500/10 border border-rose-500/20 p-6 flex items-start gap-3">
        <AlertCircle :size="20" class="text-rose-500 mt-0.5" />
        <div>
          <div class="font-semibold mb-1">{{ error }}</div>
          <button @click="router.push('/')" class="text-sm text-brand-500 hover:underline">返回首页</button>
        </div>
      </div>

      <template v-else-if="r">
        <!-- Header -->
        <div class="flex items-center justify-between mb-6">
          <button
            @click="router.push('/')"
            class="flex items-center gap-1.5 text-sm text-[var(--fg-secondary)] hover:text-[var(--fg-primary)] transition"
          >
            <ArrowLeft :size="16" />
            返回
          </button>
          <div class="flex items-center gap-2 text-xs text-[var(--fg-muted)] font-mono">
            {{ formatTime(item!.created_at) }}
          </div>
        </div>

        <!-- Status Pills -->
        <div class="flex flex-wrap gap-2 mb-6 animate-fade-in">
          <Tag
            :emoji="relationshipEmoji[r.relationship.label]"
            :label="r.relationship.label"
            variant="brand"
            :value="Math.round(r.relationship.confidence * 100) + '%'"
          />
          <Tag
            :emoji="stageEmoji[r.stage]"
            :label="r.stage + '阶段'"
            variant="accent"
          />
          <Tag
            :emoji="emotionEmoji[r.emotion.label]"
            :label="'情绪·' + r.emotion.label"
            variant="default"
            :value="Math.round(r.emotion.score * 100) + '%'"
          />
          <Tag
            v-if="r.risk.length === 0"
            emoji="✅"
            label="无明显风险"
            variant="success"
          />
          <Tag
            v-for="(rk, i) in r.risk"
            :key="i"
            :label="'风险·' + (riskLabel[rk.type] || rk.type)"
            :class="riskColor[rk.level] || ''"
          />
        </div>

        <!-- 关系/阶段/情绪/风险 详细 -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-8">
          <div class="rounded-2xl bg-[var(--bg-card)] border border-[var(--border)] p-4">
            <div class="text-[11px] font-mono text-[var(--fg-muted)] uppercase tracking-wider mb-2">
              关系判断
            </div>
            <div class="font-display font-semibold text-lg">
              {{ r.relationship.label }}
            </div>
            <p v-if="r.relationship.evidence" class="mt-1 text-sm text-[var(--fg-secondary)]">
              {{ r.relationship.evidence }}
            </p>
          </div>
          <div class="rounded-2xl bg-[var(--bg-card)] border border-[var(--border)] p-4">
            <div class="text-[11px] font-mono text-[var(--fg-muted)] uppercase tracking-wider mb-2">
              聊天阶段
            </div>
            <div class="font-display font-semibold text-lg">
              {{ r.stage }}
            </div>
            <div class="mt-1 text-sm text-[var(--fg-secondary)]">
              对方情绪：<span class="font-medium">{{ r.emotion.label }}</span>
            </div>
          </div>
        </div>

        <!-- Replies -->
        <div class="mb-8">
          <div class="flex items-center justify-between mb-4">
            <h2 class="font-display font-semibold text-xl flex items-center gap-2">
              <span>💬</span>
              <span>推荐回复（{{ r.replies.length }} 种风格）</span>
            </h2>
          </div>
          <div class="grid grid-cols-1 gap-4">
            <ReplyCard
              v-for="(rep, i) in r.replies"
              :key="i"
              :index="i"
              :analysis-id="r.analysis_id"
              :reply-style="rep.style"
              :content="rep.content"
              :reason="rep.reason"
              :expected="rep.expected_reply"
              class="animate-fade-up"
              :style="{ animationDelay: i * 80 + 'ms' }"
            />
          </div>
        </div>

        <!-- Health Report -->
        <div class="mb-8 animate-fade-up" :style="{ animationDelay: '400ms' }">
          <HealthRadar :report="r.health_report" :advice="r.advice" />
        </div>

        <!-- Summary -->
        <div class="rounded-2xl bg-gradient-to-br from-brand-500/10 to-accent-500/10 border border-brand-500/20 p-6 mb-8 animate-fade-up" :style="{ animationDelay: '480ms' }">
          <div class="text-[11px] font-mono text-brand-600 dark:text-brand-400 uppercase tracking-wider mb-2 flex items-center gap-2">
            <span>✨</span>
            <span>本轮聊天总结</span>
          </div>
          <p class="text-[15px] leading-relaxed text-[var(--fg-primary)]">
            {{ r.summary }}
          </p>
          <div v-if="r.ocr_text" class="mt-4 pt-4 border-t border-[var(--border)]/50">
            <div class="text-[11px] font-mono text-[var(--fg-muted)] mb-1">OCR 识别原文</div>
            <pre class="text-xs font-mono text-[var(--fg-secondary)] whitespace-pre-wrap">{{ r.ocr_text }}</pre>
          </div>
        </div>

        <!-- Bottom action -->
        <div class="flex justify-center pb-8">
          <button
            @click="router.push('/')"
            class="px-6 py-3 rounded-xl bg-[var(--bg-card)] border border-[var(--border)] hover:border-brand-500 hover:shadow-glow transition font-medium flex items-center gap-2"
          >
            <RefreshCw :size="16" />
            再分析一次
          </button>
        </div>
      </template>

      <div v-else class="space-y-4">
        <div v-for="i in 3" :key="i" class="rounded-2xl bg-[var(--bg-card)] border border-[var(--border)] p-6 h-32 shimmer" />
      </div>
    </div>
  </div>
</template>
