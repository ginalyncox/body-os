# Xbox 360 Salvage → Scout Robot

You have a pile of Xbox 360s. **Do not run Scout's brain on a 360** — it can't run Python/Linux in any practical way. **Do** strip them for parts that make a rolling aid cheaper and weirder in the best way.

---

## Priority salvage (what to keep)

| Part | Use in Scout | Keep? |
|------|----------------|-------|
| **Kinect (Xbox 360)** | Person tracking, "come here", obstacle depth, dock alignment | **Yes — best part** |
| **Power brick (12 V)** | Dock PSU or bench power (rewired) | Yes, one good unit |
| **Console shell** | Robot body / enclosure | Yes, one intact case |
| **Internal fan** | Pi cooling in tight shell | Yes |
| **Wireless controller + USB adapter** | Manual drive, e-stop override | Optional |
| **Hard drive** | Local log archive on Pi (USB enclosure) | Optional |
| **DVD drive** | — | Recycle |
| **Motherboard / GPU** | — | E-waste recycle |

---

## Scout build roles

```
┌─────────────────────────────────────────┐
│  Pi 5 (brain) — NOT the Xbox motherboard │
│  USB mic + speaker                       │
│  Kinect on top ──► finds you in the room │
├─────────────────────────────────────────┤
│  Hollowed 360 shell OR shell on wheels   │
│  Battery below │ charge contacts rear    │
└─────────────────────────────────────────┘
     Xbox 360 power brick ──► charging dock
```

**Aesthetic:** Scout looks like a repurposed 360 that grew wheels and learned to care about your nervous system. Peer-level robot, not clinical.

---

## Kinect for Xbox 360 (if you have one)

This is the highest-value salvage for autonomy.

| Capability | Scout use |
|------------|-----------|
| Depth map | Don't hit furniture; slow near obstacles |
| Skeleton / body tracking | Roll toward you when you say "come here" |
| Basic person position | Better than dead-reckoning waypoints |

### Pi setup

```bash
# On Raspberry Pi (USB adapter required for original Kinect)
sudo apt install libfreenect-dev python3-freenect
```

Original **Kinect for Xbox 360** needs a **Kinect USB power adapter** (split USB + wall power) — ~$10 used. The Kinect for Windows model has standard USB.

Config hook (future v0.4):

```yaml
sensors:
  kinect:
    enabled: true
    driver: libfreenect
    use_for: [person_track, obstacle_slow]
```

Until software is wired: mount Kinect on Scout's head, cable to Pi, validate with `freenect-glview`.

---

## Power brick repurposing

Xbox 360 external PSU outputs regulated DC on a proprietary plug.

| Model | Rough output | Notes |
|-------|--------------|-------|
| Slim 135 W | 12 V + 5 V rails | Common; verify with multimeter |
| Fat 203 W | Higher current | Heavier |

**For charging dock:** A 12 V brick can feed the dock **if** you:
1. Identify +12 V and GND pins (iFixit / pinout diagrams for your revision)
2. Add a fuse (5 A slow-blow minimum)
3. Never hack mains-side while plugged in

**Do not** power the Pi directly from unknown pins. Use a known 5 V buck from the 12 V rail.

One brick → dock. Keep a second as bench spare.

---

## Console shell as body

### Why it works
- Rounded edges (enclosure doc goal)
- Vents for Pi cooling
- Stable footprint when you add a plywood base + wheels
- Lighter than it looks once gutted

### Gut job (unplugged 24h+)

1. Remove HDD, DVD drive, motherboard, heat sinks
2. Keep front USB port bay for Pi USB extensions (optional)
3. Mount Pi on standoffs on bottom half of shell
4. **Cut or drill** rear panel for charge contacts + cable exit
5. Bolt **plywood base plate** under shell → mount caster wheels or motor kit

### Weight budget
Gutted shell ≈ 1–2 kg. Add battery low. Kinect on top adds ~0.5 kg.

---

## Wireless controller → manual override

Useful when autonomy misbehaves or you're tuning waypoints:

| Button | Action |
|--------|--------|
| A | Acknowledge / stop speech |
| B | E-stop motors |
| Left stick | Manual drive (future firmware) |
| Xbox button | Wake Scout |

Pi: USB wireless receiver (~$15) or wired controller. Map in `config.yaml` under `manual_override` (roadmap).

---

## What to do with the rest

| Leftover | Action |
|----------|--------|
| 9 broken motherboards | E-waste / municipal recycling |
| 8 duplicate shells | Storage bins, donate to makerspace, one backup |
| DVD drives | Scrap metal |
| Cables, AV kits | Drawer |

Label one unit **"Scout donor"** and don't mix parts mid-build.

---

## Suggested allocation (if you have "a ton")

| # | Role |
|---|------|
| 1 | Scout body (gutted shell + wheels) |
| 1 | Parts donor (fans, screws, USB door) |
| 1 | Kinect + adapter test bench |
| 1 | Power brick → dock only |
| Rest | Recycle unless you have multiple Kinects (keep 2: one mounted, one spare) |

---

## Safety

- Open consoles only **unplugged**, capacitors discharged
- Kinect motor tilt can pinch — disable tilt or tape position during bench work
- Lithium robot battery **never** inside unvented closed shell without BMS
- SFN note: soldering fumes → ventilate or have someone else solder if flaring

---

## Student budget impact

| Bought new | Salvaged from 360 pile |
|------------|-------------------------|
| ~$40 enclosure | $0 shell |
| ~$30 depth sensor | $0 Kinect (+ $10 USB adapter) |
| ~$25 12 V PSU for dock | $0 brick |
| **~$95 saved** | toward Pi or battery |

---

## Next steps

1. Inventory: how many have **Kinect ports** on the front? (Kinect sold separately)
2. Buy one **Kinect USB adapter** if needed
3. Gut one Slim model — Slim is easier to work with than Fat
4. Run Scout brain on Pi **beside** the shell first, then integrate

See also: [hardware.md](hardware.md), [enclosure.md](enclosure.md), [charging-dock.md](charging-dock.md)
