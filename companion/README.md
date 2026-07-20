# body-os Companion App

Local-first web companion for the [body-os](https://github.com/ginalyncox/body-os) health debugging framework. Built for daily use alongside CBT-CP (Cognitive Behavioral Therapy for Chronic Pain) skills — pacing, cognitive coping, and guided recovery.

## What it does

| Feature | Maps to body-os |
|--------|-----------------|
| **Daily Vitals** | 60-second morning check-in with tier suggestion |
| **Flare Log** | Structured flare logging (severity ≥ 4) |
| **Respond** | Guided scripts & runbooks with step checkoffs and timers |
| **Protocols** | Green / yellow / red / black day rules |
| **Known Triggers** | Confirmed, suspect, and cleared triggers |
| **Postmortems** | Blameless retros after red/black days |
| **SLO dashboard** | Weekly green/yellow day tracking |
| **Incident Commander** | GPT-5.6 or offline runbook response from an unstructured flare report |

## Design principles

- **Low sensory load** — warm dark palette, no harsh animations, large tap targets
- **Execute, don't improvise** — guided flows for resets and runbooks
- **Local-first** — all data stays in your browser (`localStorage`)
- **Crisis resources** — 988 linked throughout

## Quick start

```bash
cd companion
npm install
npm run dev
```

Open http://localhost:5173

## Build & deploy

```bash
npm run build
npm run preview
```

Deploy the `dist/` folder as a static site (Render, Netlify, GitHub Pages, etc.).

For the GPT-5.6 Incident Commander, run the included Node server so the API key
stays server-side:

```bash
OPENAI_API_KEY=your_key npm start
```

The root `render.yaml` configures this server and expects `OPENAI_API_KEY` as a
secret environment variable. The companion automatically uses its offline
runbook matcher if the API is unavailable.

## Data

- Stored in browser `localStorage` under key `body-os-data`
- **Export JSON** regularly from the More page for backup
- No server, no accounts, no cloud sync (by design for privacy)

## Bootstrap mode (first week)

From the body-os README:

1. Every flare ≥ 4 severity → log it
2. Every morning → Daily Vitals
3. When hijacked → run a script from Respond and log which one
4. End of week → check SLO dashboard, write postmortem if there was a red day

## Tech stack

- Vite + React + TypeScript
- Tailwind CSS v4
- React Router

## License

Same as parent body-os repo.
