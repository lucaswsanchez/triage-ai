export function percent(value: number | null | undefined, digits = 0): string {
  if (value === null || value === undefined || Number.isNaN(value)) return '–'
  return `${(value * 100).toFixed(digits)}%`
}

export function formatMs(ms: number): string {
  return ms < 1000 ? `${ms} ms` : `${(ms / 1000).toFixed(1)} s`
}

export function formatNumber(n: number): string {
  return new Intl.NumberFormat('en-US').format(n)
}

/** Split a reply into text and [KB-000] citation parts, for highlighting. */
export function splitCitations(text: string): { text: string; citation: boolean }[] {
  return text
    .split(/(\[KB-\d{3}\])/g)
    .filter(Boolean)
    .map((part) => ({ text: part, citation: /^\[KB-\d{3}\]$/.test(part) }))
}

export const DEMO_REASON_LABEL: Record<string, string> = {
  no_api_key: 'No API key on the server',
  rate_limited: 'Hourly limit reached',
  daily_budget: 'Daily budget spent',
  llm_error: 'AI provider error',
}
