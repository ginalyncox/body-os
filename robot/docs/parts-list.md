# Parts List — In-Home Scout

Buy in **phases**. Phase 0–1 works without wheels. Full rolling + self-charge is Phase 1 + 2 + 3.

**You already have:** Xbox 360 consoles → see [Salvage from your pile](#salvage-from-your-xbox-360-pile).

---

## Phase 0 — Brain only ($0)

| Part | Qty | Notes |
|------|-----|-------|
| Laptop or existing PC | 1 | Run `python3 -m brain --simulate` |
| USB speaker (optional) | 1 | Hear Edge TTS while testing |

Nothing to buy.

---

## Phase 1 — Stationary Scout (~$95–130)

Talks, syncs with companion app, mutual care. Sits on desk or nightstand.

| Part | Qty | Est. | Example / spec |
|------|-----|------|----------------|
| **Raspberry Pi 4 (4 GB)** or **Pi 5 (4 GB)** | 1 | $55–80 | Brain — do not use Xbox motherboard |
| **microSD card** 32 GB+ | 1 | $8 | Class A2; flash Raspberry Pi OS |
| **Official Pi PSU** USB-C | 1 | $12 | 5 V 3 A (Pi 4) or 5 V 5 A (Pi 5) |
| **USB mic** | 1 | $15–40 | ReSpeaker 2-Mic USB, or Jabra Speak 410 |
| **Small speaker** | 1 | $15–25 | 3.5 mm or USB; Anker Soundcore Mini class |
| **Pi case + heatsink** | 1 | $10 | Optional fan for continuous run |

**Subtotal:** ~$95–130

**Cables:** USB-A extensions if mic/speaker cables are short.

---

## Phase 2 — Rolling base (~$120–180)

Adds wheels, indoor autonomy, manual e-stop.

| Part | Qty | Est. | Example / spec |
|------|-----|------|----------------|
| **2WD robot chassis kit** | 1 | $25–45 | TT motors + acrylic plate, or gearmotor kit |
| **L298N motor driver** | 1 | $5 | Or Adafruit DC Motor HAT (stacked on Pi) |
| **12 V LiFePO₄ battery** | 1 | $35–55 | 6 Ah minimum; safer indoors than bare LiPo |
| **BMS** (if not in pack) | 1 | $8 | 12 V LiFePO₄ protection |
| **5 V buck converter** | 1 | $6 | 12 V → 5 V 3 A for Pi from battery |
| **Jumper wires** | 1 set | $5 | Pi GPIO → driver |
| **E-stop button** (NC) | 1 | $8 | Cuts motor power in series |
| **Micro bumpers** (optional) | 2 | $6 | Front contact switches |
| **HC-SR04 ultrasonic** (optional) | 1 | $3 | Slow near furniture |
| **Plywood base plate** | 1 | $5 | Mount Pi + battery; bolt chassis |
| **Pool noodle slice** | 1 | $0 | Front soft bumper |

**Subtotal:** ~$120–180 (with Phase 1 Pi)

**From Xbox pile:** wireless controller + **USB adapter** (~$15 if you don’t have one) → manual drive + e-stop mapping.

---

## Phase 3 — Self-charging dock (~$35–55)

Scout rolls home below 25% battery.

| Part | Qty | Est. | Example / spec |
|------|-----|------|----------------|
| **12 V 5 A wall PSU** | 1 | $12 | Dedicated dock circuit |
| **Copper charge strips** or **pogo pins** | 2 sets | $8 | Robot rear + dock fixed contacts |
| **INA219** current sensor (I²C) | 1 | $4 | Pi knows charging state |
| **Charge funnel** | 1 | $0–5 | Print `enclosure/dock-funnel.scad` |
| **14 AWG wire + fuse** 5 A | 1 | $8 | Between PSU and contacts |
| **TP4056** or charge indicator LED | 1 | $3 | Visible “charging” |
| **Spring contacts** (robot side) | 2 | $6 | Self-align on dock |

**From Xbox pile:** one **360 power brick** can replace wall PSU if rewired carefully (see xbox360-salvage.md).

**Subtotal:** ~$35–55

---

## Phase 4 — “Come here” (optional, ~$10–25)

Indoor person tracking — only if you have or get a Kinect.

| Part | Qty | Est. | Example / spec |
|------|-----|------|----------------|
| **Kinect for Xbox 360** | 1 | $0 | From your pile |
| **Kinect USB power adapter** | 1 | $10 | Required for original 360 Kinect on Pi |
| **USB extension** 6 ft | 1 | $8 | Kinect on Scout “head” |

Skip if no Kinect — waypoints still work.

---

## Enclosure (pick one)

| Option | Parts | Est. |
|--------|-------|------|
| **A. Minimal** | Zip ties + plywood base only | $0 |
| **B. 3D print** | Filament for `enclosure/scout-body.scad` | ~$15 PETG |
| **C. Xbox Slim shell** | 1 gutted Slim + standoffs + base plate | $0 salvage |

| Part | Qty | Notes |
|------|-----|-------|
| M3 standoffs + screws | 8 | Pi to base |
| M2.5 standoffs | 4 | Pi to shell |
| Velcro strap | 1 | Battery to base (removable) |

---

## Salvage from your Xbox 360 pile

| From pile | Replaces buying | Saves |
|-----------|-----------------|-------|
| Kinect 360 | Phase 4 sensor | ~$30–80 |
| Slim console shell | Enclosure C | ~$40 |
| Power brick | Dock PSU | ~$12 |
| Wired/wireless controller + USB dongle | Manual override | ~$20 |
| Internal fan | Pi cooling in shell | ~$5 |

**Recycle:** motherboards, DVD drives (e-waste).

---

## Tools

| Tool | Need |
|------|------|
| Soldering iron + solder | Charge contacts, GPIO |
| Multimeter | Verify 12 V / 5 V rails |
| Screwdrivers M2/M3 | Chassis |
| Wire strippers | Power wiring |
| 3D printer or makerspace | Dock funnel, optional shell |

---

## Total estimates

| Build | Parts cost (new) | With Xbox salvage |
|-------|------------------|-------------------|
| Phase 1 only (stationary) | ~$100 | ~$100 |
| Phase 1 + 2 (rolls, manual charge) | ~$250 | ~$230 |
| Phase 1 + 2 + 3 (self-dock) | ~$290 | ~$260 |
| Full + Kinect | ~$320 | ~$270 |

---

## Minimum order (if buying once)

**Starter kit** — Phase 1 + 2 in one cart:

1. Raspberry Pi 4/5 kit (Pi + PSU + SD + case)
2. USB mic array
3. Small speaker
4. 2WD chassis + L298N
5. 12 V LiFePO₄ 6 Ah + buck converter
6. E-stop button
7. Jumper wire kit

Add Phase 3 dock parts when rolling works on your floor.

---

## Do NOT buy (in-home scope)

- GPS module
- Outdoor-rated enclosures / Gore vents
- LiPo without BMS
- Gyrosphere shell / pendulum drive
- Lidar (until Phase 4+ indoor mapping desire)

---

## After parts arrive

1. `cd robot && python3 setup.py`
2. Phase 1: Pi on desk — `python3 -m brain --autonomy`
3. Phase 2: wire motors — `motor.driver: gpio` in `config.yaml`
4. Measure floor — set `motor.waypoints`
5. Phase 3: build dock — test `battery.mock_percent: 22`

See [inhome-build.md](inhome-build.md).
