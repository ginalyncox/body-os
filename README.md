# body-os

> A self-hosted health debugging framework — SRE practices applied to a body with small fiber neuropathy.

**Owner:** [@ginalyncox](https://github.com/ginalyncox)
**Status:** `v0.1` — bootstrapping
**Created:** 2026-06-28
**Companion workspace:** [Notion: body-os](https://app.notion.com/p/38df9746ca7581b9bda7ff6304b05077)

---

## What this is

You are the SRE for one production system: your body. You don't fix it by being harder on it. You fix it with logs, correlation, runbooks, tiered protocols, and blameless postmortems.

This repo is the version-controlled source of truth for that framework. The Notion workspace is the daily-driver UI; this repo is the canonical text. Drift between them is fine — the repo wins when there's a conflict, because git history doesn't gaslight you.

## Core principles

- **Logs before analysis.** No theorizing about triggers without data in the flare log.
- **Runbooks over improvisation.** When an incident fires, execute a script. Don't problem-solve during a flare.
- **Tiered protocols.** Green / yellow / red / black days have pre-written rules for what is allowed, forbidden, and minimum-required. Past-you decides for present-you.
- **Blameless postmortems.** What happened, what triggered it, what worked, what to change. Never "I should have."
- **SLOs, not SLAs.** Service-level *objectives* for yourself. Missing one is data, not failure.
- **The fridge is the pause button.** Sourdough, work, life — anything can be paused. Use it without guilt.

## Companion app

A local-first web app lives in `companion/`. It implements Daily Vitals, Flare Log, guided scripts/runbooks, tier protocols, and SLO tracking — all stored in your browser.

```bash
cd companion && npm install && npm run dev
```

See [companion/README.md](companion/README.md) for details.

## Assistive robot

A rolling, talking robot brain lives in `robot/`. Edge TTS voice, GPIO/serial motor drivers, companion sync, and a 3D-printable enclosure spec.

```bash
cd robot
python3 setup.py              # config.yaml + deps
python3 -m brain --simulate   # terminal mode
python3 -m brain              # with voice + sync server
```

Companion app → **More → Robot sync** to push/pull vitals and flares.

See [robot/README.md](robot/README.md), [robot/docs/hardware.md](robot/docs/hardware.md), [robot/docs/enclosure.md](robot/docs/enclosure.md).

## Repo layout

```
body-os/
├── README.md                    ← you are here
├── companion/                   ← web companion app (Vite + React)
├── robot/                       ← assistive robot brain (Python)
├── render.yaml                  ← optional Render static site deploy
├── observability/
│   └── schemas.md               ← database schemas (Flare Log, Daily Vitals, etc.)
├── protocols/
│   ├── green-day.md             ← low symptoms, regulated
│   ├── yellow-day.md            ← moderate, listen
│   ├── red-day.md               ← high, conservation mode
│   └── black-day.md             ← system down, survival floor
├── runbooks/
│   ├── hijacked.md              ← autonomic spike
│   ├── itch-flare.md
│   ├── pain-spike.md
│   ├── sensory-overload.md
│   └── doom-loop.md             ← cognitive/emotional spiral
├── scripts/
│   ├── reset-60s.md             ← fastest recovery
│   ├── reset-5min.md            ← standard mid-flare reset
│   ├── reset-deep.md            ← long-form recovery
│   └── shutdown.md              ← end-of-day, no matter what
├── infrastructure/
│   └── environment-defaults.md  ← lighting, sound, temp, seating
└── postmortems/
    └── TEMPLATE.md              ← blameless retro template
```

## SLOs (v0.1 — adjust as data comes in)

- 5 of 7 days at green or yellow tier
- Every red/black day gets a postmortem within 48 hours
- Every flare ≥ 6 severity gets a log entry, even retroactively
- Zero days where the body's signals are overridden for > 2 hours without a logged reason

## Bootstrap mode (first week)

Do not analyze. Do not optimize. Just log.

1. Every flare ≥ 4 severity → one row in the Flare Log (Notion)
2. Every morning → one row in Daily Vitals (60 seconds)
3. When hijacked → run a script from `scripts/` and log which one
4. End of week → first dashboard view, first postmortem if there was a red day

## Confirmed system facts (as of v0.1)

- **Diagnosis:** Small fiber neuropathy (SFN). Causes autonomic flares and nerve-driven itch/pain that misfires without external cause.
- **Yeast tolerance:** Commercial baker's yeast triggers skin itch. Mature wild sourdough starter does not. Dry flour on skin is a separate SFN itch trigger.
- **Postural rule:** Standing flares SFN. Saddle stool deployed in the kitchen as the primary accommodation.
- **Companion doc:** [Sourdough Workflow — Seated, Low-Flare, Wild-Yeast-Safe (Google Drive)](https://docs.google.com/document/d/1tzyW3wpu8jaDpGAefYkMwLl0V4SuBG3_GGlGL4Wqyqk/edit)

## Conventions

- All Markdown. No proprietary formats.
- Front matter optional, kept minimal.
- Filenames are lowercase-hyphenated.
- Severity uses a 1–10 scale, consistent across all files.
- Tiers use the names: green / yellow / red / black.
- Postmortems live forever. Never delete one.
- Branch protection on `main` once the v0.1 scaffold is merged.

## Changelog

- **v0.1** (2026-06-28) — Initial scaffold. Companion web app. Assistive robot brain with Edge TTS, motor drivers, companion sync, enclosure spec.
