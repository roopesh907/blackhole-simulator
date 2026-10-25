
import { useState } from 'react'
import BlackHoleScene from './components/BlackHoleScene'
import PhotonControls from './components/PhotonControls'
import SimulationStats from './components/SimulationStats'
import { simulatePhoton } from './lib/api'

export default function App() {
  const [mass, setMass] = useState(1)
  const [impactParameter, setImpactParameter] = useState(6)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleSimulate() {
    setLoading(true)
    setError('')

    try {
      const data = await simulatePhoton({
        black_hole_mass: mass,
        impact_parameter: impactParameter,
        initial_radius: 20 * mass,
        radial_direction: 'inward',
        initial_phi: 0,
        step_size: 0.005,
        max_steps: 100000,
        escape_radius: 100 * mass,
        max_output_points: 2000,
      })

      setResult(data)
    } catch (err) {
      setError(err.message || 'An unexpected error occurred.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen bg-[#05070d] px-4 py-6 text-slate-100 sm:px-6 lg:px-10">
      <header className="mx-auto mb-8 flex max-w-[1600px] items-center justify-between gap-4">
        <div>
          <p className="text-xs font-semibold tracking-[0.3em] text-cyan-400">
            COMPUTATIONAL ASTROPHYSICS
          </p>
          <h1 className="mt-2 text-2xl font-semibold tracking-tight sm:text-3xl">
            Schwarzschild Photon Lab
          </h1>
          <p className="mt-2 text-sm text-slate-400">
            Explore light trajectories in curved spacetime.
          </p>
        </div>

        <div className="hidden rounded-full border border-emerald-400/20 bg-emerald-400/5 px-4 py-2 text-xs text-emerald-300 sm:block">
          <span className="mr-2 inline-block h-2 w-2 rounded-full bg-emerald-400" />
          Numerical engine
        </div>
      </header>

      <div className="mx-auto grid max-w-[1600px] gap-5 lg:grid-cols-[minmax(0,1fr)_340px]">
        <section className="min-h-[420px] lg:h-[650px]">
          <BlackHoleScene points={result?.points ?? []} />
        </section>

        <aside className="space-y-5">
          <PhotonControls
            mass={mass}
            setMass={setMass}
            impactParameter={impactParameter}
            setImpactParameter={setImpactParameter}
            onSimulate={handleSimulate}
            loading={loading}
          />

          <SimulationStats result={result} />

          {error && (
            <div
              role="alert"
              className="rounded-xl border border-red-400/20 bg-red-400/5 p-4 text-sm text-red-300"
            >
              {error}
            </div>
          )}
        </aside>
      </div>

      <footer className="mx-auto mt-8 max-w-[1600px] border-t border-white/10 pt-4 text-xs text-slate-500">
        Schwarzschild metric · Null geodesics · Classical RK4 integration
      </footer>
    </main>
  )
}
