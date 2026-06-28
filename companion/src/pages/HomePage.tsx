import { Link } from 'react-router-dom'
import { useAppData, todayISO, weekStats, weekFlareStats } from '../hooks/useAppData'
import { Card, TierBadge, Button, PageHeader } from '../components/ui'

export function HomePage() {
  const { data, markDailyTaskDone, pendingDailyTasks } = useAppData()
  const today = todayISO()
  const todayVitals = data.vitals.find((v) => v.date === today)
  const tier = todayVitals?.tier ?? 'green'
  const pending = pendingDailyTasks(tier)
  const stats = weekStats(data.vitals)
  const weekFlares = weekFlareStats(data.flares)
  const recentFlares = data.flares.slice(0, 3)

  return (
    <div>
      <PageHeader
        title="body-os"
        subtitle="Logs before analysis. Runbooks over improvisation."
      />

      {todayVitals ? (
        <Card className="mb-4">
          <div className="flex items-center justify-between mb-3">
            <span className="text-sm text-text-muted">Today</span>
            <TierBadge tier={todayVitals.tier} size="lg" />
          </div>
          <div className="grid grid-cols-2 gap-3 text-sm">
            <div>
              <span className="text-text-muted">Pain</span>
              <p className="text-lg tabular-nums">{todayVitals.morningPain}/10</p>
            </div>
            <div>
              <span className="text-text-muted">Energy</span>
              <p className="text-lg tabular-nums">{todayVitals.morningEnergy}/10</p>
            </div>
            <div>
              <span className="text-text-muted">Sleep</span>
              <p className="text-lg tabular-nums">{todayVitals.sleepHours}h</p>
            </div>
            <div>
              <span className="text-text-muted">Autonomic</span>
              <p className="text-lg">{todayVitals.autonomicState}</p>
            </div>
          </div>
          <Link to={`/protocol/${todayVitals.tier}`} className="block mt-4">
            <Button variant="secondary" className="w-full text-sm min-h-10">
              View {todayVitals.tier} protocol →
            </Button>
          </Link>
        </Card>
      ) : (
        <Card className="mb-4 border-accent/30">
          <p className="text-text-muted mb-3">No vitals logged today yet.</p>
          <Link to="/vitals">
            <Button className="w-full">Morning check-in (60 sec)</Button>
          </Link>
        </Card>
      )}

      <Card className="mb-4">
        <h2 className="text-sm font-medium text-text-muted uppercase tracking-wide mb-3">
          Daily minimums
        </h2>
        {pending.length === 0 ? (
          <p className="text-sm text-tier-green">
            Minimum completes done for {tier}. Rest is optional.
          </p>
        ) : (
          <ul className="space-y-2">
            {pending.map((task) => (
              <li key={`${task.id}-${task.slot}`} className="flex items-center justify-between gap-2">
                <span className="text-sm">{task.label}</span>
                <Button
                  variant="secondary"
                  className="min-h-8 px-3 py-1 text-xs shrink-0"
                  onClick={() => markDailyTaskDone(task.id, task.slot)}
                >
                  Done
                </Button>
              </li>
            ))}
          </ul>
        )}
        <p className="text-xs text-text-muted mt-3">
          Scout nudges on schedule too. Say <span className="text-accent">tasks</span> or{' '}
          <span className="text-accent">done teeth</span> to the robot.
        </p>
      </Card>

      <section className="mb-6">
        <h2 className="text-sm font-medium text-text-muted uppercase tracking-wide mb-3">
          Quick respond
        </h2>
        <div className="grid grid-cols-2 gap-2">
          <Link to="/respond?flow=reset-60s">
            <Button variant="secondary" className="w-full text-sm min-h-14">
              reset-60s
            </Button>
          </Link>
          <Link to="/respond?flow=reset-5min">
            <Button variant="secondary" className="w-full text-sm min-h-14">
              reset-5min
            </Button>
          </Link>
          <Link to="/respond?flow=hijacked">
            <Button variant="danger" className="w-full text-sm min-h-14">
              Hijacked
            </Button>
          </Link>
          <Link to="/respond?flow=doom-loop">
            <Button variant="danger" className="w-full text-sm min-h-14">
              Doom loop
            </Button>
          </Link>
        </div>
      </section>

      <Card className="mb-4">
        <h2 className="text-sm font-medium text-text-muted uppercase tracking-wide mb-3">
          This week
        </h2>
        <div className="space-y-2 text-sm">
          <div className="flex justify-between">
            <span>Green / yellow days</span>
            <span className={stats.sloGreenYellow ? 'text-tier-green' : 'text-tier-yellow'}>
              {stats.greenYellowDays} / 5 SLO
            </span>
          </div>
          <div className="flex justify-between">
            <span>Flares ≥ 6 logged</span>
            <span className="tabular-nums">{weekFlares.length}</span>
          </div>
          <div className="flex justify-between">
            <span>Days logged</span>
            <span className="tabular-nums">{stats.daysLogged}</span>
          </div>
        </div>
      </Card>

      {recentFlares.length > 0 && (
        <section>
          <h2 className="text-sm font-medium text-text-muted uppercase tracking-wide mb-3">
            Recent flares
          </h2>
          <div className="space-y-2">
            {recentFlares.map((f) => (
              <Card key={f.id} className="py-3">
                <div className="flex justify-between items-start gap-2">
                  <div>
                    <p className="font-medium text-sm">{f.summary}</p>
                    <p className="text-xs text-text-muted mt-0.5">
                      {new Date(f.time).toLocaleDateString()} · {f.primarySymptom}
                    </p>
                  </div>
                  <span className="text-sm tabular-nums text-text-muted">{f.severity}/10</span>
                </div>
              </Card>
            ))}
          </div>
        </section>
      )}

      <p className="mt-8 text-xs text-text-muted text-center">
        Crisis support: <a href="tel:988" className="text-accent underline">988</a> (call or text)
      </p>
    </div>
  )
}
