import { useMemo, useState } from 'react'
import { useAppData } from '../hooks/useAppData'
import type { PrimarySymptom, ScriptId, SuspectedTrigger, Tier } from '../types'

type Step = { title: string; instruction: string }
type Plan = {
  tier: Tier
  headline: string
  rationale: string
  immediateSafety: string[]
  steps: Step[]
  clinicianSummary: string
  postmortemPrompt: string
  emergency: boolean
  generatedBy?: 'gpt-5.6' | 'body-os'
}

const examples = [
  'My pain jumped to 8, I am itching and getting overwhelmed.',
  'I stood too long and now I feel shaky, hot, and lightheaded.',
]

function urgentSignal(text: string) {
  return /can'?t breathe|cannot breathe|chest pain|new paralysis|face droop|stroke|passed out|unconscious|suicid|kill myself|anaphyl|throat (is )?closing/i.test(text)
}

function fallbackPlan(description: string, severity: number): Plan {
  const text = description.toLowerCase()
  const tier: Tier = severity >= 9 ? 'black' : severity >= 7 ? 'red' : severity >= 4 ? 'yellow' : 'green'
  const steps: Step[] = [{ title: 'Reduce the load', instruction: tier === 'green' ? 'Pause and notice what changed.' : 'Stop the current task. Sit or recline in your safest supported position.' }]
  if (/shaky|lightheaded|dizzy|hot|heart|standing|faint/.test(text)) steps.push({ title: 'Stabilize', instruction: 'Avoid standing. Lower stimulation and use your established autonomic-flare plan.' })
  if (/pain|burn|stab|electric|ache/.test(text)) steps.push({ title: 'Match, do not shock', instruction: 'Check posture. Try neutral temperature and tiny movement only if it helps.' })
  if (/itch|hive|rash|flush/.test(text)) steps.push({ title: 'Protect the skin', instruction: 'Move from suspected exposure and use only your established clinician-approved itch plan.' })
  if (/overwhelm|loud|loop|panic|sensory/.test(text)) steps.push({ title: 'Make the world smaller', instruction: 'Dim light, reduce sound, and choose one slow exhale longer than the inhale.' })
  steps.push({ title: 'Recheck', instruction: 'After ten minutes, note whether severity changed. Escalate to your red-day plan if it did not.' })
  return {
    tier,
    headline: tier === 'black' ? 'Nothing to prove. Survival floor only.' : tier === 'red' ? 'Stop. The system needs conservation mode.' : 'The signal is real. Reduce load now.',
    rationale: `BodyOS selected ${tier} tier from severity ${severity}/10 and matched your report to existing runbooks.`,
    immediateSafety: ['Use only treatments already approved for you.', 'If symptoms feel dangerous, new, or rapidly worsening, contact emergency services.'],
    steps,
    clinicianSummary: `Reported flare at severity ${severity}/10: ${description}`,
    postmortemPrompt: 'What changed before the incident, what helped, and what should Future You change in this runbook?',
    emergency: urgentSignal(description), generatedBy: 'body-os',
  }
}

function inferSymptom(text: string): PrimarySymptom {
  if (/itch|hive|rash|flush/i.test(text)) return 'Itch'
  if (/burn/i.test(text)) return 'Burning'
  if (/dizzy|lightheaded|shaky|standing|faint/i.test(text)) return 'Autonomic spike'
  if (/fog|confus/i.test(text)) return 'Brain fog'
  return 'Pain'
}

function inferTrigger(text: string): SuspectedTrigger {
  if (/stand/i.test(text)) return 'Standing'
  if (/heat|hot/i.test(text)) return 'Heat'
  if (/sleep|tired/i.test(text)) return 'Sleep debt'
  if (/overwhelm|loud|sensory/i.test(text)) return 'Sensory load'
  return 'Unknown'
}

export function IncidentCommander() {
  const { addFlare } = useAppData()
  const [description, setDescription] = useState('')
  const [severity, setSeverity] = useState(6)
  const [plan, setPlan] = useState<Plan | null>(null)
  const [activeStep, setActiveStep] = useState(0)
  const [loading, setLoading] = useState(false)
  const [expanded, setExpanded] = useState(false)
  const urgent = useMemo(() => urgentSignal(description), [description])

  async function start() {
    if (description.trim().length < 8) return
    setLoading(true)
    let next: Plan
    try {
      const response = await fetch('/api/incident', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ description: description.trim(), severity }) })
      if (!response.ok) throw new Error('unavailable')
      next = await response.json() as Plan
      next.generatedBy = 'gpt-5.6'
    } catch {
      next = fallbackPlan(description.trim(), severity)
    }
    addFlare({
      summary: description.trim(), time: new Date().toISOString(), severity,
      primarySymptom: inferSymptom(description), bodyRegions: ['Whole body'],
      suspectedTriggers: [inferTrigger(description)], scriptRun: 'none' as ScriptId,
      notes: `Incident Commander: ${next.tier} tier. ${next.clinicianSummary}`,
    })
    setPlan(next); setActiveStep(0); setLoading(false)
  }

  function speak() {
    if (!plan || !('speechSynthesis' in window)) return
    speechSynthesis.cancel()
    const step = plan.steps[activeStep]
    const utterance = new SpeechSynthesisUtterance(`${step.title}. ${step.instruction}`)
    utterance.rate = 0.88
    speechSynthesis.speak(utterance)
  }

  if (!expanded) return (
    <button onClick={() => setExpanded(true)} className="mb-8 w-full rounded-2xl border border-accent-dim/60 bg-gradient-to-br from-surface-raised to-surface p-5 text-left shadow-lg">
      <span className="text-xs font-semibold uppercase tracking-[0.18em] text-accent">New · Incident Commander</span>
      <strong className="mt-2 block text-xl text-text">Tell me what is happening</strong>
      <span className="mt-1 block text-sm leading-6 text-text-muted">Get one calm step at a time from your BodyOS runbooks.</span>
    </button>
  )

  if (!plan) return (
    <section className="mb-8 rounded-2xl border border-accent-dim/60 bg-surface-raised p-5 shadow-xl" aria-labelledby="commander-title">
      <div className="flex items-start justify-between gap-4">
        <div><span className="text-xs font-semibold uppercase tracking-[0.18em] text-accent">Incident Commander</span><h2 id="commander-title" className="mt-1 text-2xl font-semibold">What is happening now?</h2></div>
        <button onClick={() => setExpanded(false)} className="text-sm text-text-muted">Close</button>
      </div>
      <p className="mt-2 text-sm leading-6 text-text-muted">Short and messy is okay. You should not have to troubleshoot yourself while flaring.</p>
      <textarea value={description} onChange={(e) => setDescription(e.target.value)} rows={4} maxLength={1200} placeholder="My pain jumped and I feel overwhelmed…" className="mt-4 w-full rounded-xl border border-border bg-surface p-3 text-text placeholder:text-text-muted focus:border-accent focus:outline-none" />
      <div className="mt-2 flex flex-wrap gap-2">{examples.map((e, i) => <button key={e} onClick={() => setDescription(e)} className="text-xs text-accent underline">Example {i + 1}</button>)}</div>
      <div className="mt-5 flex items-center justify-between"><label htmlFor="incident-severity" className="text-sm font-medium">Severity</label><output className="text-2xl font-bold text-accent">{severity}<span className="text-xs text-text-muted">/10</span></output></div>
      <input id="incident-severity" type="range" min="1" max="10" value={severity} onChange={(e) => setSeverity(Number(e.target.value))} className="mt-2 w-full accent-accent" />
      {urgent && <div role="alert" className="mt-4 rounded-xl border border-tier-red bg-tier-red/10 p-3 text-sm"><strong className="block text-tier-red">This may need emergency help.</strong><span>Call 911 for immediate danger or 988 for a mental-health crisis. Do not wait for this tool.</span></div>}
      <button onClick={start} disabled={loading || description.trim().length < 8} className="mt-5 w-full rounded-xl bg-accent px-4 py-3 font-semibold text-surface disabled:opacity-50">{loading ? 'Preparing your runbook…' : 'Start incident response'}</button>
      <p className="mt-3 text-center text-[11px] leading-5 text-text-muted">Saved history stays on this device. Only the current report is sent when GPT-5.6 is available.</p>
    </section>
  )

  const tierColor = plan.tier === 'green' ? 'text-tier-green' : plan.tier === 'yellow' ? 'text-tier-yellow' : plan.tier === 'red' ? 'text-tier-red' : 'text-text-muted'
  return (
    <section className="mb-8 rounded-2xl border border-border bg-surface-raised p-5 shadow-xl" aria-live="polite">
      <div className="flex items-start justify-between gap-4"><div><span className={`text-xs font-bold uppercase tracking-[0.18em] ${tierColor}`}>{plan.tier} tier</span><h2 className="mt-2 text-2xl font-semibold leading-tight">{plan.headline}</h2></div><button onClick={() => { window.speechSynthesis?.cancel(); setPlan(null) }} className="text-sm text-text-muted">End</button></div>
      <p className="mt-3 text-sm leading-6 text-text-muted">{plan.rationale}</p>
      {plan.emergency && <div role="alert" className="mt-4 rounded-xl border border-tier-red bg-tier-red/10 p-3 text-sm"><strong className="block text-tier-red">Stop and get immediate help.</strong> Call 911 for immediate danger or 988 for a mental-health crisis.</div>}
      <article className="mt-5 rounded-2xl border border-border bg-surface p-5">
        <span className="text-xs uppercase tracking-widest text-accent">Step {activeStep + 1} of {plan.steps.length}</span>
        <h3 className="mt-3 text-xl font-semibold">{plan.steps[activeStep].title}</h3>
        <p className="mt-2 text-lg leading-7">{plan.steps[activeStep].instruction}</p>
        <div className="mt-5 grid gap-2 sm:grid-cols-2"><button onClick={speak} className="rounded-xl border border-border px-4 py-3 text-sm">Read aloud</button><button onClick={() => setActiveStep(activeStep < plan.steps.length - 1 ? activeStep + 1 : 0)} className="rounded-xl bg-accent px-4 py-3 text-sm font-semibold text-surface">{activeStep < plan.steps.length - 1 ? 'Done — next step' : 'Run again'}</button></div>
      </article>
      <div className="mt-4 rounded-xl border border-border p-4"><span className="text-xs uppercase tracking-widest text-text-muted">Clinician handoff</span><p className="mt-2 text-sm leading-6">{plan.clinicianSummary}</p><button onClick={() => navigator.clipboard.writeText(plan.clinicianSummary)} className="mt-2 text-xs text-accent underline">Copy summary</button></div>
      <p className="mt-4 text-xs text-text-muted">{plan.generatedBy === 'gpt-5.6' ? 'Structured with GPT-5.6' : 'Offline BodyOS runbook'} · Not medical advice</p>
    </section>
  )
}
