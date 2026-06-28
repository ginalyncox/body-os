import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useAppData } from '../hooks/useAppData'
import { useRobotSync } from '../hooks/useRobotSync'
import { KNOWN_TRIGGERS, SLOS, PROTOCOLS } from '../data/content'
import { Card, Button, Textarea, TierBadge, PageHeader, Input } from '../components/ui'

export function MorePage() {
  const { data, addPostmortem, exportData, importData, clearData, mergeRobotData } = useAppData()
  const robot = useRobotSync(data, mergeRobotData)
  const [showPmForm, setShowPmForm] = useState(false)
  const [pmText, setPmText] = useState({
    date: new Date().toISOString().slice(0, 10),
    tierReached: 'red' as 'red' | 'black',
    peakSeverity: 8,
    whatHappened: '',
    triggers: '',
    whatWorked: '',
    pastSelfActions: '',
    futureNote: '',
  })

  const handleExport = () => {
    const blob = new Blob([exportData()], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `body-os-export-${new Date().toISOString().slice(0, 10)}.json`
    a.click()
    URL.revokeObjectURL(url)
  }

  const handleImport = () => {
    const input = document.createElement('input')
    input.type = 'file'
    input.accept = '.json'
    input.onchange = (e) => {
      const file = (e.target as HTMLInputElement).files?.[0]
      if (!file) return
      const reader = new FileReader()
      reader.onload = () => importData(reader.result as string)
      reader.readAsText(file)
    }
    input.click()
  }

  const submitPostmortem = (e: React.FormEvent) => {
    e.preventDefault()
    addPostmortem({
      date: pmText.date,
      tierReached: pmText.tierReached,
      peakSeverity: pmText.peakSeverity,
      timeline: '',
      whatHappened: pmText.whatHappened,
      triggers: pmText.triggers,
      whatWorked: pmText.whatWorked,
      whatDidntWork: '',
      pastSelfActions: pmText.pastSelfActions,
      systemChanges: '',
      sloImpact: '',
      futureNote: pmText.futureNote,
    })
    setShowPmForm(false)
    setPmText({
      date: new Date().toISOString().slice(0, 10),
      tierReached: 'red',
      peakSeverity: 8,
      whatHappened: '',
      triggers: '',
      whatWorked: '',
      pastSelfActions: '',
      futureNote: '',
    })
  }

  return (
    <div>
      <PageHeader title="More" subtitle="Triggers, SLOs, postmortems, data" />

      <section className="mb-8">
        <h2 className="text-sm font-medium text-text-muted uppercase tracking-wide mb-3">
          Protocols
        </h2>
        <div className="grid grid-cols-2 gap-2">
          {PROTOCOLS.map((p) => (
            <Link key={p.tier} to={`/protocol/${p.tier}`}>
              <Card className="text-center py-4 hover:border-accent/40 transition-colors">
                <TierBadge tier={p.tier} />
              </Card>
            </Link>
          ))}
        </div>
      </section>

      <section className="mb-8">
        <h2 className="text-sm font-medium text-text-muted uppercase tracking-wide mb-3">
          Known triggers
        </h2>
        <div className="space-y-2">
          {KNOWN_TRIGGERS.map((t) => (
            <Card key={t.name} className="py-3">
              <div className="flex justify-between items-start gap-2 mb-1">
                <p className="font-medium text-sm">{t.name}</p>
                <span className={`text-xs px-2 py-0.5 rounded-full ${
                  t.status === 'Confirmed' ? 'bg-tier-red/20 text-tier-red' :
                  t.status === 'Suspect' ? 'bg-tier-yellow/20 text-tier-yellow' :
                  'bg-tier-green/20 text-tier-green'
                }`}>
                  {t.status}
                </span>
              </div>
              <p className="text-xs text-text-muted">{t.mitigation}</p>
            </Card>
          ))}
        </div>
      </section>

      <section className="mb-8">
        <h2 className="text-sm font-medium text-text-muted uppercase tracking-wide mb-3">
          SLOs (v0.1)
        </h2>
        <Card>
          <ul className="space-y-2 text-sm">
            {SLOS.map((slo, i) => (
              <li key={i} className="flex gap-2">
                <span className="text-accent">·</span>
                <span>{slo}</span>
              </li>
            ))}
          </ul>
        </Card>
      </section>

      <section className="mb-8">
        <div className="flex justify-between items-center mb-3">
          <h2 className="text-sm font-medium text-text-muted uppercase tracking-wide">
            Postmortems
          </h2>
          <Button variant="secondary" className="min-h-8 px-3 py-1 text-sm" onClick={() => setShowPmForm(!showPmForm)}>
            {showPmForm ? 'Cancel' : 'New'}
          </Button>
        </div>

        {showPmForm && (
          <form onSubmit={submitPostmortem} className="space-y-3 mb-4">
            <Textarea
              label="What happened (factual)"
              value={pmText.whatHappened}
              onChange={(e) => setPmText({ ...pmText, whatHappened: e.target.value })}
              required
            />
            <Textarea
              label="Triggers (hypothesis)"
              value={pmText.triggers}
              onChange={(e) => setPmText({ ...pmText, triggers: e.target.value })}
            />
            <Textarea
              label="What worked"
              value={pmText.whatWorked}
              onChange={(e) => setPmText({ ...pmText, whatWorked: e.target.value })}
            />
            <Textarea
              label="What past-you could have done differently"
              value={pmText.pastSelfActions}
              onChange={(e) => setPmText({ ...pmText, pastSelfActions: e.target.value })}
            />
            <Textarea
              label="One sentence to future-you"
              value={pmText.futureNote}
              onChange={(e) => setPmText({ ...pmText, futureNote: e.target.value })}
            />
            <Button type="submit" className="w-full">Save postmortem</Button>
          </form>
        )}

        {data.postmortems.length === 0 && !showPmForm && (
          <p className="text-sm text-text-muted">No postmortems yet. Write one after red/black days.</p>
        )}

        <div className="space-y-2">
          {data.postmortems.map((pm) => (
            <Card key={pm.id} className="py-3">
              <p className="text-sm font-medium">{pm.date} — {pm.tierReached}</p>
              <p className="text-xs text-text-muted mt-1 line-clamp-2">{pm.whatHappened}</p>
              {pm.futureNote && (
                <p className="text-xs text-accent mt-2 italic">"{pm.futureNote}"</p>
              )}
            </Card>
          ))}
        </div>
      </section>

      <section className="mb-8">
        <h2 className="text-sm font-medium text-text-muted uppercase tracking-wide mb-3">
          Robot sync
        </h2>
        <Card className="space-y-3">
          <Input
            label="Robot sync URL"
            value={robot.syncUrl}
            onChange={(e) => robot.saveUrl(e.target.value)}
            placeholder="http://127.0.0.1:8765/api/sync"
          />
          <div className="flex gap-2 flex-wrap">
            <Button variant="secondary" onClick={robot.ping} disabled={robot.loading} className="flex-1 text-sm min-h-10">
              Ping
            </Button>
            <Button variant="secondary" onClick={robot.pull} disabled={robot.loading} className="flex-1 text-sm min-h-10">
              Pull from robot
            </Button>
            <Button variant="secondary" onClick={robot.push} disabled={robot.loading} className="flex-1 text-sm min-h-10">
              Push to robot
            </Button>
          </div>
          {robot.status && (
            <p className="text-xs text-text-muted">{robot.status}</p>
          )}
          <p className="text-xs text-text-muted">
            Start the robot with sync enabled: <code className="text-accent">python3 -m brain</code>
          </p>
        </Card>
      </section>

      <section className="mb-8">
        <h2 className="text-sm font-medium text-text-muted uppercase tracking-wide mb-3">
          Data
        </h2>
        <div className="flex gap-2">
          <Button variant="secondary" onClick={handleExport} className="flex-1 text-sm">
            Export JSON
          </Button>
          <Button variant="secondary" onClick={handleImport} className="flex-1 text-sm">
            Import JSON
          </Button>
        </div>
        <Button variant="ghost" onClick={clearData} className="w-full mt-2 text-sm text-tier-red">
          Clear all local data
        </Button>
        <p className="text-xs text-text-muted mt-2 text-center">
          Data stays on this device. Export regularly for backup.
        </p>
      </section>

      <Card className="text-center">
        <p className="text-sm text-text-muted mb-2">Crisis support</p>
        <a href="tel:988" className="text-2xl font-medium text-accent">988</a>
        <p className="text-xs text-text-muted mt-1">Call or text, 24/7</p>
      </Card>
    </div>
  )
}
