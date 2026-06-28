# body-os Assistive Robot

A talking **body-os** companion — **purse-portable** with LTE + GPS + 911/988, or optional **in-home** rolling dock.

> *"Logs before analysis. Runbooks over improvisation."* — but spoken, at 2 AM, when you can't read a screen.

**Primary build:** [docs/purse-portable.md](docs/purse-portable.md) · **Emergency:** [docs/emergency.md](docs/emergency.md)  
**In-home rolling (optional):** [docs/inhome-build.md](docs/inhome-build.md) · **Parts:** [docs/parts-list.md](docs/parts-list.md)

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

```bash
cd robot
python3 setup.py          # creates config.yaml + installs deps
python3 -m brain --simulate
```

With real voice on your laptop:

```bash
pip install edge-tts
# Edit config.yaml: voice.tts_engine: edge
python3 -m brain
```

## Quick start (with hardware)

See [docs/hardware.md](docs/hardware.md) and [docs/enclosure.md](docs/enclosure.md).

```bash
# Raspberry Pi
pip install -r requirements.txt
pip install RPi.GPIO pyserial   # as needed
cp config.example.yaml config.yaml
# Set motor.driver: gpio or serial
python3 -m brain
```

Flash motor firmware: `firmware/scout-motor/scout-motor.ino` → Arduino/ESP32.

## Companion sync

The robot runs a local sync server (default `http://0.0.0.0:8765/api/sync`).

1. Start robot: `python3 -m brain` (sync starts automatically)
2. In companion app → **More → Robot sync**
3. **Push to robot** / **Pull from robot** to merge vitals & flares

Merge is bidirectional by ID/date — nothing is deleted.

## Configuration highlights (`config.yaml`)

```yaml
robot:
  name: Scout              # rename your aid here

voice:
  tts_engine: edge         # real voice
  voice: en-US-JennyNeural
  hybrid: true             # print + speak

motor:
  driver: gpio             # mock | gpio | serial

sync:
  enabled: true
  port: 8765
```

## 3D-printable enclosure

See [docs/enclosure.md](docs/enclosure.md). OpenSCAD source: `enclosure/scout-body.scad`.

## Mutual care & autonomy

Scout and you care for each other — not one-way caregiving.

| Scout's needs | Your needs |
|---------------|------------|
| Charge below 25% | Daily vitals |
| Clear path to dock | Runbooks when flaring |
| Help when stuck | Tier-appropriate quiet |

Docs:
- [docs/inhome-build.md](docs/inhome-build.md) — **canonical indoor build** (wheels, dock, Kinect)
- [docs/mutual-care.md](docs/mutual-care.md) — relationship model
- [docs/autonomy.md](docs/autonomy.md) — how Scout acts alone
- [docs/charging-dock.md](docs/charging-dock.md) — self-charging dock
- [docs/hardware.md](docs/hardware.md) — parts list
- Deferred: [docs/gyrosphere-outdoor.md](docs/gyrosphere-outdoor.md) (out of scope)

```bash
# Simulate low battery → Scout seeks dock
# Set battery.mock_percent: 22 in config.yaml
python3 -m brain --autonomy
```

Fill in `life-context.yaml` from `life-context.example.yaml` when regulated.

## Roadmap

- [x] v0.1 — Terminal simulation, voice scripts, tier-aware responses
- [x] v0.2 — Edge TTS, motor drivers, companion sync, enclosure spec
- [x] v0.3 — Mutual care loop, battery monitor, dock-seek behavior
- [ ] v0.4 — Wake-word + IR/lidar dock alignment
- [ ] v0.5 — Smart-home hooks (dim lights, brown noise)

## Personality

The robot is a **calm SRE for your body** — not a cheerleader, not a scold. See [docs/personality.md](docs/personality.md).

On **red/black days** it gets quieter, shorter, and never asks you to do more than the survival floor.

## CBT-CP integration

See [docs/cbt-cp-mapping.md](docs/cbt-cp-mapping.md) for how VA guidebook sessions map to robot skills.

## Project layout

```
robot/
├── README.md
├── setup.py                 # one-command setup
├── config.example.yaml
├── requirements.txt
├── docs/
│   ├── hardware.md
│   ├── enclosure.md
│   ├── personality.md
│   └── cbt-cp-mapping.md
├── enclosure/
│   └── scout-body.scad      # 3D-printable shell
├── firmware/
│   └── scout-motor/         # Arduino motor firmware
└── brain/
    ├── __main__.py
    ├── sync_server.py       # companion ↔ robot API
    ├── motor/               # mock | gpio | serial
    └── ...
```

## License

Same as parent body-os repo.
