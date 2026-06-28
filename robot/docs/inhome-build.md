# In-Home Scout — Canonical Build Path

**Scope decision:** Scout is an **indoor-only** assistive aid. Kitchen, desk, bedroom, bathroom — not patio, yard, or street.

Outdoor gyrosphere, weather sealing, and GPS are **deferred** (see `archive/` notes in gyrosphere-outdoor.md). This doc is the build that matches body-os as you actually live.

---

## What in-home Scout does

| Room | Behavior |
|------|----------|
| **Bedroom** | Morning vitals, shutdown script, quiet on black days |
| **Desk** | Pacing timers, yellow-day reset nudges |
| **Kitchen** | Rolls to saddle-stool zone; knows standing flares you |
| **Bathroom** | Optional waypoint — only if you want voice there |

Rolls on **hard floor** (wood, tile, low-pile rug). No grass, no curbs, no rain.

---

## Recommended chassis (in-home)

| Option | Cost | Notes |
|--------|------|-------|
| **Wheels + differential drive** | ~$150 | Default — simplest autonomy |
| **Gutted Xbox 360 Slim shell** | ~$10 adapter | Indoor body + Kinect for "come here" |
| **3D-printed cylinder** | filament | See enclosure.md |
| ~~Outdoor gyrosphere~~ | — | Out of scope |

**Brain:** Raspberry Pi 4/5 — always. Never the Xbox motherboard.

---

## Waypoints (your floor plan)

Measure once when regulated. Edit `config.yaml`:

```yaml
environment: inhome

motor:
  waypoints:
    dock:     { x: 0.0, y: 0.0 }   # charge dock — bedroom or desk corner
    desk:     { x: 2.0, y: 0.0 }
    kitchen:  { x: 4.0, y: 3.0 }   # near saddle stool
    bedroom:  { x: 1.0, y: 5.0 }
```

Teach by rolling manually first (mock mode), then dead reckoning, then Kinect person-track (indoor).

---

## Charging dock (in-home)

One dock where Scout sleeps:

- Bedroom corner **or** desk footwell — your call
- 12 V contacts + funnel (see charging-dock.md)
- Xbox 360 power brick is fine as dock PSU
- **You:** keep path clear  
- **Scout:** rolls home below 25%

No porch roof, no IP rating, no sun.

---

## Sensors (in-home only)

| Sensor | Use |
|--------|-----|
| USB mic array | Voice, wake word (later) |
| Speaker | Runbooks, advocate scripts |
| Kinect 360 (optional) | Find you, avoid couch legs |
| Bumper or ultrasonic | Stop before furniture |
| INA219 | Battery % |

Skip: GPS, weather API, Gore vents for rain.

---

## Thermal (in-home)

Pi fan + heatsink is enough. Indoor thermal config:

```yaml
thermal:
  pi_max_c: 80
  fan_gpio: 18
  # No seek_shade — there is no sun indoors
```

See thermal-cooling.md — ignore outdoor/thermosiphon sections unless you revisit scope later.

---

## Tier + rolling policy (unchanged)

| Your tier | Scout rolls? |
|-----------|----------------|
| Green | Yes — kitchen, desk, come here |
| Yellow | Yes — slower, shorter paths |
| Red | Only if you explicitly call |
| Black | No — stationary, whisper mode |

---

## Build phases (in-home)

### Phase 0 — Mind (now)
```bash
cd robot && python3 setup.py && python3 -m brain --autonomy
```

### Phase 1 — Stationary voice (~$100)
Pi + mic + speaker at desk. No wheels. Validates voice + sync + mutual care.

### Phase 2 — Wheels (~$150)
Motor kit, indoor speed cap 0.3 m/s, bumper, e-stop on controller.

### Phase 3 — Dock + autonomy
Charge contacts, `battery.mock_percent: 22` test, Scout seeks dock.

### Phase 4 — Optional Kinect
"Come here" tracks you in the living room / kitchen.

---

## Xbox 360 pile (in-home use)

| Part | Use |
|------|-----|
| Kinect | Indoor person track |
| Slim shell | Robot body |
| Power brick | Dock PSU |
| Controller | E-stop |

Full guide: [xbox360-salvage.md](xbox360-salvage.md)

---

## Advocate (in-home)

Scout speaks pre-written scripts — accommodations, "I need to lie down," boundary with visitors. No wind, no GPS. Phone relay optional.

Advocate templates: `robot/advocacy/` (roadmap — fill when regulated).

---

## Out of scope (explicit)

- Outdoor / patio / lawn
- Weather sealing IP54+
- Gyrosphere (unless you prototype **indoor** ball on hard floor later — still in-home)
- Street geofence
- Solar charging

Files kept for future reference: `gyrosphere-outdoor.md`, outdoor sections of `thermal-cooling.md`.

---

## One sentence

> Scout lives where you live — same rooms, same tiers, same runbooks — and rolls on floors you already trust.
