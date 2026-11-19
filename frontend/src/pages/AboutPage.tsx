import type { Health } from '../lib/api'

export default function AboutPage({ health }: { health: Health | null }) {
  return <p>TriageAI {health?.version}</p>
}
