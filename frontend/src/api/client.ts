import axios, { type AxiosInstance, type AxiosError } from 'axios'

const baseURL = import.meta.env.VITE_API_BASE || '/api'

export const http: AxiosInstance = axios.create({
  baseURL,
  timeout: 60000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 响应拦截：解包 data
http.interceptors.response.use(
  (response) => {
    const body = response.data
    if (body && typeof body === 'object' && 'code' in body) {
      if (body.code === 0) {
        return body.data
      }
      const err: any = new Error(body.msg || '请求失败')
      err.code = body.code
      err.response = response
      return Promise.reject(err)
    }
    return body
  },
  (error: AxiosError) => {
    return Promise.reject(error)
  },
)

// API 类型
export interface AnalysisResult {
  analysis_id: string
  input_type: 'text' | 'image'
  messages: Array<{ time: string; sender: string; content: string }>
  relationship: { label: string; confidence: number; evidence?: string }
  stage: string
  emotion: { label: string; score: number }
  risk: Array<{ type: string; level: string; evidence?: string }>
  replies: Array<{
    style: 'high_eq' | 'humor' | 'formal' | 'flirty' | 'concise'
    content: string
    reason: string
    expected_reply: string[]
  }>
  health_report: {
    naturalness: number
    engagement: number
    silence_risk: number
    reply_quality: number
  }
  summary: string
  advice: string[]
  ocr_text?: string
}

export interface ApiResponse<T> {
  code: number
  msg: string
  data: T
  request_id?: string
}

export async function analyzeText(payload: {
  raw_text: string
  user_role?: string
  extra_context?: string
}): Promise<AnalysisResult> {
  return http.post('/analyze/text', payload)
}

export async function analyzeImage(files: File[]): Promise<AnalysisResult> {
  const form = new FormData()
  files.forEach((f) => form.append('images', f))
  return http.post('/analyze/image', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
    timeout: 90000,
  })
}

export async function submitFeedback(payload: {
  analysis_id: string
  reply_index: number
  useful: boolean
  comment?: string
}): Promise<{ ok: true }> {
  return http.post('/feedback', payload)
}
