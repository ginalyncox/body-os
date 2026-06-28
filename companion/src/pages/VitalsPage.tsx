import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAppData, todayISO, suggestTier } from '../hooks/useAppData'
import { Card, Button, Input, Select, Textarea, TierBadge, PageHeader } from '../components/ui'
import type { AutonomicState, Tier } from '../types'

const TIERS: Tier[] = ['green', 'yellow', 'red', 'black']
const AUTONOMIC: AutonomicState[] = ['Calm', 'Edgy', 'Activated', 'Hijacked']

export function VitalsPage() {
  const { data, addVitals } = useAppData()
  const navigate = useNavigate()
  const today = todayISO()
  const existing = data.vitals.find((v) => v.date === today)

  const [sleepHours, setSleepHours] = useState(existing?.sleepHours ?? 7)
  const [sleepQuality, setSleepQuality] = useState(existing?.sleepQuality ?? 3)
  const [morningPain, setMorningPain] = useState(existing?.morningPain ?? 3)
  const [morningEnergy, setMorningEnergy] = useState(existing?.morningEnergy ?? 5)
  const [autonomicState, setAutonomicState] = useState<AutonomicState>(existing?.autonomicState ?? 'Calm')
  const [tier, setTier] = useState<Tier>(existing?.tier ?? 'green')
  const [notable, setNotable] = useState(existing?.notable ?? '')
  const [tierOverridden, setTierOverridden] = useState(false)

  const suggested = suggestTier({ morningPain, morningEnergy, sleepHours, autonomicState })

  const handleFieldChange = () => {
    if (!tierOverridden && suggested) {
      setTier(suggested)
    }
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    addVitals({
      date: today,
      tier,
      sleepHours,
      sleepQuality,
      morningPain,
      morningEnergy,
      autonomicState,
      notable: notable || undefined,
    })
    navigate('/')
  }

  return (
    <div>
      <PageHeader
        title="Daily Vitals"
        subtitle={`${today} — 60 second morning baseline`}
      />

      <form onSubmit={handleSubmit} className="space-y-4">
        <Card>
          <div className="flex items-center justify-between mb-4">
            <span className="text-sm text-text-muted">Today's tier</span>
            <TierBadge tier={tier} size="lg" />
          </div>

          {suggested && suggested !== tier && !tierOverridden && (
            <p className="text-sm text-tier-yellow mb-3">
              Suggested: <button type="button" onClick={() => setTier(suggested)} className="underline">{suggested}</button>
            </p>
          )}

          <Select
            label="Tier"
            value={tier}
            onChange={(e) => {
              setTier(e.target.value as Tier)
              setTierOverridden(true)
            }}
          >
            {TIERS.map((t) => (
              <option key={t} value={t}>{t.charAt(0).toUpperCase() + t.slice(1)}</option>
            ))}
          </Select>
        </Card>

        <Input
          label="Sleep hours"
          type="number"
          min={0}
          max={14}
          step={0.5}
          value={sleepHours}
          onChange={(e) => {
            setSleepHours(Number(e.target.value))
            handleFieldChange()
          }}
          required
        />

        <Select
          label="Sleep quality (1–5)"
          value={sleepQuality}
          onChange={(e) => setSleepQuality(Number(e.target.value))}
        >
          {[1, 2, 3, 4, 5].map((n) => (
            <option key={n} value={n}>{n}</option>
          ))}
        </Select>

        <label className="block space-y-1.5">
          <span className="text-sm text-text-muted">Morning pain (1–10)</span>
          <input
            type="range"
            min={1}
            max={10}
            value={morningPain}
            onChange={(e) => {
              setMorningPain(Number(e.target.value))
              handleFieldChange()
            }}
            className="w-full accent-accent"
          />
          <span className="text-lg tabular-nums">{morningPain}/10</span>
        </label>

        <label className="block space-y-1.5">
          <span className="text-sm text-text-muted">Morning energy (1–10)</span>
          <input
            type="range"
            min={1}
            max={10}
            value={morningEnergy}
            onChange={(e) => {
              setMorningEnergy(Number(e.target.value))
              handleFieldChange()
            }}
            className="w-full accent-accent"
          />
          <span className="text-lg tabular-nums">{morningEnergy}/10</span>
        </label>

        <Select
          label="Autonomic state"
          value={autonomicState}
          onChange={(e) => {
            setAutonomicState(e.target.value as AutonomicState)
            handleFieldChange()
          }}
        >
          {AUTONOMIC.map((a) => (
            <option key={a} value={a}>{a}</option>
          ))}
        </Select>

        <Textarea
          label="Notable (one sentence max)"
          value={notable}
          onChange={(e) => setNotable(e.target.value)}
          rows={2}
          maxLength={200}
        />

        <Button type="submit" className="w-full">
          {existing ? 'Update today\'s vitals' : 'Log vitals'}
        </Button>
      </form>

      {data.vitals.length > 1 && (
        <section className="mt-8">
          <h2 className="text-sm font-medium text-text-muted uppercase tracking-wide mb-3">
            History
          </h2>
          <div className="space-y-2">
            {data.vitals.slice(0, 7).map((v) => (
              <Card key={v.id} className="py-3 flex justify-between items-center">
                <div>
                  <p className="text-sm font-medium">{v.date}</p>
                  <p className="text-xs text-text-muted">
                    Pain {v.morningPain} · Energy {v.morningEnergy} · {v.autonomicState}
                  </p>
                </div>
                <TierBadge tier={v.tier} size="sm" />
              </Card>
            ))}
          </div>
        </section>
      )}
    </div>
  )
}
