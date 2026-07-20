import { useState, useEffect } from 'react'
import { useSearchParams } from 'react-router-dom'
import { GUIDED_FLOWS } from '../data/content'
import { FlowCard, GuidedRunner } from '../components/GuidedRunner'
import { PageHeader } from '../components/ui'
import { IncidentCommander } from '../components/IncidentCommander'
import type { GuidedFlow } from '../types'

export function RespondPage() {
  const [searchParams] = useSearchParams()
  const [activeFlow, setActiveFlow] = useState<GuidedFlow | null>(null)

  const scripts = GUIDED_FLOWS.filter((f) => f.type === 'script')
  const runbooks = GUIDED_FLOWS.filter((f) => f.type === 'runbook')

  useEffect(() => {
    const flowId = searchParams.get('flow')
    if (flowId) {
      const flow = GUIDED_FLOWS.find((f) => f.id === flowId)
      if (flow) setActiveFlow(flow)
    }
  }, [searchParams])

  if (activeFlow) {
    return (
      <GuidedRunner
        flow={activeFlow}
        onComplete={() => setActiveFlow(null)}
        onCancel={() => setActiveFlow(null)}
      />
    )
  }

  const urgentRunbooks = ['hijacked', 'pain-spike', 'doom-loop']

  return (
    <div>
      <PageHeader
        title="Respond"
        subtitle="Execute a script. Don't problem-solve during a flare."
      />

      <IncidentCommander />

      <section className="mb-8">
        <h2 className="text-sm font-medium text-text-muted uppercase tracking-wide mb-3">
          Scripts
        </h2>
        <div className="space-y-3">
          {scripts.map((flow) => (
            <FlowCard key={flow.id} flow={flow} onStart={() => setActiveFlow(flow)} />
          ))}
        </div>
      </section>

      <section>
        <h2 className="text-sm font-medium text-text-muted uppercase tracking-wide mb-3">
          Runbooks
        </h2>
        <div className="space-y-3">
          {runbooks.map((flow) => (
            <FlowCard
              key={flow.id}
              flow={flow}
              onStart={() => setActiveFlow(flow)}
              urgent={urgentRunbooks.includes(flow.id)}
            />
          ))}
        </div>
      </section>

      <p className="mt-8 text-center text-sm text-text-muted">
        Crisis: <a href="tel:988" className="text-accent underline">988</a> call or text
      </p>
    </div>
  )
}
