import { describe, expect, it } from 'vitest'
import { formatMs, percent, splitCitations } from './format'

describe('format helpers', () => {
  it('formats percentages and missing values', () => {
    expect(percent(0.913)).toBe('91%')
    expect(percent(0.9134, 1)).toBe('91.3%')
    expect(percent(null)).toBe('–')
  })

  it('formats latency', () => {
    expect(formatMs(850)).toBe('850 ms')
    expect(formatMs(2340)).toBe('2.3 s')
  })

  it('splits KB citations out of a reply', () => {
    expect(splitCitations('Restart the VPN [KB-009] and retry.')).toEqual([
      { text: 'Restart the VPN ', citation: false },
      { text: '[KB-009]', citation: true },
      { text: ' and retry.', citation: false },
    ])
  })
})
