import { useState } from 'react'
import { useAppData } from '../hooks/useAppData'
import {
  Card, Button, Input, Select, Textarea, SeverityBar, PageHeader,
} from '../components/ui'
import {
  PRIMARY_SYMPTOMS, BODY_REGIONS, SUSPECTED_TRIGGERS, SCRIPTS,
} from '../data/content'
import type { PrimarySymptom, BodyRegion, SuspectedTrigger, ScriptId } from '../types'

export function FlarePage() {
  const { data, addFlare } = useAppData()
  const [submitted, setSubmitted] = useState(false)

  const [summary, setSummary] = useState('')
  const [severity, setSeverity] = useState(5)
  const [primarySymptom, setPrimarySymptom] = useState<PrimarySymptom>('Pain')
  const [bodyRegions, setBodyRegions] = useState<BodyRegion[]>([])
  const [suspectedTriggers, setSuspectedTriggers] = useState<SuspectedTrigger[]>([])
  const [doingWhat, setDoingWhat] = useState('')
  const [scriptRun, setScriptRun] = useState<ScriptId>('none')
  const [notes, setNotes] = useState('')

  const toggleMulti = <T extends string>(list: T[], item: T, setter: (v: T[]) => void) => {
    if (list.includes(item)) setter(list.filter((x) => x !== item))
    else setter([...list, item])
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    addFlare({
      summary: summary || `${primarySymptom} flare`,
      time: new Date().toISOString(),
      severity,
      primarySymptom,
      bodyRegions,
      suspectedTriggers: suspectedTriggers.length ? suspectedTriggers : ['Unknown'],
      doingWhat: doingWhat || undefined,
      scriptRun,
      notes: notes || undefined,
    })
    setSubmitted(true)
    setSummary('')
    setSeverity(5)
    setDoingWhat('')
    setNotes('')
    setBodyRegions([])
    setSuspectedTriggers([])
    setScriptRun('none')
    setTimeout(() => setSubmitted(false), 3000)
  }

  const needsLog = severity >= 4

  return (
    <div>
      <PageHeader
        title="Flare Log"
        subtitle="Log first, analyze later. ≥ 4 severity required; ≥ 6 non-negotiable."
      />

      {submitted && (
        <Card className="mb-4 border-tier-green/40 text-tier-green text-sm">
          Flare logged. You did the right thing.
        </Card>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <Card>
          <label className="block space-y-2">
            <span className="text-sm text-text-muted">Severity (1–10)</span>
            <input
              type="range"
              min={1}
              max={10}
              value={severity}
              onChange={(e) => setSeverity(Number(e.target.value))}
              className="w-full accent-accent"
            />
            <SeverityBar value={severity} />
          </label>
          {severity >= 6 && (
            <p className="text-xs text-tier-red mt-2">≥ 6 — log is mandatory</p>
          )}
          {!needsLog && (
            <p className="text-xs text-text-muted mt-2">Below logging threshold (≥ 4)</p>
          )}
        </Card>

        <Input
          label="Summary (one line)"
          value={summary}
          onChange={(e) => setSummary(e.target.value)}
          placeholder="e.g. Burning hands after standing"
        />

        <Select
          label="Primary symptom"
          value={primarySymptom}
          onChange={(e) => setPrimarySymptom(e.target.value as PrimarySymptom)}
        >
          {PRIMARY_SYMPTOMS.map((s) => (
            <option key={s} value={s}>{s}</option>
          ))}
        </Select>

        <fieldset>
          <legend className="text-sm text-text-muted mb-2">Body regions</legend>
          <div className="flex flex-wrap gap-2">
            {BODY_REGIONS.map((r) => (
              <button
                key={r}
                type="button"
                onClick={() => toggleMulti(bodyRegions, r, setBodyRegions)}
                className={`px-3 py-2 rounded-lg text-sm border transition-colors ${
                  bodyRegions.includes(r)
                    ? 'bg-accent/20 border-accent text-accent'
                    : 'bg-surface-overlay border-border text-text-muted'
                }`}
              >
                {r}
              </button>
            ))}
          </div>
        </fieldset>

        <fieldset>
          <legend className="text-sm text-text-muted mb-2">Suspected triggers</legend>
          <div className="flex flex-wrap gap-2">
            {SUSPECTED_TRIGGERS.map((t) => (
              <button
                key={t}
                type="button"
                onClick={() => toggleMulti(suspectedTriggers, t, setSuspectedTriggers)}
                className={`px-3 py-2 rounded-lg text-sm border transition-colors ${
                  suspectedTriggers.includes(t)
                    ? 'bg-accent/20 border-accent text-accent'
                    : 'bg-surface-overlay border-border text-text-muted'
                }`}
              >
                {t}
              </button>
            ))}
          </div>
        </fieldset>

        <Input
          label="Doing what at onset"
          value={doingWhat}
          onChange={(e) => setDoingWhat(e.target.value)}
          placeholder="One line"
        />

        <Select
          label="Script run"
          value={scriptRun}
          onChange={(e) => setScriptRun(e.target.value as ScriptId)}
        >
          {SCRIPTS.map((s) => (
            <option key={s} value={s}>{s}</option>
          ))}
        </Select>

        <Textarea
          label="Notes"
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          rows={2}
        />

        <Button type="submit" className="w-full" disabled={!needsLog}>
          Log flare
        </Button>
      </form>

      {data.flares.length > 0 && (
        <section className="mt-8">
          <h2 className="text-sm font-medium text-text-muted uppercase tracking-wide mb-3">
            Recent ({data.flares.length} total)
          </h2>
          <div className="space-y-2">
            {data.flares.slice(0, 10).map((f) => (
              <Card key={f.id} className="py-3">
                <div className="flex justify-between items-start mb-1">
                  <p className="font-medium text-sm">{f.summary}</p>
                  <span className="text-sm tabular-nums">{f.severity}/10</span>
                </div>
                <p className="text-xs text-text-muted">
                  {new Date(f.time).toLocaleString()} · {f.primarySymptom}
                  {f.scriptRun !== 'none' && ` · ${f.scriptRun}`}
                </p>
              </Card>
            ))}
          </div>
        </section>
      )}
    </div>
  )
}
