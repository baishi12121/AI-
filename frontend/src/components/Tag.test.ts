/**
 * Tag 组件测试
 */
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import Tag from '../components/Tag.vue'

describe('Tag.vue', () => {
  it('渲染 label', () => {
    const w = mount(Tag, { props: { label: '测试标签' } })
    expect(w.text()).toContain('测试标签')
  })

  it('emoji 与 value 显示', () => {
    const w = mount(Tag, {
      props: { label: '朋友', emoji: '🧑', value: '85%', variant: 'brand' },
    })
    expect(w.text()).toContain('🧑')
    expect(w.text()).toContain('朋友')
    expect(w.text()).toContain('85%')
  })

  it('不同 variant 应用不同 class', () => {
    const variants = ['brand', 'accent', 'danger', 'success', 'warning'] as const
    for (const v of variants) {
      const w = mount(Tag, { props: { label: 'x', variant: v } })
      expect(w.html()).toBeTruthy()
    }
  })

  it('默认 variant 是 default', () => {
    const w = mount(Tag, { props: { label: 'x' } })
    expect(w.classes().join(' ')).not.toContain('bg-brand')
  })
})
