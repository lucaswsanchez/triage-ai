import type { Matrix } from '../lib/api'

const SHORT: Record<string, string> = {
  'Accounts & Identity': 'Accounts',
  'Microsoft 365': 'M365',
  Network: 'Network',
  'Hardware & Printing': 'Hardware',
  Software: 'Software',
  Security: 'Security',
  'Onboarding & Offboarding': 'On/Offboard',
  Other: 'Other',
}

export default function ConfusionMatrix({ data, caption }: { data: Matrix; caption: string }) {
  const max = Math.max(1, ...data.matrix.flat())
  const label = (l: string) => SHORT[l] ?? l
  return (
    <div className="overflow-x-auto">
      <table className="min-w-full border-separate border-spacing-1 text-xs">
        <caption className="mb-2 text-left text-sm text-muted">{caption}</caption>
        <thead>
          <tr>
            <th scope="col" className="p-1 text-left font-medium text-muted">
              Expected ↓ / Predicted →
            </th>
            {data.labels.map((l) => (
              <th key={l} scope="col" className="p-1 text-center font-medium text-ink-2" title={l}>
                {label(l)}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.matrix.map((row, i) => (
            <tr key={data.labels[i]}>
              <th
                scope="row"
                className="whitespace-nowrap p-1 pr-2 text-left font-medium text-ink-2"
                title={data.labels[i]}
              >
                {label(data.labels[i])}
              </th>
              {row.map((count, j) => {
                const diagonal = i === j
                const alpha = count === 0 ? 0 : 0.15 + 0.85 * (count / max)
                const bg =
                  count === 0
                    ? '#f6f5f1'
                    : diagonal
                      ? `rgba(14,107,98,${alpha})`
                      : `rgba(180,35,24,${alpha})`
                const dark = alpha > 0.55
                return (
                  <td
                    key={j}
                    className={`h-9 min-w-9 rounded-md text-center font-mono tabular-nums ${
                      dark ? 'text-white' : count === 0 ? 'text-muted/60' : 'text-ink'
                    }`}
                    style={{ background: bg }}
                    aria-label={`${data.labels[i]} predicted as ${data.labels[j]}: ${count}`}
                  >
                    {count}
                  </td>
                )
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
