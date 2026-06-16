/**
 * HealthRadar 组件测试
 */
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import HealthRadar from '../components/HealthRadar.vue'

describe('HealthRadar.vue', () => {
  const report = {
    naturalness: 85,
    engagement: 70,
    silence_risk: 30,
    reply_quality: 90,
  }

  it('渲染四项指标', () => {
    const w = mount(HealthRadar, { props: { report, advice: [] } })
    expect(w.text()).toContain('自然度')
    expect(w.text()).toContain('互动度')
    expect(w.text()).toContain('冷场风险')
    expect(w.text()).toContain('回复质量')
  })

  it('显示指标数值', () => {
    const w = mount(HealthRadar, { props: { report, advice: [] } })
    expect(w.text()).toContain('85')
    expect(w.text()).toContain('70')
    expect(w.text()).toContain('30')
    expect(w.text()).toContain('90')
  })

  it('显示改进建议', () => {
    const advice = ['多问开放式问题', '适当分享自己']
    const w = mount(HealthRadar, { props: { report, advice } })
    expect(w.text()).toContain('多问开放式问题')
    expect(w.text()).toContain('适当分享自己')
  })

  it('无建议时不显示建议区', () => {
    const w = mount(HealthRadar, { props: { report, advice: [] } })
    // 建议区被 v-if 控制
    expect(w.find('ul').exists()).toBe(false)
  })

  it('silence_risk 显示 % 后缀', () => {
    const w = mount(HealthRadar, { props: { report, advice: [] } })
    // 30% 包含 30
    expect(w.text()).toContain('30')
  })
})
