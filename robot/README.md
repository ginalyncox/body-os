# body-os Assistive Robot

A rolling, talking assistive aid that runs **body-os** protocols and **CBT-CP** skills on your behalf — calmly, predictably, without improvisation during flares.

> *"Logs before analysis. Runbooks over improvisation."* — but spoken, at 2 AM, when you can't read a screen.

## What this robot does

| Capability | Source |
|-----------|--------|
| Morning vitals check-in | body-os Daily Vitals |
| Tier-aware behavior | Green / yellow / red / black protocols |
| Voice-guided resets & runbooks | `scripts/` + `runbooks/` |
| Pacing timers & break reminders | CBT-CP Session 4 (Exercise & Pacing) |
| Cognitive reframing prompts | CBT-CP Session 8–9 + doom-loop runbook |
| Relaxation breathing | CBT-CP Session 5 + reset scripts |
| Evening shutdown | `scripts/shutdown.md` |
| Flare logging | body-os Flare Log schema |
| Crisis routing | 988 on doom-loop / black-day escalation |

## What it does NOT do

- Diagnose or change medications
- Nag on black days (survival floor only)
- Make decisions about money, work, or relationships while you're symptomatic
- Replace your clinician or CBT-CP therapist

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│  You (voice)  ←→  Brain (Python)  ←→  Companion app    │
│                      │                                   │
│              ┌───────┴───────┐                           │
│              │  Skills layer │  vitals, pacing, flows   │
│              └───────┬───────┘                           │
│                      │                                   │
│         ┌────────────┼────────────┐                    │
│         ▼            ▼            ▼                    │
│      Voice I/O    State store   Motor driver           │
│    (mic/speaker)  (JSON/local)  (wheels / mock)        │
└─────────────────────────────────────────────────────────┘
```

## Quick start (no hardware)

Simulate the robot in your terminal — text in, spoken-style prompts out:

```bash
cd robot
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp config.example.yaml config.yaml
python -m brain --simulate
```

Try:
- `help` — list commands
- `morning` — daily vitals check-in
- `reset` — guided reset-60s
- `hijacked` — autonomic spike runbook
- `pacing start study 25` — 25-minute pacing block (CBT-CP)
- `tier yellow` — switch tier (changes how the robot talks)
- `come here` — simulate rolling to you

## Quick start (with hardware)

See [docs/hardware.md](docs/hardware.md) for the full bill of materials and build tiers.

Minimum rolling stack:
1. Raspberry Pi 4/5 (4 GB+)
2. USB conference mic + small powered speaker
3. 2-wheel differential-drive chassis + motor HAT
4. 12V battery pack (≥ 10 Ah)
5. Optional: smart-plug for lamp dimming per `infrastructure/environment-defaults.md`

```bash
# On the Pi
pip install -r requirements.txt
cp config.example.yaml config.yaml
# Edit config: set motor.driver to "gpio" or "serial", set your wake word
python -m brain
```

## Configuration

Copy `config.example.yaml` → `config.yaml`:

```yaml
robot:
  name: "Scout"           # what you call it
  wake_words: ["scout", "hey scout"]

voice:
  tts_engine: "console"   # console | edge | pyttsx3
  stt_engine: "console"   # console | whisper | google

motor:
  driver: "mock"          # mock | serial | gpio

tier: "green"             # current day tier

companion:
  sync_url: ""            # optional: companion app export endpoint
```

## Personality

The robot is a **calm SRE for your body** — not a cheerleader, not a scold. See [docs/personality.md](docs/personality.md).

On **red/black days** it gets quieter, shorter, and never asks you to do more than the survival floor.

## CBT-CP integration

See [docs/cbt-cp-mapping.md](docs/cbt-cp-mapping.md) for how VA guidebook sessions map to robot skills.

## Project layout

```
robot/
├── README.md
├── config.example.yaml
├── requirements.txt
├── docs/
│   ├── hardware.md
│   ├── personality.md
│   └── cbt-cp-mapping.md
└── brain/
    ├── __main__.py          # python -m brain
    ├── config.py
    ├── state.py             # tier + session state
    ├── router.py            # intent → skill
    ├── voice/
    │   ├── tts.py
    │   ├── stt.py
    │   └── orchestrator.py
    ├── skills/
    │   ├── morning_vitals.py
    │   ├── guided_flow.py
    │   ├── pacing.py
    │   ├── flare_log.py
    │   ├── shutdown.py
    │   └── crisis.py
    ├── motor/
    │   ├── base.py
    │   └── mock.py
    ├── content/
    │   └── flows.json       # scripts + runbooks (voice-ready)
    └── data/
        └── store.py         # local JSON persistence
```

## Roadmap

- [x] v0.1 — Terminal simulation, voice scripts, tier-aware responses
- [ ] v0.2 — Raspberry Pi GPIO motor driver, wake-word detection
- [ ] v0.3 — Companion app sync over local network
- [ ] v0.4 — Room waypoints (kitchen, desk, bedroom) via lidar or beacons
- [ ] v0.5 — Smart-home hooks (dim lights, brown noise on sensory overload)

## License

Same as parent body-os repo.
