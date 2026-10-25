
export default function PhotonControls({
  mass,
  setMass,
  impactParameter,
  setImpactParameter,
  onSimulate,
  loading,
}) {
  return (
    <section className="space-y-6 rounded-2xl border border-white/10 bg-white/[0.03] p-5">
      <div>
        <h2 className="text-sm font-semibold tracking-wide text-white">
          SIMULATION PARAMETERS
        </h2>
        <p className="mt-1 text-xs text-slate-500">
          Schwarzschild spacetime · Geometrized units
        </p>
      </div>

      <label className="block space-y-3">
        <div className="flex justify-between text-sm">
          <span className="text-slate-300">Black-hole mass</span>
          <span className="font-mono text-cyan-300">{mass.toFixed(1)} M</span>
        </div>

        <input
          type="range"
          min="0.5"
          max="3"
          step="0.1"
          value={mass}
          onChange={(event) => setMass(Number(event.target.value))}
          className="w-full accent-cyan-400"
        />
      </label>

      <label className="block space-y-3">
        <div className="flex justify-between text-sm">
          <span className="text-slate-300">Impact parameter</span>
          <span className="font-mono text-cyan-300">
            {impactParameter.toFixed(2)} M
          </span>
        </div>

        <input
          type="range"
          min="3"
          max="12"
          step="0.1"
          value={impactParameter}
          onChange={(event) =>
            setImpactParameter(Number(event.target.value))
          }
          className="w-full accent-cyan-400"
        />
      </label>

      <button
        onClick={onSimulate}
        disabled={loading}
        className="w-full rounded-xl bg-cyan-400 px-4 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-300 disabled:cursor-wait disabled:opacity-50"
      >
        {loading ? 'Calculating trajectory…' : 'Run simulation'}
      </button>
    </section>
  )
}
