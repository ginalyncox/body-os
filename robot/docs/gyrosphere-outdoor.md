# Gyrosphere Scout — Outdoor Rolling Aid

> **Status: OUT OF SCOPE.** Scout is **in-home only** for now. See [inhome-build.md](inhome-build.md) for the active build path.  
> This file is kept if you revisit outdoor later — don't build from it today.

---

## What a gyrosphere actually is

```
        ┌─────────────────────────┐
       /    outer shell (rolls)   \
      │   ┌─────────────────┐    │
      │   │  internal frame  │    │  ← Pi, battery, motors stay
      │   │  (does NOT roll) │    │     mostly upright-ish
      │   │      🤖 Scout      │    │
      │   └────────┬────────┘    │
      │            │ pendulum /   │
      │            │ roller drive │
       \           │              /
        └──────────┴──────────────┘
              ground
```

The **shell spins**; the **brain rides inside** like a hamster that chose computer science.

---

## Drive options (pick one for v1)

| Type | How it works | Outdoor? | Build difficulty |
|------|----------------|----------|------------------|
| **Pendulum drive** | Internal mass swings; gravity rolls ball | OK on hard paths | Medium |
| **Roller drive** | Omni-wheel pressed to inner wall spins shell | Better torque | Medium–hard |
| **Two-motor pendulum** | Two axes of tilt = steerable ball | Best control | Hard |

**Recommendation for first outdoor prototype:** pendulum drive inside a **tough polycarbonate or PETG sphere** (not a cheap hamster ball — they crack in cold and UV).

Research keywords: *pendulum-driven spherical robot*, *BB-8 internal mechanism* (magnetic variant is harder; pendulum is DIY-friendlier).

---

## Outdoor requirements (non-negotiable)

| Hazard | What Scout needs |
|--------|------------------|
| **Rain / dew** | IP54 minimum (splash); sealed cable glands; mic port with Gore vent |
| **Dust / pollen** | Filter on vents; SFN note: pollen is a flare trigger — document it |
| **Sun / heat** | Light shell; heat pipes / thermosiphon; thermal autonomy → porch | See [thermal-cooling.md](thermal-cooling.md) |
| **Cold** | LiFePO₄ battery (better than LiPo in cold); shorten outdoor sessions |
| **Grass / mulch** | Sphere diameter ≥ 50 cm or it buries in soft ground |
| **Gravel / sidewalk gaps** | Mass + traction; internal pendulum needs torque |
| **Wind** | Mic useless in open wind — advocate mode = phone link outdoors |
| **Stuck** | Bumper isn't a sphere edge — use IMU stall detect: "I'm stuck" |

### body-os specific (your body, outside)

| Factor | Design response |
|--------|-----------------|
| **Heat** | SFN + autonomic flares — Scout lists outdoor temp ceiling in config |
| **Standing** | Sphere must **come to you** on patio; you don't fetch it from yard |
| **Sensory load** | Outdoor = high stimuli; yellow/red → **no outdoor autonomy** |
| **Sun / glare** | Kinect/depth struggles in bright sun; use GPS + IMU outdoors instead |

```yaml
# config.yaml — outdoor policy
outdoor:
  enabled: true
  max_tier: yellow          # never auto-out on red/black
  max_minutes: 20           # pacing for the robot too
  max_temp_c: 32
  min_temp_c: 5
  return_to_dock: true      # porch dock, not bedroom
  wind_max_kmh: 25          # above → voice degrades, stay home
```

---

## Size matters outside

| Diameter | Where it works |
|----------|----------------|
| 30 cm | Hard floor only — **not outdoor** |
| 40–50 cm | Firm patio, short grass |
| 60 cm+ | Lawn, light gravel, looks like a lawn ball |

Bigger = more battery space + harder to store. For a student apartment: **porch/patio sphere** first, not full lawn rover.

---

## Shell materials

| Material | Outdoor | Notes |
|----------|---------|-------|
| PETG 3D print (thick) | Fair | UV degrades over months — paint or coat |
| Polycarbonate globe (lighting diffuser) | Good | Hackable hemispheres |
| Rotomolded sphere (custom) | Best | Expensive |
| Dog exercise ball | Bad | Cracks, not IP rated |

Split equator with **bolted flange** + silicone gasket for service access.

---

## Electronics layout (inside the ball)

```
Top (internal "up"):
  USB mic array (foam isolated from shell rumble)
  Status LED visible through frosted window patch

Middle:
  Raspberry Pi 5
  IMU (MPU6050) — essential for steer + stall detect

Bottom (heavy side):
  LiFePO₄ pack (mass helps pendulum anyway)
  Pendulum motor + gearbox
  Motor driver

Sides:
  Small speaker behind acoustic foam
  Optional: GSM/HAT for advocate SMS when phone nearby
```

**Center of mass low** = stable rolling. **Foam isolate** mic/speaker from shell rumble or every voice command sounds like an earthquake.

---

## Outdoor navigation (different from indoor)

Kinect and waypoints **don't work well** outside. Plan for:

| Sensor | Use |
|--------|-----|
| **GPS module** | Porch radius, "stay in yard" geofence |
| **IMU** | Heading, stuck detection, roll rate cap |
| **Ultrasonic** | Low obstacle — curb, chair leg on patio |
| **Optional camera** | Later; sun is painful |

Scout's `go patio` = roll until GPS fence or ultrasonic hit, not kitchen coordinates.

---

## Charging outdoors

Indoor dock doesn't transfer. Options:

1. **Porch dock** — funnel + contacts under a roof overhang (rain-safe)
2. **Manual lift** — you place on dock (bad for SFN on red days — avoid as primary)
3. **Solar trickle** — supplement only; not reliable enough alone

Mutual care: **you** keep the porch dock clear; **Scout** returns below 25% before rain if weather API says storm (v0.5).

---

## Advocate mode outside

Voice advocacy on a windy patio is hard. Outdoor advocate stack:

| Mode | How |
|------|-----|
| **Pre-recorded** | Scout plays your script: accommodations, "I need to sit down" |
| **Phone relay** | Bluetooth to your phone → call/text advocate contact |
| **QR on shell** | Medical info card for strangers (optional) |

Past-you writes scripts in `advocacy/` — Scout plays them; doesn't improvise.

---

## Xbox 360 pile vs gyrosphere

| 360 salvage | Gyrosphere use |
|-------------|----------------|
| Console shell | ❌ Wrong shape |
| Kinect | ❌ Poor in outdoor sun |
| Power brick | ✅ Porch dock PSU |
| Controller | ✅ Manual override while tuning |

The 360 dream shifts to **dock power + bench testing**; the sphere is a new mechanical project.

---

## Build phases (honest timeline)

### Phase A — Roll on patio (goal)
- [ ] 50 cm polycarbonate sphere, pendulum drive, Pi, IMU
- [ ] Scout brain in simulation → then on Pi
- [ ] Hard patio only, 10 min sessions, yellow-tier days only
- [ ] Manual kill switch on controller

### Phase B — Weather-ish
- [ ] Gasket equator, vented mic, LiFePO₄
- [ ] Porch dock with roof
- [ ] Stuck detection + "come back" geofence

### Phase C — Advocate outside
- [ ] Wind-aware voice (defer to phone)
- [ ] Pre-written outdoor advocate scripts
- [ ] Flare log tags `outdoor: true` for correlation

### Phase D — Lawn (optional, hard)
- [ ] 60 cm+ sphere, more torque, grass testing
- [ ] Probably not semester 1

---

## Safety

- **Never** chase into street — geofence hard limit
- **E-stop** on controller cuts motor **and** latches until reset
- **No autonomous outdoor** on red/black human tier
- **Weight limit** — sphere rolling into ankles hurts; cap speed ≤ 0.4 m/s outdoor
- **Pets / people** — ultrasonic slow-down; no silent approach from behind

---

## The honest take

A gyrosphere outside is **buildable** as a patio companion that rolls to you, speaks your scripts, and charges under the porch roof. It is **not** a quick salvage hack like the Xbox shell.

Wheels first teaches autonomy in one weekend. **Sphere teaches physics in one semester.** Both can wear the same Scout mind.

If the gyrosphere is the dream that keeps you building, do it — but **prototype pendulum roll on the patio before you weatherproof your heart.**

---

## Next file to write (when regulated)

`robot/life-context.yaml` → add:

```yaml
outdoor:
  why: "Patio air on green days. Scout rolls with me."
  hard_limits:
    - no street
    - no outdoor when tier red or black
  advocate_outside: "Play script porch-quiet.txt"
```

See also: [hardware.md](hardware.md), [mutual-care.md](mutual-care.md), [autonomy.md](autonomy.md)
