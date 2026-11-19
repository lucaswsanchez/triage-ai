import type { ReactNode } from 'react'
import type { Priority } from '../lib/api'

const PRIORITY_STYLE: Record<Priority, string> = {
  P1: 'bg-p1-soft text-p1 ring-p1/30',
  P2: 'bg-p2-soft text-p2 ring-p2/30',
  P3: 'bg-p3-soft text-p3 ring-p3/30',
  P4: 'bg-p4-soft text-p4 ring-p4/30',
}

const PRIORITY_LABEL: Record<Priority, string> = {
  P1: 'Critical',
  P2: 'High',
  P3: 'Medium',
  P4: 'Low',
}

export function PriorityBadge({
  priority,
  large = false,
}: {
  priority: Priority
  large?: boolean
}) {
  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full font-semibold ring-1 ring-inset ${PRIORITY_STYLE[priority]} ${
        large ? 'px-3 py-1 text-base' : 'px-2 py-0.5 text-xs'
      }`}
    >
      {priority}
      <span className="font-medium opacity-80">{PRIORITY_LABEL[priority]}</span>
    </span>
  )
}

export function Pill({
  children,
  tone = 'neutral',
}: {
  children: ReactNode
  tone?: 'neutral' | 'accent' | 'demo' | 'danger'
}) {
  const tones = {
    neutral: 'bg-p4-soft text-ink-2',
    accent: 'bg-accent-soft text-accent-ink',
    demo: 'bg-demo-soft text-demo',
    danger: 'bg-p1-soft text-p1',
  }
  return (
    <span
      className={`inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-xs font-medium ${tones[tone]}`}
    >
      {children}
    </span>
  )
}

export function Field({ label, children }: { label: string; children: ReactNode }) {
  return (
    <div>
      <dt className="eyebrow">{label}</dt>
      <dd className="mt-1 text-sm font-medium text-ink">{children}</dd>
    </div>
  )
}

export function Spinner({ label }: { label: string }) {
  return (
    <span role="status" className="inline-flex items-center gap-2">
      <svg className="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none" aria-hidden="true">
        <circle cx="12" cy="12" r="9" stroke="currentColor" strokeOpacity="0.25" strokeWidth="3" />
        <path
          d="M21 12a9 9 0 0 0-9-9"
          stroke="currentColor"
          strokeWidth="3"
          strokeLinecap="round"
        />
      </svg>
      <span>{label}</span>
    </span>
  )
}

export function ErrorBox({ message, onRetry }: { message: string; onRetry?: () => void }) {
  return (
    <div
      role="alert"
      className="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-p1/25 bg-p1-soft px-4 py-3 text-sm text-p1"
    >
      <span>{message}</span>
      {onRetry && (
        <button
          type="button"
          onClick={onRetry}
          className="rounded-lg bg-white px-3 py-1.5 font-medium text-p1 ring-1 ring-p1/30 hover:bg-p1-soft"
        >
          Try again
        </button>
      )}
    </div>
  )
}

export function ConfidenceMeter({ value }: { value: number }) {
  const pct = Math.round(value * 100)
  const tone = value >= 0.75 ? 'bg-accent' : value >= 0.5 ? 'bg-p3' : 'bg-p1'
  return (
    <div className="flex items-center gap-2">
      <div
        className="h-1.5 w-20 overflow-hidden rounded-full bg-line"
        role="meter"
        aria-valuemin={0}
        aria-valuemax={100}
        aria-valuenow={pct}
        aria-label="Model confidence"
      >
        <div className={`h-full ${tone}`} style={{ width: `${pct}%` }} />
      </div>
      <span className="tabular-nums">{pct}%</span>
    </div>
  )
}
