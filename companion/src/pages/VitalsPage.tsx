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
  const initialSleepHours = existing?.sleepHours ?? 7
  const initialMorningPain = existing?.morningPain ?? 3
  const initialMorningEnergy = existing?.morningEnergy ?? 5
  const initialAutonomicState = existing?.autonomicState ?? 'Calm'

  const [sleepHours, setSleepHours] = useState(initialSleepHours)
  const [sleepQuality, setSleepQuality] = useState(existing?.sleepQuality ?? 3)
  const [morningPain, setMorningPain] = useState(initialMorningPain)
  const [morningEnergy, setMorningEnergy] = useState(initialMorningEnergy)
  const [autonomicState, setAutonomicState] = useState<AutonomicState>(initialAutonomicState)
  const [tier, setTier] = useState<Tier>(
    existing?.tier ??
    suggestTier({
      morningPain: initialMorningPain,
      morningEnergy: initialMorningEnergy,
      sleepHours: initialSleepHours,
      autonomicState: initialAutonomicState,
    }) ??
    'green',
  )
  const [notable, setNotable] = useState(existing?.notable ?? '')
  const [tierOverridden, setTierOverridden] = useState(false)

  const suggested = suggestTier({ morningPain, morningEnergy, sleepHours, autonomicState })

  const handleFieldChange = (updatedVitals: {
    sleepHours?: number
    morningPain?: number
    morningEnergy?: number
    autonomicState?: AutonomicState
  }) => {
    const nextSuggested = suggestTier({
      morningPain,
      morningEnergy,
      sleepHours,
      autonomicState,
      ...updatedVitals,
    })
    if (!tierOverridden && nextSuggested) {
      setTier(nextSuggested)
    }
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    addVitals({
      date: today,
      tier: !tierOverridden && suggested ? suggested : tier,
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
            const nextSleepHours = Number(e.target.value)
            setSleepHours(nextSleepHours)
            handleFieldChange({ sleepHours: nextSleepHours })
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
              const nextMorningPain = Number(e.target.value)
              setMorningPain(nextMorningPain)
              handleFieldChange({ morningPain: nextMorningPain })
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
              const nextMorningEnergy = Number(e.target.value)
              setMorningEnergy(nextMorningEnergy)
              handleFieldChange({ morningEnergy: nextMorningEnergy })
            }}
            className="w-full accent-accent"
          />
          <span className="text-lg tabular-nums">{morningEnergy}/10</span>
        </label>

        <Select
          label="Autonomic state"
          value={autonomicState}
          onChange={(e) => {
            const nextAutonomicState = e.target.value as AutonomicState
            setAutonomicState(nextAutonomicState)
            handleFieldChange({ autonomicState: nextAutonomicState })
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
