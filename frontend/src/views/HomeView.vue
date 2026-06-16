<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Sparkles, FileText, Image as ImageIcon, Wand2, ArrowRight, AlertCircle } from 'lucide-vue-next'
import Uploader from '@/components/Uploader.vue'
import { analyzeText, analyzeImage } from '@/api/client'
import { useHistoryStore } from '@/stores/history'

const router = useRouter()
const history = useHistoryStore()

const tab = ref<'text' | 'image'>('text')
const text = ref('')
const files = ref<File[]>([])
const userRole = ref('我')
const extra = ref('')
const loading = ref(false)
const error = ref('')

const SAMPLE = `[2026-06-15 10:23] 我: 在吗？周末有空吗
[2026-06-15 10:25] 她: 在 怎么了
[2026-06-15 10:26] 我: 想约你看个电影
[2026-06-15 10:30] 她: 嗯…最近有点忙
[2026-06-15 10:31] 我: 好吧 那下次吧
[2026-06-15 10:35] 她: 嗯嗯`

function useSample() {
  tab.value = 'text'
  text.value = SAMPLE
}

async function start() {
  error.value = ''
  if (tab.value === 'text' && !text.value.trim()) {
    error.value = '请粘贴聊天记录'
    return
  }
  if (tab.value === 'image' && files.value.length === 0) {
    error.value = '请上传至少一张截图'
    return
  }

  loading.value = true
  try {
    const result =
      tab.value === 'text'
        ? await analyzeText({
            raw_text: text.value,
            user_role: userRole.value,
            extra_context: extra.value,
          })
        : await analyzeImage(files.value)

    const preview =
      tab.value === 'text'
        ? text.value.slice(0, 80)
        : `[图片] ${files.value[0].name}`

    await history.add({
      id: result.analysis_id,
      created_at: Date.now(),
      input_type: tab.value,
      preview,
      result,
    })

    router.push(`/result/${result.analysis_id}`)
  } catch (e: any) {
    error.value = e?.msg || e?.message || '分析失败，请稍后重试'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="bg-aurora min-h-[calc(100vh-4rem)]">
    <div class="max-w-3xl mx-auto px-6 py-12 sm:py-20">
      <!-- Hero -->
      <div class="text-center mb-10 animate-fade-in">
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-500/10 text-brand-600 dark:text-brand-400 text-xs font-mono mb-4 border border-brand-500/20">
          <Sparkles :size="12" />
          <span>AI · 对话教练</span>
        </div>
        <h1 class="font-display text-4xl sm:text-5xl font-bold tracking-tight mb-3">
          不止替你回，<br class="sm:hidden" />
          <span class="bg-gradient-to-r from-brand-500 to-accent-500 bg-clip-text text-transparent">
            更教你如何回
          </span>
        </h1>
        <p class="text-[var(--fg-secondary)] text-base max-w-xl mx-auto">
          上传微信截图或粘贴聊天记录，AI 帮你分析关系、情绪、风险，<br class="hidden sm:inline" />
          并生成 5 种风格的回复建议。
        </p>
      </div>

      <!-- Card -->
      <div class="rounded-3xl bg-[var(--bg-card)] border border-[var(--border)] shadow-card p-6 sm:p-8 animate-fade-up">
        <!-- Tabs -->
        <div class="flex gap-1 p-1 rounded-xl bg-[var(--bg-elevated)] mb-6 max-w-xs">
          <button
            v-for="t in ['text', 'image'] as const"
            :key="t"
            @click="tab = t"
            class="flex-1 flex items-center justify-center gap-1.5 py-2 rounded-lg text-sm font-medium transition"
            :class="tab === t
              ? 'bg-[var(--bg-card)] shadow text-[var(--fg-primary)]'
              : 'text-[var(--fg-muted)] hover:text-[var(--fg-secondary)]'"
          >
            <FileText v-if="t === 'text'" :size="14" />
            <ImageIcon v-else :size="14" />
            {{ t === 'text' ? '文本' : '图片' }}
          </button>
        </div>

        <!-- Text -->
        <div v-if="tab === 'text'">
          <textarea
            v-model="text"
            :disabled="loading"
            rows="10"
            placeholder="[时间] 发送方: 内容&#10;[2026-06-15 10:23] 我: 在吗&#10;[2026-06-15 10:24] 她: 嗯嗯"
            class="w-full rounded-xl bg-[var(--bg-elevated)] border border-[var(--border)] focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 outline-none p-4 text-sm font-mono resize-y transition"
          />
          <button
            v-if="!text"
            @click="useSample"
            class="mt-2 text-xs text-[var(--fg-muted)] hover:text-brand-500 transition flex items-center gap-1"
          >
            <Wand2 :size="12" />
            加载示例数据
          </button>
        </div>

        <!-- Image -->
        <div v-else>
          <Uploader v-model:files="files" :loading="loading" />
        </div>

        <!-- Optional -->
        <div v-if="!loading" class="mt-6 grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label class="text-[11px] font-mono text-[var(--fg-muted)] uppercase tracking-wider">
              我方身份
            </label>
            <input
              v-model="userRole"
              placeholder="我 / 我方 / 用户"
              class="mt-1 w-full rounded-lg bg-[var(--bg-elevated)] border border-[var(--border)] focus:border-brand-500 outline-none px-3 py-2 text-sm transition"
            />
          </div>
          <div>
            <label class="text-[11px] font-mono text-[var(--fg-muted)] uppercase tracking-wider">
              额外背景
            </label>
            <input
              v-model="extra"
              placeholder="例如：刚认识 2 周的同事"
              class="mt-1 w-full rounded-lg bg-[var(--bg-elevated)] border border-[var(--border)] focus:border-brand-500 outline-none px-3 py-2 text-sm transition"
            />
          </div>
        </div>

        <!-- Error -->
        <div v-if="error" class="mt-4 flex items-start gap-2 rounded-lg bg-rose-500/10 border border-rose-500/20 px-3 py-2 text-sm text-rose-600 dark:text-rose-400">
          <AlertCircle :size="16" class="mt-0.5 flex-shrink-0" />
          <span>{{ error }}</span>
        </div>

        <!-- Submit -->
        <button
          @click="start"
          :disabled="loading"
          class="mt-6 w-full py-3.5 rounded-xl font-display font-semibold text-white bg-gradient-to-r from-brand-500 to-accent-500 hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed transition shadow-glow flex items-center justify-center gap-2"
        >
          <span v-if="!loading" class="flex items-center gap-2">
            开始分析
            <ArrowRight :size="18" />
          </span>
          <span v-else class="flex items-center gap-2">
            <span class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            正在分析中...
          </span>
        </button>

        <p class="mt-4 text-center text-xs text-[var(--fg-muted)]">
          🔒 你的聊天内容不会被保存，临时文件 1 小时内自动清理
        </p>
      </div>
    </div>
  </div>
</template>
