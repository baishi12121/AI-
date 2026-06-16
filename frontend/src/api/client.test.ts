/**
 * api/client 测试（mock axios）
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'
import axios from 'axios'

vi.mock('axios', () => {
  // 真实实现拦截器：保存 success 回调，post 时调用
  let successHandler: ((r: any) => any) | null = null
  let nextResponse: any = { data: null }
  const mockAxios: any = {
    create: vi.fn(() => mockAxios),
    interceptors: {
      response: {
        use: vi.fn((onFulfilled: any) => {
          successHandler = onFulfilled
        }),
      },
    },
    post: vi.fn(async (..._args: any[]) => {
      const resp = nextResponse
      if (successHandler) return successHandler(resp)
      return resp
    }),
    get: vi.fn(),
    __setNextResponse: (r: any) => {
      nextResponse = r
    },
  }
  return { default: mockAxios }
})

describe('api/client', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('analyzeText 调用 /analyze/text 并解包 data', async () => {
    const { analyzeText } = await import('../api/client')
    const mock = axios as unknown as {
      post: any
      __setNextResponse: (r: any) => void
    }
    mock.__setNextResponse({ data: { code: 0, data: { ok: true } } })
    const result = await analyzeText({ raw_text: 'test' })
    expect(mock.post).toHaveBeenCalledWith('/analyze/text', { raw_text: 'test' })
    expect(result).toEqual({ ok: true })
  })

  it('submitFeedback 调用 /feedback', async () => {
    const { submitFeedback } = await import('../api/client')
    const mock = axios as unknown as {
      post: any
      __setNextResponse: (r: any) => void
    }
    mock.__setNextResponse({ data: { code: 0, data: { ok: true } } })
    await submitFeedback({
      analysis_id: 'a1',
      reply_index: 0,
      useful: true,
    })
    expect(mock.post).toHaveBeenCalledWith('/feedback', {
      analysis_id: 'a1',
      reply_index: 0,
      useful: true,
    })
  })

  it('analyzeImage 用 FormData', async () => {
    const { analyzeImage } = await import('../api/client')
    const mock = axios as unknown as {
      post: any
      __setNextResponse: (r: any) => void
    }
    mock.__setNextResponse({ data: { code: 0, data: { ok: true } } })
    const f = new File(['x'], 'a.png', { type: 'image/png' })
    await analyzeImage([f])
    expect(mock.post).toHaveBeenCalledWith(
      '/analyze/image',
      expect.any(FormData),
      expect.objectContaining({
        headers: expect.objectContaining({ 'Content-Type': 'multipart/form-data' }),
      }),
    )
  })

  it('响应 code != 0 抛出错误', async () => {
    const { analyzeText } = await import('../api/client')
    const mock = axios as unknown as {
      post: any
      __setNextResponse: (r: any) => void
    }
    mock.__setNextResponse({
      data: { code: 1001, msg: 'param error', data: null },
    })
    await expect(analyzeText({ raw_text: '' })).rejects.toBeTruthy()
  })
})
