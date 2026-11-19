import { useEffect, useId, useState } from 'react'

export default function Mermaid({ chart, title }: { chart: string; title: string }) {
  const [svg, setSvg] = useState<string | null>(null)
  const [failed, setFailed] = useState(false)
  const id = useId().replace(/:/g, '')

  useEffect(() => {
    let cancelled = false
    import('mermaid')
      .then(async ({ default: mermaid }) => {
        mermaid.initialize({
          startOnLoad: false,
          theme: 'base',
          fontFamily: 'IBM Plex Sans, sans-serif',
          themeVariables: {
            primaryColor: '#e2f1ee',
            primaryBorderColor: '#0e6b62',
            primaryTextColor: '#17191f',
            lineColor: '#5f6573',
            secondaryColor: '#fdf1d8',
            tertiaryColor: '#ffffff',
          },
        })
        const { svg } = await mermaid.render(`m${id}`, chart)
        if (!cancelled) setSvg(svg)
      })
      .catch(() => !cancelled && setFailed(true))
    return () => {
      cancelled = true
    }
  }, [chart, id])

  if (failed) return <pre className="overflow-x-auto rounded-lg bg-paper p-4 text-xs">{chart}</pre>
  if (!svg) return <div className="skeleton h-72" aria-label={`Loading diagram: ${title}`} />
  return (
    <figure role="img" aria-label={title}>
      <div
        className="overflow-x-auto [&_svg]:mx-auto [&_svg]:max-w-none md:[&_svg]:max-w-full [&_svg]:min-w-[680px] md:[&_svg]:min-w-0"
        dangerouslySetInnerHTML={{ __html: svg }}
      />
      <figcaption className="mt-2 text-xs text-muted md:hidden">
        Swipe sideways to see the whole diagram.
      </figcaption>
    </figure>
  )
}
