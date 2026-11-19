import { Link } from 'react-router-dom'
import { usePageTitle } from '../lib/usePageTitle'

export default function NotFoundPage() {
  usePageTitle('Page not found')
  return (
    <div className="mx-auto max-w-lg py-16 text-center">
      <p className="font-mono text-sm text-muted">404</p>
      <h1 className="mt-2 text-3xl font-semibold tracking-tight">This page does not exist</h1>
      <p className="mt-3 text-ink-2">
        The link may be old or mistyped. The triage assistant is one click away.
      </p>
      <Link
        to="/"
        className="mt-6 inline-block rounded-xl bg-accent px-5 py-2.5 font-medium text-white hover:bg-accent-ink"
      >
        Go to Triage
      </Link>
    </div>
  )
}
