export type Priority = 'P1' | 'P2' | 'P3' | 'P4'
export type Level3 = 'High' | 'Medium' | 'Low'

export interface Classification {
  category: string
  priority: Priority
  impact: Level3
  urgency: Level3
  level: 'L1' | 'L2'
  sentiment: 'positive' | 'neutral' | 'frustrated' | 'angry'
  confidence: number
  language: 'en' | 'es'
  summary: string
  priority_reason: string
  is_support_request: boolean
  injection_detected: boolean
}

export interface ArticleRef {
  id: string
  title: string
  category: string
  level: string
  url: string
  score: number
  section: string
  cited: boolean
}

export interface TriageResponse {
  mode: 'live' | 'demo'
  demo_reason: 'no_api_key' | 'rate_limited' | 'daily_budget' | 'llm_error' | null
  notice: string | null
  classification: Classification | null
  articles: ArticleRef[]
  reply: string | null
  usage: { prompt_tokens: number; completion_tokens: number; total_tokens: number } | null
  latency_ms: number
  model: string | null
  prompt_version: string
  flags: string[]
}

export interface Sample {
  id: string
  title: string
  language: 'en' | 'es'
  text: string
}

export interface Health {
  status: string
  version: string
  llm_enabled: boolean
  model: string | null
  prompt_version: string
  kb_articles: number
  demo_results: number
  rate_limit: { requests: number; window_seconds: number }
  max_ticket_chars: number
}

export interface Matrix {
  labels: string[]
  matrix: number[][]
}

export interface EvalFailure {
  id: string
  language: string
  text: string
  expected: { category: string; priority: Priority; impact: Level3; urgency: Level3 }
  predicted: {
    category: string
    priority: Priority
    impact: Level3
    urgency: Level3
    confidence: number
  }
  priority_reason: string
  wrong: string[]
}

export interface EvalResults {
  generated_at: string
  mode: 'full' | 'retrieval_only'
  model: string | null
  prompt_version: string
  dataset: {
    tickets: number
    by_language: Record<string, number>
    by_category: Record<string, number>
    by_priority: Record<string, number>
  }
  retrieval: {
    labeled_tickets: number
    hit_rate_at_1: number
    hit_rate_at_3: number
    mrr_at_3: number
    hit_rate_at_3_by_language: Record<string, { hits: number; total: number; rate: number }>
    misses: { id: string; expected: string; retrieved: string[] }[]
    baseline_category_accuracy: number
    without_glossary: {
      hit_rate_at_1: number
      hit_rate_at_3: number
      hit_rate_at_3_by_language: Record<string, { hits: number; total: number; rate: number }>
    }
  }
  classification?: {
    evaluated: number
    errors: { id: string; error: string }[]
    category_accuracy: number
    priority_accuracy: number
    priority_within_one_accuracy: number
    level_accuracy: number
    language_accuracy: number
    citation_accuracy: number
    json_retries: number
    category_confusion: Matrix
    priority_confusion: Matrix
    latency_ms: { mean: number; p95: number }
    tokens: { total: number; mean_per_ticket: number }
    failures: EvalFailure[]
  }
  injection_cases?: {
    id: string
    name: string
    passed: boolean
    checks: Record<string, boolean>
    category: string
    priority: Priority
    reply: string
  }[]
}

const BASE = (import.meta.env.VITE_API_URL ?? '').replace(/\/$/, '')

export class ApiError extends Error {
  status: number
  constructor(message: string, status: number) {
    super(message)
    this.status = status
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let res: Response
  try {
    // Only send Content-Type with a body: simple GETs then skip the CORS preflight.
    const headers = init?.body ? { 'Content-Type': 'application/json' } : undefined
    res = await fetch(`${BASE}${path}`, { ...init, headers })
  } catch {
    throw new ApiError('Cannot reach the API. The server may be waking up, try again.', 0)
  }
  if (!res.ok) {
    let detail = `Request failed (${res.status})`
    try {
      const body = await res.json()
      if (typeof body.detail === 'string') detail = body.detail
      else if (Array.isArray(body.detail) && body.detail[0]?.msg) detail = body.detail[0].msg
    } catch {
      /* keep the generic message */
    }
    throw new ApiError(detail, res.status)
  }
  return res.json() as Promise<T>
}

export const api = {
  health: () => request<Health>('/api/health'),
  samples: () => request<Sample[]>('/api/samples'),
  triage: (text: string) =>
    request<TriageResponse>('/api/triage', { method: 'POST', body: JSON.stringify({ text }) }),
  evaluation: () => request<EvalResults>('/api/eval'),
}
