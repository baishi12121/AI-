/**
 * history store 测试
 */
import { describe, it, expect, beforeEach, vi } from 'vitest'

// mock idb-keyval 避免依赖 indexedDB
vi.mock('idb-keyval', () => ({
  get: vi.fn().mockResolvedValue(undefined),
  set: vi.fn().mockResolvedValue(undefined),
  del: vi.fn().mockResolvedValue(undefined),
}))

import { setActivePinia, createPinia } from 'pinia'
import { useHistoryStore, type HistoryItem } from '../stores/history'

const sampleItem: HistoryItem = {
  id: 'a1',
  created_at: Date.now(),
  input_type: 'text',
  preview: '在吗？',
  result: {
    analysis_id: 'a1',
    input_type: 'text',
    messages: [],
    relationship: { label: '朋友', confidence: 0.8 },
    stage: '破冰',
    emotion: { label: '礼貌', score: 0.5 },
    risk: [],
    replies: [],
    health_report: { naturalness: 70, engagement: 60, silence_risk: 30, reply_quality: 65 },
    summary: '...',
    advice: [],
  },
}

describe('history store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  it('初始为空', () => {
    const s = useHistoryStore()
    expect(s.items).toEqual([])
  })

  it('add 后能 findById', async () => {
    const s = useHistoryStore()
    await s.add(sampleItem)
    expect(s.items.length).toBe(1)
    expect(s.findById('a1')).toBeTruthy()
  })

  it('add 同 id 会覆盖', async () => {
    const s = useHistoryStore()
    await s.add(sampleItem)
    await s.add({ ...sampleItem, preview: 'updated' })
    expect(s.items.length).toBe(1)
    expect(s.items[0].preview).toBe('updated')
  })

  it('最多保留 20 条', async () => {
    const s = useHistoryStore()
    for (let i = 0; i < 25; i++) {
      await s.add({ ...sampleItem, id: `id-${i}` })
    }
    expect(s.items.length).toBe(20)
  })

  it('remove 移除指定项', async () => {
    const s = useHistoryStore()
    await s.add({ ...sampleItem, id: 'a1' })
    await s.add({ ...sampleItem, id: 'a2' })
    await s.remove('a1')
    expect(s.items.length).toBe(1)
    expect(s.findById('a1')).toBeUndefined()
    expect(s.findById('a2')).toBeTruthy()
  })

  it('clear 清空', async () => {
    const s = useHistoryStore()
    await s.add(sampleItem)
    await s.clear()
    expect(s.items.length).toBe(0)
  })

  it('新项排在最前', async () => {
    const s = useHistoryStore()
    await s.add({ ...sampleItem, id: 'old' })
    await s.add({ ...sampleItem, id: 'new' })
    expect(s.items[0].id).toBe('new')
    expect(s.items[1].id).toBe('old')
  })
})
