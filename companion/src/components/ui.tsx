import type { Tier } from '../types'

const TIER_STYLES: Record<Tier, { bg: string; text: string; border: string; label: string }> = {
  green: {
    bg: 'bg-tier-green/20',
    text: 'text-tier-green',
    border: 'border-tier-green/40',
    label: 'Green',
  },
  yellow: {
    bg: 'bg-tier-yellow/20',
    text: 'text-tier-yellow',
    border: 'border-tier-yellow/40',
    label: 'Yellow',
  },
  red: {
    bg: 'bg-tier-red/20',
    text: 'text-tier-red',
    border: 'border-tier-red/40',
    label: 'Red',
  },
  black: {
    bg: 'bg-tier-black/40',
    text: 'text-text-muted',
    border: 'border-tier-black/60',
    label: 'Black',
  },
}

export function TierBadge({ tier, size = 'md' }: { tier: Tier; size?: 'sm' | 'md' | 'lg' }) {
  const s = TIER_STYLES[tier]
  const sizeClass = size === 'lg' ? 'text-lg px-4 py-2' : size === 'sm' ? 'text-xs px-2 py-0.5' : 'text-sm px-3 py-1'
  return (
    <span className={`inline-flex items-center rounded-full border font-medium capitalize ${s.bg} ${s.text} ${s.border} ${sizeClass}`}>
      {s.label}
    </span>
  )
}

export function SeverityBar({ value, max = 10 }: { value: number; max?: number }) {
  const pct = Math.min(100, (value / max) * 100)
  const color =
    value <= 3 ? 'bg-tier-green' :
    value <= 6 ? 'bg-tier-yellow' :
    value <= 8 ? 'bg-tier-red' : 'bg-tier-black'

  return (
    <div className="flex items-center gap-2">
      <div className="h-2 flex-1 rounded-full bg-surface-overlay overflow-hidden">
        <div className={`h-full rounded-full transition-all ${color}`} style={{ width: `${pct}%` }} />
      </div>
      <span className="text-sm text-text-muted w-8 text-right tabular-nums">{value}</span>
    </div>
  )
}

export function Card({ children, className = '' }: { children: React.ReactNode; className?: string }) {
  return (
    <div className={`rounded-xl border border-border bg-surface-raised p-4 ${className}`}>
      {children}
    </div>
  )
}

export function Button({
  children,
  onClick,
  variant = 'primary',
  className = '',
  disabled = false,
  type = 'button',
}: {
  children: React.ReactNode
  onClick?: () => void
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost'
  className?: string
  disabled?: boolean
  type?: 'button' | 'submit'
}) {
  const variants = {
    primary: 'bg-accent text-surface font-semibold hover:bg-accent/90 active:bg-accent-dim',
    secondary: 'bg-surface-overlay border border-border text-text hover:bg-border/50',
    danger: 'bg-tier-red/20 border border-tier-red/40 text-tier-red hover:bg-tier-red/30',
    ghost: 'text-text-muted hover:text-text hover:bg-surface-overlay',
  }

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`min-h-12 px-5 py-3 rounded-xl text-base transition-colors disabled:opacity-40 disabled:cursor-not-allowed ${variants[variant]} ${className}`}
    >
      {children}
    </button>
  )
}

export function Input({
  label,
  ...props
}: React.InputHTMLAttributes<HTMLInputElement> & { label: string }) {
  return (
    <label className="block space-y-1.5">
      <span className="text-sm text-text-muted">{label}</span>
      <input
        {...props}
        className="w-full min-h-12 px-4 rounded-xl bg-surface-overlay border border-border text-text text-base placeholder:text-text-muted/50 focus:border-accent focus:outline-none"
      />
    </label>
  )
}

export function Select({
  label,
  children,
  ...props
}: React.SelectHTMLAttributes<HTMLSelectElement> & { label: string }) {
  return (
    <label className="block space-y-1.5">
      <span className="text-sm text-text-muted">{label}</span>
      <select
        {...props}
        className="w-full min-h-12 px-4 rounded-xl bg-surface-overlay border border-border text-text text-base focus:border-accent focus:outline-none appearance-none"
      >
        {children}
      </select>
    </label>
  )
}

export function Textarea({
  label,
  ...props
}: React.TextareaHTMLAttributes<HTMLTextAreaElement> & { label: string }) {
  return (
    <label className="block space-y-1.5">
      <span className="text-sm text-text-muted">{label}</span>
      <textarea
        {...props}
        className="w-full min-h-24 px-4 py-3 rounded-xl bg-surface-overlay border border-border text-text text-base placeholder:text-text-muted/50 focus:border-accent focus:outline-none resize-y"
      />
    </label>
  )
}

export function PageHeader({ title, subtitle }: { title: string; subtitle?: string }) {
  return (
    <header className="mb-6">
      <h1 className="text-2xl font-semibold text-text tracking-tight">{title}</h1>
      {subtitle && <p className="mt-1 text-text-muted">{subtitle}</p>}
    </header>
  )
}

export function ListSection({ title, items, variant = 'neutral' }: {
  title: string
  items: string[]
  variant?: 'allowed' | 'forbidden' | 'neutral'
}) {
  const icon = variant === 'allowed' ? '✓' : variant === 'forbidden' ? '✗' : '·'
  const color = variant === 'allowed' ? 'text-tier-green' : variant === 'forbidden' ? 'text-tier-red' : 'text-text-muted'

  return (
    <section className="space-y-2">
      <h3 className="text-sm font-medium text-text-muted uppercase tracking-wide">{title}</h3>
      <ul className="space-y-2">
        {items.map((item, i) => (
          <li key={i} className="flex gap-2 text-sm leading-relaxed">
            <span className={`shrink-0 ${color}`}>{icon}</span>
            <span>{item}</span>
          </li>
        ))}
      </ul>
    </section>
  )
}
