// 关系标签 → 颜色
export const relationshipEmoji: Record<string, string> = {
  同事: '🤝',
  老板: '👔',
  客户: '💼',
  女朋友: '💑',
  男朋友: '💑',
  家长: '👨‍👩‍👧',
  朋友: '🧑‍🤝‍🧑',
  陌生人: '👋',
}

export const stageEmoji: Record<string, string> = {
  破冰: '🌱',
  热聊: '🔥',
  平稳: '🌊',
  冷场: '🥶',
  收尾: '👋',
}

export const emotionEmoji: Record<string, string> = {
  开心: '😊',
  生气: '😠',
  敷衍: '😑',
  礼貌: '🙂',
  好奇: '🤔',
  无聊: '🥱',
  难过: '😢',
}

export const riskColor: Record<string, string> = {
  low: 'text-emerald-500 bg-emerald-500/10',
  mid: 'text-amber-500 bg-amber-500/10',
  high: 'text-rose-500 bg-rose-500/10',
}

export const riskLabel: Record<string, string> = {
  single_side_initiative: '单方主动',
  short_reply: '回复敷衍',
  dead_topic: '话题已死',
  sensitive_word: '敏感词',
  do_not_continue: '不建议继续',
}

export const styleLabel: Record<string, string> = {
  high_eq: '高情商',
  humor: '幽默',
  formal: '正式',
  flirty: '暧昧',
  concise: '简洁',
}

export const styleEmoji: Record<string, string> = {
  high_eq: '💎',
  humor: '😄',
  formal: '🎩',
  flirty: '💕',
  concise: '⚡',
}

export function formatTime(ts: number): string {
  const d = new Date(ts)
  const pad = (n: number) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`
}
