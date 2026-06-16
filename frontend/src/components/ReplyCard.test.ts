/**
 * ReplyCard 组件测试
 */
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'

// mock lucide icons
vi.mock('lucide-vue-next', () => ({
  Copy: { template: '<span />' },
  Check: { template: '<span />' },
  ThumbsUp: { template: '<span />' },
  ThumbsDown: { template: '<span />' },
}))

// mock API
vi.mock('../api/client', () => ({
  submitFeedback: vi.fn().mockResolvedValue({ ok: true }),
}))

import ReplyCard from '../components/ReplyCard.vue'

describe('ReplyCard.vue', () => {
  const baseProps = {
    index: 0,
    analysisId: 'test-123',
    replyStyle: 'high_eq' as const,
    content: '这是一个测试回复',
    reason: '测试推荐理由',
    expected: ['好的', '可以'],
  }

  beforeEach(() => {
    setActivePinia(createPinia())
    // happy-dom 下 navigator.clipboard 是只读 getter，需用 defineProperty
    Object.defineProperty(navigator, 'clipboard', {
      value: { writeText: vi.fn().mockResolvedValue(undefined) },
      configurable: true,
      writable: true,
    })
  })

  it('渲染回复内容与推荐理由', () => {
    const w = mount(ReplyCard, { props: baseProps })
    expect(w.text()).toContain('这是一个测试回复')
    expect(w.text()).toContain('测试推荐理由')
  })

  it('显示风格标签', () => {
    const w = mount(ReplyCard, { props: baseProps })
    expect(w.text()).toContain('高情商')
  })

  it('显示预期回复', () => {
    const w = mount(ReplyCard, { props: baseProps })
    expect(w.text()).toContain('好的')
    expect(w.text()).toContain('可以')
  })

  it('点击复制按钮调用 clipboard', async () => {
    const w = mount(ReplyCard, { props: baseProps })
    const buttons = w.findAll('button')
    const copyBtn = buttons.find((b) => b.text().includes('复制'))
    expect(copyBtn).toBeTruthy()
    await copyBtn!.trigger('click')
    await flushPromises()
    expect(navigator.clipboard.writeText).toHaveBeenCalledWith('这是一个测试回复')
  })
})
