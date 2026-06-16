/**
 * 工具函数 / 格式化测试
 */
import { describe, it, expect } from 'vitest'
import {
  relationshipEmoji,
  stageEmoji,
  emotionEmoji,
  riskColor,
  riskLabel,
  styleLabel,
  styleEmoji,
  formatTime,
} from '../utils/format'

describe('format utils', () => {
  describe('relationshipEmoji', () => {
    it('包含所有关系标签', () => {
      for (const k of ['同事', '老板', '客户', '女朋友', '男朋友', '家长', '朋友', '陌生人']) {
        expect(relationshipEmoji[k]).toBeTruthy()
      }
    })
  })

  describe('stageEmoji', () => {
    it('包含所有阶段', () => {
      for (const k of ['破冰', '热聊', '平稳', '冷场', '收尾']) {
        expect(stageEmoji[k]).toBeTruthy()
      }
    })
  })

  describe('emotionEmoji', () => {
    it('包含所有情绪', () => {
      for (const k of ['开心', '生气', '敷衍', '礼貌', '好奇', '无聊', '难过']) {
        expect(emotionEmoji[k]).toBeTruthy()
      }
    })
  })

  describe('riskColor', () => {
    it('low/mid/high 三档都有', () => {
      expect(riskColor.low).toContain('emerald')
      expect(riskColor.mid).toContain('amber')
      expect(riskColor.high).toContain('rose')
    })
  })

  describe('riskLabel', () => {
    it('包含已知 risk 类型', () => {
      expect(riskLabel.single_side_initiative).toBe('单方主动')
      expect(riskLabel.short_reply).toBe('回复敷衍')
    })
  })

  describe('styleLabel', () => {
    it('包含 5 种风格', () => {
      for (const k of ['high_eq', 'humor', 'formal', 'flirty', 'concise']) {
        expect(styleLabel[k]).toBeTruthy()
        expect(styleEmoji[k]).toBeTruthy()
      }
    })
  })

  describe('formatTime', () => {
    it('输出 YYYY-MM-DD HH:MM 格式', () => {
      const out = formatTime(new Date('2026-06-15 10:23:00').getTime())
      expect(out).toBe('2026-06-15 10:23')
    })

    it('小于 10 的数字补 0', () => {
      const out = formatTime(new Date('2026-01-05 09:05:00').getTime())
      expect(out).toBe('2026-01-05 09:05')
    })
  })
})
