import { useEffect, useState } from 'react'
import ConfusionMatrix from '../components/ConfusionMatrix'
import { ErrorBox, Pill, PriorityBadge } from '../components/ui'
import { usePageTitle } from '../lib/usePageTitle'
import { api, ApiError, type EvalResults } from '../lib/api'
import { formatMs, formatNumber, percent } from '../lib/format'
import { ERROR_ANALYSIS } from './evalNotes'

function Stat({ label, value, hint }: { label: string; value: string; hint?: string }) {
  return (
    <div className="card p-4">
      <p className="eyebrow">{label}</p>
      <p className="mt-1 text-3xl font-semibold tracking-tight tabular-nums">{value}</p>
      {hint && <p className="mt-1 text-xs text-muted">{hint}</p>}
    </div>
  )
}

function Section({
  title,
  children,
  subtitle,
}: {
  title: string
  subtitle?: string
  children: React.ReactNode
}) {
  return (
    <section className="card p-5">
      <h2 className="font-semibold">{title}</h2>
      {subtitle && <p className="mt-0.5 text-sm text-muted">{subtitle}</p>}
      <div className="mt-4">{children}</div>
    </section>
  )
}

export default function EvaluationPage() {
  usePageTitle('Evaluation')
  const [data, setData] = useState<EvalResults | null>(null)
  const [error, setError] = useState<string | null>(null)

  const fetchResults = () =>
    api
      .evaluation()
      .then(setData)
      .catch((e) => setError(e instanceof ApiError ? e.message : 'Could not load the evaluation.'))

  useEffect(() => {
    void fetchResults()
  }, [])

  const retry = () => {
    setError(null)
    void fetchResults()
  }

  if (error) return <ErrorBox message={error} onRetry={retry} />
  if (!data)
    return (
      <div className="space-y-4" aria-busy="true" aria-label="Loading evaluation">
        <div className="skeleton h-10 w-72" />
        <div className="grid gap-4 sm:grid-cols-4">
          {Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="skeleton h-28" />
          ))}
        </div>
        <div className="skeleton h-80" />
      </div>
    )

  const r = data.retrieval
  const c = data.classification
  const date = new Date(data.generated_at).toLocaleDateString('en-US', { dateStyle: 'medium' })

  return (
    <div className="space-y-8">
      <header>
        <p className="eyebrow">Evaluation</p>
        <h1 className="mt-1 text-3xl font-semibold tracking-tight">How good is it, really?</h1>
        <p className="mt-2 max-w-3xl text-ink-2">
          {data.dataset.tickets} hand-labeled tickets ({data.dataset.by_language.en ?? 0} English,{' '}
          {data.dataset.by_language.es ?? 0} Spanish) run through the real pipeline with{' '}
          <code className="font-mono text-sm">python -m eval.run</code>. These are the numbers that
          came out, including the failures.
        </p>
        <div className="mt-3 flex flex-wrap gap-2">
          <Pill>Run: {date}</Pill>
          {data.model && <Pill>Model: {data.model}</Pill>}
          <Pill>Prompt {data.prompt_version}</Pill>
          {data.mode === 'retrieval_only' && <Pill tone="demo">Retrieval-only run</Pill>}
        </div>
      </header>

      {!c && (
        <div className="rounded-xl border border-demo/20 bg-demo-soft px-4 py-3 text-sm text-demo">
          This run did not call the LLM, so only retrieval metrics are available. Classification
          metrics are published after a run with an API key.
        </div>
      )}

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {c && (
          <>
            <Stat
              label="Category accuracy"
              value={percent(c.category_accuracy)}
              hint={`${c.evaluated} tickets`}
            />
            <Stat
              label="Priority accuracy"
              value={percent(c.priority_accuracy)}
              hint={`${percent(c.priority_within_one_accuracy)} within one level`}
            />
          </>
        )}
        <Stat
          label="Retrieval hit@3"
          value={percent(r.hit_rate_at_3)}
          hint={`${r.labeled_tickets} tickets with a labeled article`}
        />
        <Stat
          label="Retrieval hit@1"
          value={percent(r.hit_rate_at_1)}
          hint={`MRR@3 ${r.mrr_at_3.toFixed(2)}`}
        />
        {!c && (
          <Stat
            label="Baseline category accuracy"
            value={percent(r.baseline_category_accuracy)}
            hint="Category of the top BM25 article, no LLM"
          />
        )}
      </div>

      {c && (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <Stat label="Level (L1/L2)" value={percent(c.level_accuracy)} />
          <Stat label="Reply language" value={percent(c.language_accuracy)} />
          <Stat label="Cited the right article" value={percent(c.citation_accuracy)} />
          <Stat
            label="Avg. latency / tokens"
            value={formatMs(c.latency_ms.mean)}
            hint={`p95 ${formatMs(c.latency_ms.p95)} · ${formatNumber(c.tokens.mean_per_ticket)} tokens per ticket`}
          />
        </div>
      )}

      {ERROR_ANALYSIS.length > 0 && (
        <Section title="Error analysis" subtitle="What the failures say about the system">
          <ul className="list-disc space-y-2 pl-5 text-sm leading-relaxed text-ink-2">
            {ERROR_ANALYSIS.map((line) => (
              <li key={line}>{line}</li>
            ))}
          </ul>
        </Section>
      )}

      {c && (
        <div className="grid gap-4 lg:grid-cols-[minmax(0,3fr)_minmax(0,2fr)]">
          <Section
            title="Category confusion matrix"
            subtitle="Green diagonal = correct, red = mistakes"
          >
            <ConfusionMatrix data={c.category_confusion} caption={`${c.evaluated} tickets`} />
          </Section>
          <Section
            title="Priority confusion matrix"
            subtitle="Priority = impact × urgency (computed in code)"
          >
            <ConfusionMatrix data={c.priority_confusion} caption={`${c.evaluated} tickets`} />
          </Section>
        </div>
      )}

      <Section title="Retrieval (BM25)" subtitle="Is the labeled KB article in the top results?">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="text-left text-muted">
              <tr className="border-b border-line">
                <th className="py-2 font-medium">Configuration</th>
                <th className="py-2 font-medium">hit@1</th>
                <th className="py-2 font-medium">hit@3</th>
                {Object.keys(r.hit_rate_at_3_by_language).map((lang) => (
                  <th key={lang} className="py-2 font-medium">
                    hit@3 {lang.toUpperCase()}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="tabular-nums">
              <tr className="border-b border-line">
                <td className="py-2">BM25 + Spanish glossary (used)</td>
                <td>{percent(r.hit_rate_at_1, 1)}</td>
                <td>{percent(r.hit_rate_at_3, 1)}</td>
                {Object.entries(r.hit_rate_at_3_by_language).map(([lang, v]) => (
                  <td key={lang}>
                    {percent(v.rate, 1)}{' '}
                    <span className="text-muted">
                      ({v.hits}/{v.total})
                    </span>
                  </td>
                ))}
              </tr>
              <tr>
                <td className="py-2">BM25 without glossary (ablation)</td>
                <td>{percent(r.without_glossary.hit_rate_at_1, 1)}</td>
                <td>{percent(r.without_glossary.hit_rate_at_3, 1)}</td>
                {Object.keys(r.hit_rate_at_3_by_language).map((lang) => {
                  const v = r.without_glossary.hit_rate_at_3_by_language[lang]
                  return (
                    <td key={lang}>
                      {percent(v?.rate, 1)}{' '}
                      <span className="text-muted">
                        ({v?.hits}/{v?.total})
                      </span>
                    </td>
                  )
                })}
              </tr>
            </tbody>
          </table>
        </div>
        <p className="mt-3 text-sm text-muted">
          Baseline: using the category of the top article as the classification gives{' '}
          {percent(r.baseline_category_accuracy)} category accuracy without any LLM.
          {r.misses.length === 0
            ? ' No ticket missed its article in the top 3.'
            : ` Misses: ${r.misses.map((m) => `${m.id} (expected ${m.expected})`).join(', ')}.`}
        </p>
      </Section>

      {c && (
        <Section
          title={`Failed examples (${c.failures.length})`}
          subtitle="Tickets where the category or the priority did not match the label"
        >
          {c.failures.length === 0 ? (
            <p className="text-sm text-muted">No failures in this run.</p>
          ) : (
            <ul className="divide-y divide-line">
              {c.failures.map((f) => (
                <li key={f.id} className="py-4">
                  <div className="flex flex-wrap items-center gap-2 text-sm">
                    <span className="font-mono font-medium">{f.id}</span>
                    <Pill>{f.language.toUpperCase()}</Pill>
                    {f.wrong.map((w) => (
                      <Pill key={w} tone="danger">
                        wrong {w}
                      </Pill>
                    ))}
                  </div>
                  <p className="mt-2 text-sm text-ink-2">“{f.text}”</p>
                  <div className="mt-3 grid gap-2 text-sm sm:grid-cols-2">
                    <div className="rounded-lg bg-paper px-3 py-2">
                      <p className="eyebrow">Expected</p>
                      <p className="mt-1 flex flex-wrap items-center gap-2">
                        {f.expected.category} <PriorityBadge priority={f.expected.priority} />
                        <span className="text-muted">
                          {f.expected.impact} × {f.expected.urgency}
                        </span>
                      </p>
                    </div>
                    <div className="rounded-lg bg-p1-soft/50 px-3 py-2">
                      <p className="eyebrow">Predicted</p>
                      <p className="mt-1 flex flex-wrap items-center gap-2">
                        {f.predicted.category} <PriorityBadge priority={f.predicted.priority} />
                        <span className="text-muted">
                          {f.predicted.impact} × {f.predicted.urgency} · conf.{' '}
                          {percent(f.predicted.confidence)}
                        </span>
                      </p>
                    </div>
                  </div>
                  <p className="mt-2 text-xs text-muted">Model's reason: {f.priority_reason}</p>
                </li>
              ))}
            </ul>
          )}
        </Section>
      )}

      {data.injection_cases && (
        <Section
          title="Prompt injection cases"
          subtitle="The 3 attacks documented in prompts/DECISIONS.md"
        >
          <ul className="space-y-3">
            {data.injection_cases.map((inj) => (
              <li key={inj.id} className="rounded-lg border border-line p-3 text-sm">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="font-mono font-medium">{inj.id}</span>
                  <span className="font-medium">{inj.name}</span>
                  <Pill tone={inj.passed ? 'accent' : 'danger'}>
                    {inj.passed ? 'passed' : 'failed'}
                  </Pill>
                </div>
                <p className="mt-1 text-muted">
                  {Object.entries(inj.checks)
                    .map(([k, ok]) => `${ok ? '✓' : '✗'} ${k.replaceAll('_', ' ')}`)
                    .join(' · ')}
                </p>
              </li>
            ))}
          </ul>
        </Section>
      )}

      <Section title="Caveats">
        <ul className="list-disc space-y-1.5 pl-5 text-sm text-ink-2">
          <li>
            The dataset is small and was written by the same person who wrote the prompt: treat it
            as a sanity check.
          </li>
          <li>
            A retrieval bug was found with this dataset and fixed (the Spanish glossary rewrote the
            English word “mail”), so it is no longer a pure hold-out set.
          </li>
          <li>
            Impact and urgency labels are judgement calls; “within one level” is reported for that
            reason.
          </li>
          <li>
            LLM outputs vary slightly between runs. Each run stores its date, model and prompt
            version.
          </li>
        </ul>
      </Section>
    </div>
  )
}
