import { useParams, Link } from 'react-router-dom'
import { PROTOCOLS } from '../data/content'
import { Card, TierBadge, ListSection, PageHeader } from '../components/ui'
import type { Tier } from '../types'

export function ProtocolPage() {
  const { tier } = useParams<{ tier: Tier }>()
  const protocol = PROTOCOLS.find((p) => p.tier === tier)

  if (!protocol) {
    return (
      <div>
        <PageHeader title="Protocols" subtitle="Select a tier" />
        <div className="space-y-2">
          {PROTOCOLS.map((p) => (
            <Link key={p.tier} to={`/protocol/${p.tier}`}>
              <Card className="flex items-center justify-between hover:border-accent/40 transition-colors">
                <div>
                  <p className="font-medium">{p.title}</p>
                  <p className="text-sm text-text-muted">{p.tagline}</p>
                </div>
                <TierBadge tier={p.tier} />
              </Card>
            </Link>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div>
      <div className="flex items-center gap-3 mb-2">
        <TierBadge tier={protocol.tier} size="lg" />
        <Link to="/protocol" className="text-sm text-text-muted hover:text-text">All tiers</Link>
      </div>
      <PageHeader title={protocol.title} subtitle={protocol.tagline} />

      <div className="space-y-6">
        <Card>
          <ListSection title="Entry criteria" items={protocol.entryCriteria} />
        </Card>

        <Card>
          <ListSection title="Allowed" items={protocol.allowed} variant="allowed" />
        </Card>

        <Card>
          <ListSection title="Forbidden" items={protocol.forbidden} variant="forbidden" />
        </Card>

        <Card>
          <ListSection title="Minimum daily completes" items={protocol.minimums} />
        </Card>

        {(protocol.exitUp || protocol.exitDown) && (
          <Card className="space-y-3">
            {protocol.exitUp && (
              <div>
                <h3 className="text-sm font-medium text-tier-green mb-1">↑ Up to previous tier</h3>
                <p className="text-sm text-text-muted">{protocol.exitUp}</p>
              </div>
            )}
            {protocol.exitDown && (
              <div>
                <h3 className="text-sm font-medium text-tier-red mb-1">↓ Down to next tier</h3>
                <p className="text-sm text-text-muted">{protocol.exitDown}</p>
              </div>
            )}
          </Card>
        )}

        <p className="text-sm text-text-muted italic border-l-2 border-accent/40 pl-4">
          {protocol.notes}
        </p>
      </div>
    </div>
  )
}
