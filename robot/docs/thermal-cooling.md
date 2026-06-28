# Thermal Management — Outdoor Gyrosphere

> **Status: OUT OF SCOPE** for in-home Scout. Use a Pi heatsink + fan indoors.  
> See [inhome-build.md](inhome-build.md). This file applies only if outdoor gyrosphere returns later.

---

## The honest answer on liquid cooling

| Approach | Verdict for outdoor sphere |
|----------|----------------------------|
| **AIO pump + radiator** (PC style) | ❌ Leak risk, vibration, power draw, pump dies = toast |
| **Mineral oil immersion** | ❌ Servicing nightmare; mic/speaker hate it |
| **Peltier (TEC)** | ❌ Hot side still needs dumping; adds power in heat |
| **Thermosiphon loop** (passive liquid) | ✅ Best *liquid* option — no pump |
| **Heat pipes** | ✅ Passive; not liquid but same job |
| **PCM heat pads** | ✅ Spikes only; pairs with everything |
| **Autonomous "seek cool"** | ✅ **Required** — behavior is layer zero |

**Self** should mean: Scout monitors temp and **acts** — fan on, motors derate, roll to porch shade/dock — not that you refill coolant.

---

## How heat gets trapped

```
     ☀️ sun on shell
        ↓
   plastic absorbs (dark = death)
        ↓
   air inside stagnates (sealed sphere)
        ↓
   Pi + motor driver + battery all radiate into same pocket
        ↓
   throttle → silence → stuck outside → you fetch it (bad for SFN)
```

Goal: **short path from hot chips → shell → outside air**, plus **behavioral escape** when physics loses.

---

## Recommended stack (build in this order)

### Layer 0 — Behavioral (software, $0)

Already fits body-os autonomy:

```yaml
thermal:
  pi_max_c: 78
  internal_max_c: 45
  actions:
    - at 60: fan_pwm 80%
    - at 70: cap motor speed 50%
    - at 78: announce once, roll to porch_dock or shade waypoint
    - at 85: shutdown Pi gracefully, latch until cool
```

Scout says: *"I'm hot. Heading to the porch."* — mutual care for the robot.

Outdoor policy already has `max_temp_c` — thermal extends it with **actions**, not just limits.

### Layer 1 — Passive mechanical ($20–40)

| Part | Role |
|------|------|
| **White / silver shell** | Reflect sun; biggest win |
| **Aluminum spreader plate** under Pi | 3 mm plate bolted to heatsink |
| **Heat pipes** (6 mm, 2×) | Pi plate → shell inner wall "radiator patches" |
| **PCM pads** (phase-change, 45 °C) | Absorb 10–15 min sun spikes |
| **Gore vent** | Pressure equalize; not a dirt highway |

Heat pipes are **vapor inside** — technically liquid cooling, passive, no pump. Good enough for most builds.

### Layer 2 — Active air ($10)

- 40 mm 5 V fan on Pi heatsink
- **Foam duct** to shell vent — don't recirculate hot air inside the ball
- Fan PWM from Pi GPIO via thermal config

### Layer 3 — Thermosiphon loop (advanced, ~$60)

Only if Layer 1–2 fail in **your** patio tests.

```
Pi block → rising hot tube → shell radiator patch (top of internal frame)
                ↓
         falling cool tube → reservoir → Pi block
```

- **No pump** — coolant circulates when hot (water + antifreeze mix, or propylene glycol)
- Radiator patch = aluminum strip **epoxied to inner shell** where equator doesn't roll (internal frame stays oriented)
- **Fill port** at equator flange service gap
- **Leak test** 24 h before sealing sphere

Because the **shell rotates** but the **internal frame stays upright**, radiator patches on the frame (not the shell) work better than sticking fins to the spinning wall.

### Layer 4 — Pumped liquid (not recommended v1)

If you insist: flexible tubing, barbed fittings, **secondary drip tray**, leak sensor GPIO → instant shutdown. Treat like a bomb that rolls.

---

## "Self" cooling = closed-loop thermal autonomy

```
        ┌─────────────┐
        │ DS18B20 /   │
        │ Pi CPU temp │
        └──────┬──────┘
               ↓
        ┌──────────────┐
        │ thermal mgr  │
        └──┬───┬───┬───┘
           │   │   │
     fan PWM  motor  navigation
               derate  → shade/dock
```

| Sensor | Placement |
|--------|-----------|
| Pi CPU | onboard |
| DS18B20 | internal air |
| Optional | motor driver heatsink |

Scout logs `thermal_events.json` for postmortems — same SRE mindset as flares.

---

## Outdoor + SFN pairing

| Your state | Scout thermal policy |
|------------|----------------------|
| Green, 28 °C patio | Normal outdoor session |
| Green, 35 °C | Short sessions; PCM + fan max |
| Yellow | Outdoor max 15 min or stay porch |
| Red / black | **No outdoor roll**; indoor dock only |
| You heat-sensitive (SFN) | Scout doesn't lure you outside in afternoon sun |

The robot avoiding heat **models** pacing — you don't have to be the only system that stops before damage.

---

## Cold side (brief)

LiFePO₄ below 0 °C: don't charge. Config:

```yaml
thermal:
  min_charge_c: 5
  min_operate_c: -10   # shorten sessions; no glass transition on polycarbonate
```

---

## Parts list (thermosiphon + passive, student budget)

| Item | ~Cost |
|------|-------|
| Pi aluminum heatsink + fan | $15 |
| 2× 6×100 mm heat pipe | $12 |
| PCM sheet 45 °C (cut to size) | $18 |
| DS18B20 waterproof probe | $3 |
| Aluminum plate 100×100×3 mm | $8 |
| Gore vent plug | $5 |

Skip pump, reservoir, and fittings until patio logs prove you need them.

---

## Test procedure (patio)

1. Seal sphere with Pi + fan only → log CPU temp every 10 s for 30 min full sun  
2. Add heat pipes → repeat  
3. Add PCM → repeat  
4. If still throttling at 78 °C → design thermosiphon  
5. Enable behavioral retreat → confirm Scout reaches porch dock before shutdown  

**Pass:** 20 min green-tier outdoor session without throttle.

---

## What not to do

- Dark paint on outdoor shell  
- Seal with zero venting  
- Run motors full torque when Pi is at 75 °C  
- Liquid loop with **rotating** joints at the equator (leak guaranteed)  
- Expect PC watercooling ethos in a ball that falls off a curb  

---

## Relation to gyrosphere build

See [gyrosphere-outdoor.md](gyrosphere-outdoor.md). Thermal is **Phase B** (weather-ish), after Phase A proves roll on patio.

**Mind unchanged.** Thermal manager is another reflex layer — like low battery → dock.
