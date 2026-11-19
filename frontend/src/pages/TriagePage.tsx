import { useEffect, useId, useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import { ArrowIcon, ChipIcon, ClockIcon, FileIcon, TokensIcon } from '../components/icons'
import { ConfidenceMeter, ErrorBox, Field, Pill, PriorityBadge, Spinner } from '../components/ui'
import { usePageTitle } from '../lib/usePageTitle'
import { api, ApiError, type Health, type Sample, type TriageResponse } from '../lib/api'
import { DEMO_REASON_LABEL, formatMs, formatNumber } from '../lib/format'

const SENTIMENT: Record<string, { label: string; dot: string }> = {
  positive: { label: 'Positive', dot: 'bg-accent' },
  neutral: { label: 'Neutral', dot: 'bg-p4' },
  frustrated: { label: 'Frustrated', dot: 'bg-p3' },
  angry: { label: 'Angry', dot: 'bg-p1' },
}

const STEPS = [
  {
    title: 'Classify',
    body: 'Category, impact × urgency, priority P1–P4, L1/L2 level and sentiment, as validated JSON.',
  },
  {
    title: 'Retrieve',
    body: 'BM25 finds the 3 most relevant sections in the 21-article help desk knowledge base.',
  },
  {
    title: 'Draft',
    body: 'A reply in the language of the ticket that cites the articles it used. You review it.',
  },
]

function Samples({
  samples,
  onPick,
  disabled,
}: {
  samples: Sample[] | null
  onPick: (s: Sample) => void
  disabled: boolean
}) {
  if (!samples)
    return (
      <div className="flex flex-wrap gap-2" aria-hidden="true">
        {Array.from({ length: 6 }).map((_, i) => (
          <div key={i} className="skeleton h-8 w-36" />
        ))}
      </div>
    )
  return (
    <div className="flex flex-wrap gap-2">
      {samples.map((s) => (
        <button
          key={s.id}
          type="button"
          disabled={disabled}
          onClick={() => onPick(s)}
          className="rounded-full border border-line bg-card px-3 py-1.5 text-sm text-ink-2 transition hover:border-accent hover:text-accent-ink disabled:opacity-50"
        >
          <span className="mr-1.5 rounded bg-paper px-1 font-mono text-[0.7rem] uppercase text-muted">
            {s.language}
          </span>
          {s.title}
        </button>
      ))}
    </div>
  )
}

function ReplyEditor({ initial, language }: { initial: string; language: string }) {
  const [text, setText] = useState(initial)
  const [copied, setCopied] = useState(false)
  const id = useId()

  const copy = async () => {
    try {
      await navigator.clipboard.writeText(text)
      setCopied(true)
      setTimeout(() => setCopied(false), 1800)
    } catch {
      setCopied(false)
    }
  }

  return (
    <section className="card p-5" aria-labelledby={`${id}-title`}>
      <div className="mb-3 flex flex-wrap items-center justify-between gap-2">
        <h2 id={`${id}-title`} className="font-semibold">
          Suggested reply{' '}
          <span className="ml-1 text-sm font-normal text-muted">
            ({language === 'es' ? 'Spanish' : 'English'}, editable)
          </span>
        </h2>
        <div className="flex gap-2">
          {text !== initial && (
            <button
              type="button"
              onClick={() => setText(initial)}
              className="rounded-lg px-3 py-1.5 text-sm text-muted hover:bg-paper"
            >
              Reset
            </button>
          )}
          <button
            type="button"
            onClick={copy}
            className="rounded-lg bg-ink px-3 py-1.5 text-sm font-medium text-paper hover:bg-ink-2"
          >
            {copied ? 'Copied ✓' : 'Copy reply'}
          </button>
        </div>
      </div>
      <label htmlFor={id} className="sr-only">
        Suggested reply
      </label>
      <textarea
        id={id}
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={Math.min(16, Math.max(8, text.split('\n').length + 2))}
        className="w-full resize-y rounded-xl border border-line bg-paper/50 p-4 text-[0.95rem] leading-relaxed outline-none focus:border-accent focus:ring-2 focus:ring-accent/20"
      />
      <span className="sr-only" aria-live="polite">
        {copied ? 'Reply copied to clipboard' : ''}
      </span>
    </section>
  )
}

function Result({ result }: { result: TriageResponse }) {
  const c = result.classification
  return (
    <div className="space-y-5">
      {result.mode === 'demo' && (
        <div className="flex flex-wrap items-start gap-3 rounded-xl border border-demo/20 bg-demo-soft px-4 py-3 text-sm text-demo">
          <Pill tone="demo">Demo mode</Pill>
          <span>
            <strong>{result.demo_reason ? DEMO_REASON_LABEL[result.demo_reason] : ''}.</strong>{' '}
            {result.notice}
          </span>
        </div>
      )}
      {result.flags.includes('possible_prompt_injection') && (
        <div
          role="alert"
          className="rounded-xl border border-p1/25 bg-p1-soft px-4 py-3 text-sm text-p1"
        >
          <strong>Possible prompt injection.</strong> The ticket contains instructions aimed at the
          AI. They were treated as data and ignored. Review the ticket before replying.
        </div>
      )}

      {c ? (
        <section className="card p-5" aria-label="Classification">
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div className="min-w-0">
              <p className="eyebrow">Classification</p>
              <h2 className="mt-1 text-xl font-semibold tracking-tight">{c.category}</h2>
              <p className="mt-1 text-sm text-ink-2">{c.summary}</p>
            </div>
            <PriorityBadge priority={c.priority} large />
          </div>
          <dl className="mt-5 grid grid-cols-2 gap-x-6 gap-y-4 sm:grid-cols-4">
            <Field label="Impact × urgency">
              {c.impact} × {c.urgency}
            </Field>
            <Field label="Support level">{c.level}</Field>
            <Field label="Sentiment">
              <span className="inline-flex items-center gap-1.5">
                <span className={`h-2 w-2 rounded-full ${SENTIMENT[c.sentiment].dot}`} />
                {SENTIMENT[c.sentiment].label}
              </span>
            </Field>
            <Field label="Confidence">
              <ConfidenceMeter value={c.confidence} />
            </Field>
          </dl>
          <p className="mt-4 rounded-lg bg-paper px-3 py-2 text-sm text-ink-2">
            <span className="font-medium text-ink">Why this priority: </span>
            {c.priority_reason}
          </p>
          {!c.is_support_request && (
            <p className="mt-3 text-sm text-muted">
              Not an IT support request: the reply politely declines.
            </p>
          )}
        </section>
      ) : (
        <section className="card p-5 text-sm text-ink-2">
          <p className="eyebrow">Classification</p>
          <p className="mt-2">
            Not available without the live AI. The knowledge base search below runs on the server
            for every ticket.
          </p>
        </section>
      )}

      <section className="card p-5" aria-labelledby="kb-title">
        <h2 id="kb-title" className="font-semibold">
          Knowledge base articles
          <span className="ml-2 text-sm font-normal text-muted">
            BM25 top {result.articles.length}
          </span>
        </h2>
        {result.articles.length === 0 ? (
          <p className="mt-3 text-sm text-muted">
            No relevant article found. The ticket probably needs a human or is out of scope.
          </p>
        ) : (
          <ul className="mt-3 divide-y divide-line">
            {result.articles.map((a) => (
              <li key={a.id} className="flex flex-wrap items-center justify-between gap-2 py-3">
                <div className="min-w-0">
                  <a
                    href={a.url}
                    target="_blank"
                    rel="noreferrer"
                    className="font-medium text-accent-ink underline-offset-2 hover:underline"
                  >
                    <span className="font-mono text-sm">{a.id}</span> · {a.title} ↗
                  </a>
                  <p className="text-xs text-muted">
                    {a.category} · {a.level} · best match: {a.section}
                  </p>
                </div>
                <div className="flex items-center gap-2">
                  {a.cited && <Pill tone="accent">Cited in reply</Pill>}
                  <span className="font-mono text-xs text-muted" title="BM25 score">
                    {a.score.toFixed(1)}
                  </span>
                </div>
              </li>
            ))}
          </ul>
        )}
      </section>

      {result.reply && c && (
        <ReplyEditor key={result.reply} initial={result.reply} language={c.language} />
      )}

      <p className="flex flex-wrap gap-x-5 gap-y-1.5 text-xs text-muted">
        <span className="inline-flex items-center gap-1.5" title="Response time">
          <ClockIcon />
          {formatMs(result.latency_ms)}
          {result.mode === 'demo' && c ? ' (recorded run)' : ''}
        </span>
        {result.usage && (
          <span className="inline-flex items-center gap-1.5" title="Tokens used">
            <TokensIcon />
            {formatNumber(result.usage.total_tokens)} tokens (
            {formatNumber(result.usage.prompt_tokens)} in /{' '}
            {formatNumber(result.usage.completion_tokens)} out)
          </span>
        )}
        {result.model && (
          <span className="inline-flex items-center gap-1.5" title="Model">
            <ChipIcon />
            {result.model}
          </span>
        )}
        <span className="inline-flex items-center gap-1.5" title="Prompt version">
          <FileIcon />
          prompt {result.prompt_version}
        </span>
      </p>
    </div>
  )
}

function ResultSkeleton() {
  return (
    <div className="space-y-5" aria-hidden="true">
      <div className="card space-y-3 p-5">
        <div className="skeleton h-4 w-24" />
        <div className="skeleton h-6 w-56" />
        <div className="skeleton h-4 w-full" />
        <div className="grid grid-cols-4 gap-4 pt-2">
          {Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="skeleton h-9" />
          ))}
        </div>
      </div>
      <div className="card space-y-3 p-5">
        <div className="skeleton h-5 w-48" />
        <div className="skeleton h-10" />
        <div className="skeleton h-10" />
      </div>
    </div>
  )
}

export default function TriagePage({ health }: { health: Health | null }) {
  usePageTitle('Triage')
  const [samples, setSamples] = useState<Sample[] | null>(null)
  const [text, setText] = useState('')
  const [result, setResult] = useState<TriageResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const resultRef = useRef<HTMLDivElement>(null)
  const maxChars = health?.max_ticket_chars ?? 4000
  const tooShort = text.trim().length < 10
  const tooLong = text.length > maxChars

  useEffect(() => {
    api
      .samples()
      .then((list) => {
        setSamples(list)
        // Deep link: /?sample=<id> loads and triages a sample ticket.
        const wanted = new URLSearchParams(window.location.search).get('sample')
        const sample = list.find((s) => s.id === wanted)
        if (sample) {
          setText(sample.text)
          void run(sample.text)
        }
      })
      .catch(() => setSamples([]))
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const run = async (value = text) => {
    setLoading(true)
    setError(null)
    try {
      const res = await api.triage(value)
      setResult(res)
      requestAnimationFrame(() =>
        resultRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' }),
      )
    } catch (e) {
      setError(e instanceof ApiError ? e.message : 'Something went wrong.')
    } finally {
      setLoading(false)
    }
  }

  const pick = (s: Sample) => {
    setText(s.text)
    void run(s.text)
  }

  return (
    <div className="grid gap-8 lg:grid-cols-[minmax(0,5fr)_minmax(0,6fr)]">
      <section aria-labelledby="triage-title" className="lg:sticky lg:top-24 lg:self-start">
        <p className="eyebrow">AI help desk assistant</p>
        <h1 id="triage-title" className="mt-1 text-3xl font-semibold tracking-tight sm:text-4xl">
          Triage a ticket in seconds
        </h1>
        <p className="mt-3 text-ink-2">
          Paste a ticket or email. TriageAI classifies it (category, priority from impact × urgency,
          level, sentiment), finds the right knowledge base articles and drafts a cited reply for
          you to review.
        </p>

        <div className="mt-6">
          <p className="mb-2 text-sm font-medium">Try a sample ticket</p>
          <Samples samples={samples} onPick={pick} disabled={loading} />
        </div>

        <form
          className="mt-6"
          onSubmit={(e) => {
            e.preventDefault()
            if (!tooShort && !tooLong) void run()
          }}
        >
          <label htmlFor="ticket" className="mb-2 block text-sm font-medium">
            Ticket text
          </label>
          <textarea
            id="ticket"
            value={text}
            onChange={(e) => setText(e.target.value)}
            rows={7}
            placeholder="e.g. Since this morning Outlook says 'Disconnected' and I'm not receiving emails. Webmail works…"
            aria-describedby="ticket-help"
            className="w-full resize-y rounded-xl border border-line bg-card p-4 leading-relaxed shadow-sm outline-none placeholder:text-muted/70 focus:border-accent focus:ring-2 focus:ring-accent/20"
          />
          <div id="ticket-help" className="mt-1 flex justify-between text-xs text-muted">
            <span>English or Spanish. Do not paste real personal data.</span>
            <span className={tooLong ? 'font-semibold text-p1' : 'tabular-nums'}>
              {text.length} / {maxChars}
            </span>
          </div>
          <div className="mt-4 flex items-center gap-3">
            <button
              type="submit"
              disabled={loading || tooShort || tooLong}
              className="rounded-xl bg-accent px-5 py-2.5 font-medium text-white shadow-sm transition hover:bg-accent-ink disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading ? <Spinner label="Triaging…" /> : 'Triage ticket'}
            </button>
            {text && !loading && (
              <button
                type="button"
                onClick={() => {
                  setText('')
                  setResult(null)
                  setError(null)
                }}
                className="text-sm text-muted underline hover:text-ink"
              >
                Clear
              </button>
            )}
          </div>
          {health && (
            <p className="mt-3 text-xs text-muted">
              Live AI limit: {health.rate_limit.requests} tickets per hour per visitor. After that,
              samples use precomputed results.
            </p>
          )}
        </form>
      </section>

      <div ref={resultRef} className="scroll-mt-24" aria-live="polite" aria-busy={loading}>
        {error && <ErrorBox message={error} onRetry={() => void run()} />}
        {loading && <ResultSkeleton />}
        {!loading && result && <Result result={result} />}
        {!loading && !result && !error && (
          <div className="card flex h-full flex-col p-6 sm:p-8">
            <p className="eyebrow">How it works</p>
            <h2 className="mt-1 text-xl font-semibold tracking-tight">
              From raw ticket to a reviewed reply
            </h2>
            <ol className="mt-6 space-y-5">
              {STEPS.map((step, i) => (
                <li key={step.title} className="flex gap-4">
                  <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-accent-soft font-mono text-sm font-medium text-accent-ink">
                    {i + 1}
                  </span>
                  <div>
                    <p className="font-medium">{step.title}</p>
                    <p className="mt-0.5 text-sm leading-relaxed text-ink-2">{step.body}</p>
                  </div>
                </li>
              ))}
            </ol>
            <div className="flex flex-1 flex-col justify-center py-7">
              <figure
                className="rounded-xl border border-line bg-paper/60 p-4"
                aria-label="Example output"
              >
                <figcaption className="eyebrow">Example output</figcaption>
                <div className="mt-3 flex flex-wrap items-center justify-between gap-2">
                  <span className="font-semibold">Security</span>
                  <PriorityBadge priority="P2" />
                </div>
                <p className="mt-1 text-sm text-ink-2">
                  Credentials entered on a fake Microsoft page, MFA prompt approved.
                </p>
                <div className="mt-3 flex flex-wrap gap-2 text-xs">
                  <Pill>Low × High</Pill>
                  <Pill>L2</Pill>
                  <Pill tone="accent">KB-018 cited</Pill>
                  <Pill tone="accent">KB-001 cited</Pill>
                </div>
              </figure>
            </div>
            <div className="flex flex-wrap items-center justify-between gap-3 border-t border-line pt-5 text-sm">
              <span className="text-muted">Pick a sample ticket to see it in action.</span>
              <Link
                to="/evaluation"
                className="inline-flex items-center gap-1.5 font-medium text-accent-ink hover:underline"
              >
                See how accurate it is <ArrowIcon />
              </Link>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
