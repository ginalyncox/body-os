# Self-Charging Dock — Hardware & Behavior

Scout finds home, backs onto contacts, and charges without you plugging it in. You keep the path clear; Scout keeps itself powered. Mutual care.

---

## Architecture

```
┌──────────────┐     roll + align      ┌─────────────────┐
│    Scout     │ ──────────────────►  │  Charging dock   │
│  12V battery │ ◄── copper contacts ──│  12V PSU 5A+    │
│  INA219 ADC  │     charge sense      │  guide funnel   │
└──────────────┘                       └─────────────────┘
```

---

## Dock parts list (~$40–80)

| Part | Purpose |
|------|---------|
| 12 V 5 A wall PSU | Dock power (dedicated circuit) |
| 2× copper charge strips | Robot contacts (spring-loaded on robot side) |
| 3D-printed funnel guide | Last 10 cm alignment — see `enclosure/dock-funnel.scad` |
| TP4056 or BMS with charge LED | Visible "charging" from across room |
| INA219 module (I²C) | Pi reads voltage + current |
| Optional: IR LED on dock | Dock beacon for alignment (v0.4) |

**Robot side:** two spring pogo pins or copper strips on rear bumper.  
**Dock side:** fixed contacts + V-shaped funnel so backward driving seats the pins.

---

## Power path

```
Dock PSU 12V ──► charge contacts ──► robot battery ──► BMS ──► buck 5V ──► Pi
                                      │
                                   INA219 (monitor)
```

- Pi runs on battery always; charging doesn't require shutdown
- When current &gt; 200 mA and voltage rising → `charging = true`
- When battery ≥ 90% → `charged = true`, optional leave-dock allowed

---

## Dock waypoint

Add to `config.yaml`:

```yaml
motor:
  waypoints:
    dock: { x: 0.0, y: 0.0 }   # home position — measure your floor
    desk: { x: 1.0, y: 0.0 }
    kitchen: { x: 3.0, y: 2.0 }
```

`dock` is **required** for autonomy. First-time setup: drive Scout manually to dock, mark position, save.

---

## Seek-dock behavior (software)

1. **Announce** once if battery &lt; 25% (tier-aware brevity)
2. **Navigate** to `dock` waypoint (dead reckoning v0.2; IR/lidar v0.4)
3. **Creep** backward slowly last 20 cm (firmware `DOCK` command)
4. **Sense** charge current via INA219
5. If no charge in 30s → retry once, then ask for help
6. **While charging:** silent, LED breathe, no proactive speech

---

## Arduino firmware addition

Add to `scout-motor.ino`:

```
DOCK     → slow reverse 3s (alignment creep)
CHARGE?  → reply CHARGING or IDLE (if charge sense wired)
```

---

## Safety

- Dock in **same room** Scout sleeps — no hallway navigation while low battery
- **No auto-leave dock** below 40% without human OK (configurable)
- **E-stop** cuts charge relay if you add one (recommended)
- **Never** charge LiPo unattended without proper BMS — prefer LiFePO₄ for indoor robots

---

## Your responsibilities (mutual care)

- Plug dock PSU into wall (or smart plug on schedule)
- Keep 80 cm path clear
- Wipe contacts monthly (oxidation)
- Re-teach dock waypoint if furniture moves

## Scout's responsibilities

- Go to dock at 25% without nagging
- Stop asking you to manage its battery
- Tell you clearly when it can't find home

---

## Mock testing (no hardware)

```yaml
battery:
  driver: mock
  mock_percent: 22        # simulate low battery
  mock_charging: false
```

Run `python3 -m brain --autonomy` — Scout should seek dock.
