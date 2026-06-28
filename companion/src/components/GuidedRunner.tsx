import { useState, useEffect, useCallback } from 'react'
import { Button, Card } from './ui'
import type { GuidedFlow } from '../types'

interface GuidedRunnerProps {
  flow: GuidedFlow
  onComplete: () => void
  onCancel: () => void
}

export function GuidedRunner({ flow, onComplete, onCancel }: GuidedRunnerProps) {
  const [stepIndex, setStepIndex] = useState(0)
  const [checked, setChecked] = useState<Set<number>>(new Set())
  const [timerLeft, setTimerLeft] = useState<number | null>(null)
  const [running, setRunning] = useState(false)

  const step = flow.steps[stepIndex]
  const isLast = stepIndex >= flow.steps.length - 1

  const advance = useCallback(() => {
    if (isLast) {
      onComplete()
    } else {
      setStepIndex((i) => i + 1)
      setTimerLeft(null)
      setRunning(false)
    }
  }, [isLast, onComplete])

  useEffect(() => {
    if (!running || timerLeft === null) return
    if (timerLeft <= 0) {
      advance()
      return
    }
    const id = setTimeout(() => setTimerLeft((t) => (t ?? 0) - 1), 1000)
    return () => clearTimeout(id)
  }, [running, timerLeft, advance])

  const startTimer = () => {
    if (step.durationSeconds) {
      setTimerLeft(step.durationSeconds)
      setRunning(true)
    }
  }

  const toggleCheck = () => {
    const next = new Set(checked)
    if (next.has(stepIndex)) next.delete(stepIndex)
    else next.add(stepIndex)
    setChecked(next)
  }

  const formatTime = (s: number) => {
    const m = Math.floor(s / 60)
    const sec = s % 60
    return m > 0 ? `${m}:${sec.toString().padStart(2, '0')}` : `${sec}s`
  }

  return (
    <div className="fixed inset-0 z-50 flex flex-col bg-surface">
      <header className="flex items-center justify-between border-b border-border px-4 py-3">
        <button onClick={onCancel} className="text-text-muted hover:text-text min-h-12 px-2">
          ← Back
        </button>
        <span className="text-sm text-text-muted">
          Step {stepIndex + 1} / {flow.steps.length}
        </span>
      </header>

      <div className="flex-1 flex flex-col px-4 py-8 max-w-lg mx-auto w-full">
        <p className="text-sm text-accent mb-2">{flow.title}</p>
        <h2 className="text-xl font-medium leading-relaxed mb-8">{step.text}</h2>

        {step.durationSeconds && (
          <div className="mb-8 text-center">
            {running && timerLeft !== null ? (
              <div className="text-5xl font-light tabular-nums text-accent">
                {formatTime(timerLeft)}
              </div>
            ) : (
              <Button onClick={startTimer} variant="secondary" className="w-full">
                Start {formatTime(step.durationSeconds)} timer
              </Button>
            )}
          </div>
        )}

        <label className="flex items-center gap-3 min-h-14 cursor-pointer">
          <input
            type="checkbox"
            checked={checked.has(stepIndex)}
            onChange={toggleCheck}
            className="w-6 h-6 rounded border-border accent-accent"
          />
          <span className="text-text-muted">Step complete</span>
        </label>
      </div>

      <footer className="border-t border-border p-4 max-w-lg mx-auto w-full">
        <Button
          onClick={advance}
          className="w-full"
          disabled={!checked.has(stepIndex) && !running}
        >
          {isLast ? 'Finish' : 'Next step'}
        </Button>
      </footer>
    </div>
  )
}

export function FlowCard({
  flow,
  onStart,
  urgent = false,
}: {
  flow: GuidedFlow
  onStart: () => void
  urgent?: boolean
}) {
  return (
    <Card className={urgent ? 'border-tier-red/40' : ''}>
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs text-text-muted uppercase tracking-wide mb-1">
            {flow.type}
          </p>
          <h3 className="font-medium text-lg">{flow.title}</h3>
          <p className="text-sm text-text-muted mt-1">{flow.subtitle}</p>
        </div>
        <Button onClick={onStart} variant={urgent ? 'danger' : 'primary'} className="shrink-0 min-h-10 px-4 py-2 text-sm">
          Run
        </Button>
      </div>
    </Card>
  )
}
