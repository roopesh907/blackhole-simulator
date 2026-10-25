
export default function SimulationStats({ result }) {
  const items = [
    {
      label: 'TRAJECTORY STATUS',
      value: result?.status ?? 'Awaiting simulation',
    },
    {
      label: 'INTEGRATION STEPS',
      value: result?.steps_taken?.toLocaleString() ?? '—',
    },
    {
      label: 'CLOSEST APPROACH',
      value: result ? `${result.closest_approach.toFixed(3)} M` : '—',
    },
    {
      label: 'FINAL RADIUS',
      value: result ? `${result.final_radius.toFixed(3)} M` : '—',
    },
  ]

  return (
    <section className="grid grid-cols-2 gap-3">
      {items.map((item) => (
        <div
          key={item.label}
          className="rounded-xl border border-white/10 bg-white/[0.03] p-4"
        >
          <p className="text-[10px] font-semibold tracking-[0.15em] text-slate-500">
            {item.label}
          </p>

          <p className="mt-2 break-words font-mono text-lg text-cyan-200">
            {item.value}
          </p>
        </div>
      ))}
    </section>
  )
}
