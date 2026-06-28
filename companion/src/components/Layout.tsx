import { NavLink, Outlet } from 'react-router-dom'

const navItems = [
  { to: '/', label: 'Home', icon: '◉' },
  { to: '/vitals', label: 'Vitals', icon: '♡' },
  { to: '/respond', label: 'Respond', icon: '◎' },
  { to: '/flare', label: 'Flare', icon: '△' },
  { to: '/more', label: 'More', icon: '⋯' },
]

export function Layout() {
  return (
    <div className="flex min-h-dvh flex-col">
      <main className="flex-1 px-4 pt-6 pb-24 max-w-lg mx-auto w-full">
        <Outlet />
      </main>

      <nav
        className="fixed bottom-0 inset-x-0 border-t border-border bg-surface-raised/95 backdrop-blur-sm safe-area-pb"
        aria-label="Main navigation"
      >
        <div className="flex max-w-lg mx-auto">
          {navItems.map(({ to, label, icon }) => (
            <NavLink
              key={to}
              to={to}
              end={to === '/'}
              className={({ isActive }) =>
                `flex flex-1 flex-col items-center gap-0.5 py-3 text-xs transition-colors ${
                  isActive ? 'text-accent' : 'text-text-muted hover:text-text'
                }`
              }
            >
              <span className="text-lg leading-none" aria-hidden>{icon}</span>
              <span>{label}</span>
            </NavLink>
          ))}
        </div>
      </nav>
    </div>
  )
}
