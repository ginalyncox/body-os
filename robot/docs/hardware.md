# Hardware Guide — Rolling Assistive Robot

Three build tiers. Start at **Tier 0** (simulation), move up when the brain behaves the way you need.

---

## Tier 0 — Brain only (start here)

**Cost:** $0 (use your laptop)

Run `python -m brain --simulate` from this repo. Validates skills, pacing, runbooks, and tier logic before you buy parts.

**Optional upgrade:** USB speaker plugged into laptop so TTS is audible while you test from bed.

---

## Tier 1 — Stationary talking aid

**Cost:** ~$80–150  
**Goal:** Voice + mic at desk/bedside without wheels.

| Part | Example | Notes |
|------|---------|-------|
| Compute | Raspberry Pi 4 (4 GB) or old phone/tablet | Pi preferred for GPIO later |
| Mic | ReSpeaker USB 2-Mic Array or Jabra Speak | Pickup from across the room |
| Speaker | Anker Soundcore Mini or Pi HDMI audio | Warm, not harsh |
| Power | Pi official USB-C PSU | |

Mount mic + speaker on a small stand. The robot "brain" runs on the Pi; you carry nothing. Good for validating wake-word + TTS in your actual rooms.

---

## Tier 2 — Rolling robot (recommended target)

**Cost:** ~$250–450  
**Goal:** Differential-drive base that rolls to kitchen / desk / bedroom waypoints.

### Chassis options

| Option | Pros | Cons |
|--------|------|------|
| **DIY 2-motor kit** (L298N + TT motors + acrylic plate) | Cheapest, hackable | No encoders; drift over time |
| **Yahboom / Waveshare JetBot-style kit** | Pi HAT included, tutorials | Small payload |
| **Used Roomba / Create 2 base** | Real navigation, battery | Heavier, hacky serial API |
| **Wirecutter-style robot cart** | Stable platform for Pi + battery | You add motors |

For SFN/postural needs: the robot comes **to you** so you don't stand up to fetch reminders.

### Electronics

| Part | Qty | Notes |
|------|-----|-------|
| Raspberry Pi 5 (4–8 GB) | 1 | Or Pi 4 4 GB |
| Motor driver HAT | 1 | Adafruit DC & Stepper HAT, or L298N via GPIO |
| Gearmotors + wheels | 2 | Encoders strongly recommended |
| 12 V LiFePO₄ or SLA battery | 1 | ≥ 10 Ah; separate 5 V buck for Pi |
| USB mic array | 1 | See Tier 1 |
| Powered speaker | 1 | 3.5 mm or Bluetooth |
| Emergency stop button | 1 | Physical kill — wire in series with motor power |
| Bumper switch (optional) | 2 | Front contact stops motors |

### Mechanical

- **Low center of gravity** — battery on the bottom plate
- **Cable management** — no loose wires near wheels
- **Soft bumper** — pool noodle or foam strip on front
- **Max speed cap** in firmware — this is an indoor aid, not a racer (≤ 0.3 m/s)

### Safety requirements (non-negotiable)

1. **E-stop** — one press cuts motor power
2. **Bumper or ultrasonic** — stops on contact
3. **Never auto-drive on red/black tier** — config enforces `motor.allowed_tiers: [green, yellow]`
4. **No stairs** — use only on single level or block doorways

---

## Tier 3 — Room-aware navigation

**Cost:** ~$600–1200+  
**Adds:** LD06 or RPLidar, depth camera, ROS 2 Nav2, mapped waypoints.

Only pursue after Tier 2 works reliably. Mapping kitchen / desk / bed as named waypoints lets you say *"Scout, come to the kitchen"* and it routes around furniture.

---

## Wiring sketch (Tier 2, L298N)

```
Battery 12V ── E-stop ── L298N VCC
                         ├── Motor A → Left wheel
                         └── Motor B → Right wheel

Pi GPIO ── L298N IN1–IN4, ENA, ENB
Pi USB  ── Mic
Pi 3.5mm ─ Speaker (or USB audio)
Pi 5V   ← Buck converter from battery
```

---

## 3D printing / enclosure

- Print or buy a simple cylinder or rounded box — **no sharp edges**
- Speaker faces **up and forward** (voice projects toward you when it rolls up)
- Mic on top, away from speaker cone (reduces echo)
- Status LED: green = idle, amber = listening, red = flare mode, off = black-day quiet

---

## Environment integration (from body-os)

Per `infrastructure/environment-defaults.md`, optional smart-home hooks:

| Trigger | Robot action |
|---------|--------------|
| Sensory overload runbook | Dim lights via smart plug (if configured) |
| reset-deep | Offer to play brown noise on room speaker |
| shutdown script | Dim lights below 50%, remind phone DND |

Use Home Assistant MQTT or Kasa local API — wired in v0.5 roadmap.

---

## Salvage path — Xbox 360 pile ($0 enclosure + sensors)

If you have old Xbox 360 consoles, **don't use them as the brain** — use them as parts:

| Salvage | Scout role |
|---------|------------|
| Kinect for Xbox 360 | Find you in the room, obstacle depth |
| Gutted console shell | Rounded robot body |
| Power brick | Charging dock 12 V supply |
| Controller + USB adapter | Manual override / e-stop |

Full guide: [xbox360-salvage.md](xbox360-salvage.md)

---

## Student budget path

1. Week 1–2: Tier 0 simulation on laptop
2. Month 1: Tier 1 Pi + speaker at desk (~$100)
3. **Salvage:** gut one 360 shell + Kinect if you have it (~$10 USB adapter only)
4. When skills feel right: motor kit + battery (~$150 more)
5. Iterate enclosure — or skip 3D print and use the 360 shell

Borrow a Pi from your university CS/EE lab if available — many have loaner hardware programs.
