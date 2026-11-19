import Mermaid from '../components/Mermaid'
import { usePageTitle } from '../lib/usePageTitle'
import type { Health } from '../lib/api'

const ARCHITECTURE = `flowchart LR
  A([Support agent]) --> W[React app<br/>Vercel]
  W -->|POST /api/triage| G{Cost guard}
  G -->|no key or<br/>limit reached| D[Demo mode<br/>precomputed results]
  G -->|allowed| R[BM25 retriever<br/>top 3 sections]
  KB[(helpdesk-kb<br/>21 articles)] -.-> R
  R --> L[LLM call<br/>prompt v1, JSON mode]
  L --> V[Pydantic validation<br/>priority = impact x urgency]
  V -->|classification<br/>articles, reply| W
  D --> W`

const DECISIONS = [
  {
    title: 'BM25 instead of embeddings',
    body: '21 short, well-structured articles with distinctive vocabulary (VPN, BitLocker, OneDrive). BM25 is free, deterministic, has no extra service to pay or host, and reached a high hit@3 in the evaluation. The Retriever interface lets embeddings replace it later.',
  },
  {
    title: 'One LLM call with validated JSON',
    body: 'Classification and reply come from a single JSON-mode call, validated with Pydantic. Invalid JSON gets one retry with the validation error; after that the API falls back to demo mode instead of showing broken data.',
  },
  {
    title: 'The model judges, the code decides the priority',
    body: 'The model estimates impact and urgency; priority is computed from the documented matrix. Lookup tables are something code does perfectly and LLMs do inconsistently.',
  },
  {
    title: 'Demo mode as a first-class path',
    body: 'No key, hourly limit, daily budget or provider error all lead to the same graceful path: precomputed real results for the samples, or the KB search for anything else. The demo never breaks and costs stay bounded.',
  },
  {
    title: 'Evaluation before claims',
    body: 'A labeled dataset and a script produce the metrics shown on the Evaluation page, including failures. It already caught a real retrieval bug.',
  },
]

const LIMITATIONS = [
  'BM25 matches words, not meaning: a ticket that describes a problem with unusual vocabulary can miss its article. Spanish tickets rely on a small hand-written glossary.',
  'Rate limit and budget live in process memory: they reset on restart and do not work across several instances.',
  'The client IP comes from X-Forwarded-For, which can be spoofed; the global daily budget is the hard cost cap.',
  'The evaluation set is small (50 tickets) and written by the author of the prompt.',
  'No authentication, no persistence and no feedback loop: suggestions are not stored or learned from.',
]

const NEXT = [
  'Embeddings retriever (or hybrid BM25 + embeddings) behind the same Retriever interface, compared on the same dataset.',
  'Agent feedback: thumbs up/down and edits to the draft stored and added to the evaluation set.',
  'Zendesk or Freshdesk integration through a webhook: triage new tickets automatically and post the draft as an internal note.',
  'Redis-backed rate limiting and structured logs to a log service.',
  'A larger evaluation set built from anonymized real tickets, with a second labeler to measure agreement.',
]

export default function AboutPage({ health }: { health: Health | null }) {
  usePageTitle('About')
  return (
    <div className="space-y-8">
      <header className="max-w-3xl">
        <p className="eyebrow">About</p>
        <h1 className="mt-1 text-3xl font-semibold tracking-tight">How TriageAI works</h1>
        <p className="mt-2 text-ink-2">
          A portfolio project that shows LLM integration, prompt engineering, retrieval-augmented
          generation and AI evaluation applied to IT support. The knowledge base is{' '}
          <a
            className="text-accent-ink underline"
            href="https://lucaswsanchez.github.io/helpdesk-kb/"
          >
            helpdesk-kb
          </a>
          , a separate project with {health?.kb_articles ?? 21} articles for a fictional company.
        </p>
      </header>

      <section className="card p-5">
        <h2 className="font-semibold">Architecture</h2>
        <div className="mt-4">
          <Mermaid
            chart={ARCHITECTURE}
            title="TriageAI architecture: React frontend, FastAPI backend, BM25 retriever and LLM provider"
          />
        </div>
      </section>

      <section>
        <h2 className="mb-3 font-semibold">Technical decisions</h2>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {DECISIONS.map((d) => (
            <article key={d.title} className="card p-4">
              <h3 className="font-medium">{d.title}</h3>
              <p className="mt-1.5 text-sm leading-relaxed text-ink-2">{d.body}</p>
            </article>
          ))}
        </div>
      </section>

      <div className="grid gap-4 md:grid-cols-2">
        <section className="card p-5">
          <h2 className="font-semibold">Limitations</h2>
          <ul className="mt-3 list-disc space-y-2 pl-5 text-sm text-ink-2">
            {LIMITATIONS.map((l) => (
              <li key={l}>{l}</li>
            ))}
          </ul>
        </section>
        <section className="card p-5">
          <h2 className="font-semibold">Next steps</h2>
          <ul className="mt-3 list-disc space-y-2 pl-5 text-sm text-ink-2">
            {NEXT.map((l) => (
              <li key={l}>{l}</li>
            ))}
          </ul>
        </section>
      </div>

      <section className="card p-5 text-sm text-ink-2">
        <h2 className="font-semibold text-ink">Stack</h2>
        <p className="mt-2">
          Python 3.12 · FastAPI · Pydantic · rank_bm25 · OpenAI SDK (DeepSeek
          {health?.model ? `, ${health.model}` : ''}) · pytest · React · Vite · TypeScript ·
          Tailwind CSS · Mermaid · GitHub Actions · Render · Vercel
        </p>
        <p className="mt-3">
          Source and documentation:{' '}
          <a
            className="text-accent-ink underline"
            href="https://github.com/lucaswsanchez/triage-ai"
          >
            github.com/lucaswsanchez/triage-ai
          </a>{' '}
          · API docs at <code className="font-mono">/docs</code> on the backend.
        </p>
      </section>
    </div>
  )
}
