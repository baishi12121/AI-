/**
 * Uploader 组件测试
 */
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'

// mock lucide icons
vi.mock('lucide-vue-next', () => ({
  ImagePlus: { template: '<span />' },
  X: { template: '<span />' },
  ImageIcon: { template: '<span />' },
  Loader2: { template: '<span />' },
}))

import Uploader from '../components/Uploader.vue'

describe('Uploader.vue', () => {
  beforeEach(() => {
    document.body.innerHTML = ''
  })

  it('初始无文件时显示拖拽区', () => {
    const w = mount(Uploader, { props: { files: [] } })
    expect(w.text()).toContain('点击或拖拽上传聊天截图')
  })

  it('有文件时显示预览网格', () => {
    const file = new File(['x'], 'test.png', { type: 'image/png' })
    const w = mount(Uploader, { props: { files: [file] } })
    expect(w.find('img').exists()).toBe(true)
  })

  it('emit update:files 当文件被添加', async () => {
    const w = mount(Uploader, { props: { files: [] } })
    const input = w.find('input[type="file"]')
    const file = new File(['x'], 'test.png', { type: 'image/png' })
    Object.defineProperty(input.element, 'files', { value: [file], configurable: true })
    await input.trigger('change')
    expect(w.emitted('update:files')).toBeTruthy()
  })

  it('emit update:files 当点击移除按钮', async () => {
    const file1 = new File(['x'], 'a.png', { type: 'image/png' })
    const file2 = new File(['y'], 'b.png', { type: 'image/png' })
    const w = mount(Uploader, { props: { files: [file1, file2] } })
    const removeBtn = w.find('button[title="移除"]')
    expect(removeBtn.exists()).toBe(true)
    await removeBtn.trigger('click')
    const emitted = w.emitted('update:files')
    expect(emitted).toBeTruthy()
    if (emitted && emitted[0]) {
      const next = emitted[0][0] as File[]
      expect(next.length).toBe(1)
      expect(next[0].name).toBe('b.png')
    }
  })

  it('超过 max 数量时禁用拖拽区', () => {
    const files = [new File(['x'], 'a0.png', { type: 'image/png' })]
    const w = mount(Uploader, { props: { files, max: 1 } })
    expect(w.text()).not.toContain('点击或拖拽上传聊天截图')
  })

  it('文件超过 maxSizeMB 被过滤', async () => {
    const w = mount(Uploader, { props: { files: [], maxSizeMB: 1 } })
    const bigFile = new File([new Uint8Array(2 * 1024 * 1024)], 'big.png', {
      type: 'image/png',
    })
    const input = w.find('input[type="file"]')
    Object.defineProperty(input.element, 'files', { value: [bigFile], configurable: true })
    await input.trigger('change')
    const emitted = w.emitted('update:files')
    if (emitted && emitted[0]) {
      const next = emitted[0][0] as File[]
      expect(next.length).toBe(0)
    }
  })

  it('非图片类型被过滤', async () => {
    const w = mount(Uploader, { props: { files: [] } })
    const txtFile = new File(['hello'], 'test.txt', { type: 'text/plain' })
    const input = w.find('input[type="file"]')
    Object.defineProperty(input.element, 'files', { value: [txtFile], configurable: true })
    await input.trigger('change')
    const emitted = w.emitted('update:files')
    if (emitted && emitted[0]) {
      const next = emitted[0][0] as File[]
      expect(next.length).toBe(0)
    }
  })
})
