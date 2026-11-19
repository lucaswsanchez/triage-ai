import { lazy, Suspense, useEffect, useState } from 'react'
import { BrowserRouter, NavLink, Route, Routes } from 'react-router-dom'
import { Pill, Spinner } from './components/ui'
import { api, type Health } from './lib/api'
import TriagePage from './pages/TriagePage'

const EvaluationPage = lazy(() => import('./pages/EvaluationPage'))
const AboutPage = lazy(() => import('./pages/AboutPage'))

const NAV = [
  { to: '/', label: 'Triage' },
  { to: '/evaluation', label: 'Evaluation' },
  { to: '/about', label: 'About' },
]

function Logo() {
  return (
    <svg viewBox="0 0 32 32" className="h-8 w-8" aria-hidden="true">
      <rect width="32" height="32" rx="8" fill="#17191f" />
      <path d="M9 11h14M9 16h9M9 21h5" stroke="#f6f5f1" strokeWidth="2.4" strokeLinecap="round" />
      <circle cx="22.5" cy="20.5" r="3.5" fill="#2bb3a3" />
    </svg>
  )
}

function StatusPill({ health, failed }: { health: Health | null; failed: boolean }) {
  if (failed) return <Pill tone="danger">API offline</Pill>
  if (!health)
    return (
      <span className="text-xs text-muted">
        <Spinner label="Waking up API" />
      </span>
    )
  return health.llm_enabled ? (
    <Pill tone="accent">● Live AI · {health.model}</Pill>
  ) : (
    <Pill tone="demo">● Demo mode</Pill>
  )
}

export default function App() {
  const [health, setHealth] = useState<Health | null>(null)
  const [healthFailed, setHealthFailed] = useState(false)

  useEffect(() => {
    // Also warms up the free-tier backend while the user reads the page.
    api
      .health()
      .then(setHealth)
      .catch(() => setHealthFailed(true))
  }, [])

  return (
    <BrowserRouter>
      <a
        href="#main"
        className="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:rounded focus:bg-white focus:px-3 focus:py-2"
      >
        Skip to content
      </a>
      <header className="border-b border-line bg-paper/90 backdrop-blur supports-[backdrop-filter]:bg-paper/70 sticky top-0 z-10">
        <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-3 px-4 py-3 sm:px-6">
          <NavLink to="/" className="flex items-center gap-2.5">
            <Logo />
            <span className="text-lg font-semibold tracking-tight">TriageAI</span>
          </NavLink>
          <nav aria-label="Main" className="order-3 flex w-full gap-1 sm:order-none sm:w-auto">
            {NAV.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                end
                className={({ isActive }) =>
                  `rounded-lg px-3 py-1.5 text-sm font-medium transition-colors ${
                    isActive ? 'bg-ink text-paper' : 'text-ink-2 hover:bg-line/60'
                  }`
                }
              >
                {item.label}
              </NavLink>
            ))}
          </nav>
          <StatusPill health={health} failed={healthFailed} />
        </div>
      </header>

      <main id="main" className="mx-auto max-w-6xl px-4 py-8 sm:px-6">
        <Suspense
          fallback={
            <div className="py-20 text-center text-muted">
              <Spinner label="Loading page" />
            </div>
          }
        >
          <Routes>
            <Route path="/" element={<TriagePage health={health} />} />
            <Route path="/evaluation" element={<EvaluationPage />} />
            <Route path="/about" element={<AboutPage health={health} />} />
            <Route path="*" element={<TriagePage health={health} />} />
          </Routes>
        </Suspense>
      </main>

      <footer className="border-t border-line">
        <div className="mx-auto flex max-w-6xl flex-wrap justify-between gap-2 px-4 py-6 text-sm text-muted sm:px-6">
          <span>
            Built by{' '}
            <a className="underline hover:text-ink" href="https://github.com/lucaswsanchez">
              Lucas Sanchez
            </a>{' '}
            · Portfolio project, fictional company data
          </span>
          <span className="flex gap-4">
            <a
              className="underline hover:text-ink"
              href="https://github.com/lucaswsanchez/triage-ai"
            >
              Source code
            </a>
            <a
              className="underline hover:text-ink"
              href="https://lucaswsanchez.github.io/helpdesk-kb/"
            >
              Knowledge base
            </a>
          </span>
        </div>
      </footer>
    </BrowserRouter>
  )
}
