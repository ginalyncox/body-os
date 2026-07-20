# Purse-portable Scout

Scout as a **carry device** — small pouch, purse, or bag strap. Cellular + GPS + emergency button. No home Wi‑Fi required. Optional rolling dock at home later.

---

## What fits in a purse

| Component | Pick | Notes |
|-----------|------|-------|
| **Brain** | Raspberry Pi Zero 2 W or Pi 4 | Zero 2 W = smaller; Pi 4 = easier dev |
| **LTE + GPS** | Waveshare SIM7600G-H (or Sixfab kit) | Voice + SMS + GNSS on one HAT |
| **SIM** | Prepaid with **voice** (not data-only IoT) | Must dial 911 / 988 |
| **Battery** | 5000–10000 mAh USB-C PD pack | Pass-through charging overnight |
| **Mic** | USB mini mic or HAT with audio | ReSpeaker 2-Mic HAT fits Zero form factor |
| **Speaker** | Small 8Ω + amp HAT, or USB speaker | Keep volume moderate in public |
| **Emergency button** | Red illuminated, panel mount | GPIO 27, hold 2s — accessible through pouch |
| **Enclosure** | Soft pouch + rigid inner plate | Pool noodle edge, no sharp corners |

**Skip in purse build:** wheels, L298N, dock funnel (until you add a home base).

---

## Size target

| Version | Rough size | Weight |
|---------|------------|--------|
| **Zero 2 W + LTE HAT** | ~12 × 8 × 4 cm | ~250 g + battery |
| **Pi 4 + LTE USB dongle** | ~15 × 10 × 5 cm | ~400 g + battery |

A **cross-body mini pouch** or **purse organizer sleeve** works. Button faces up or toward you — thumb reach without looking.

---

## Power (wireless + runs while charging)

```
USB-C power bank (pass-through)
    ├── charges from wall at night
    └── powers Pi + LTE HAT all day
```

Pi and LTE **always** on battery bus. Wall only charges the pack. Scout stays awake on the nightstand and in the purse.

---

## Connectivity (no Wi‑Fi needed)

| Function | Link |
|----------|------|
| Daily nudges | Local voice or **SMS via LTE** |
| 911 / 988 / contacts | **LTE voice** + GPS |
| Vitals / flare log | Local JSON on SD card |
| Companion sync | Optional Wi‑Fi or Bluetooth when home |

---

## Software

```bash
cp config.example.yaml config.yaml
cp emergency.example.yaml emergency.yaml
# Edit emergency.yaml — contacts, address fallback, dry_run: true

cd robot && python3 setup.py
python3 -m brain --autonomy
```

```yaml
form_factor: portable
emergency:
  enabled: true
  dry_run: true
voice:
  tts_engine: pyttsx3
sync:
  enabled: false
```

---

## Daily carry checklist

- [ ] Power bank charged  
- [ ] LTE antenna not crushed  
- [ ] Red button reachable  
- [ ] `dry_run: false` only after testing with your own number  
- [ ] `gps_fallback_address` filled (home + campus) for indoor GPS gaps  

---

## Home vs go

| Location | Scout |
|----------|-------|
| **In purse** | Nudges, flare log, emergency button, 911/988 |
| **On nightstand** | Charging via power bank, shutdown script, morning vitals |
| **At desk** (optional) | Wi‑Fi sync to companion app |
| **Rolling dock** (later) | `form_factor: rolling` — separate phase |

---

## One sentence

> Purse Scout is a **medical-alert-class cellular companion** that also knows your body-os tiers — small enough to always be on you, independent of home Wi‑Fi.

See also: [emergency.md](./emergency.md), [parts-list.md](./parts-list.md)
