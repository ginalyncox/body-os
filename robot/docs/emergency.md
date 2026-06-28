# Emergency calls — 911, 988, contacts + GPS

Scout as a **purse-portable safety device**: cellular voice, SMS with map links, GNSS, physical red button. Fixed scripts only — no improvisation.

---

## Architecture

```
Red button (GPIO) ──┐
Voice "emergency" ──┼──► EmergencySkill
Crisis keywords ────┘         │
                              ├─► GPS fix (GNSS / fallback address)
                              ├─► SMS each contact (map link)
                              └─► Voice dial 911 or 988
```

**No Wi‑Fi required.** LTE HAT carries voice, SMS, and GPS.

---

## Setup

1. Copy configs:
   ```bash
   cp emergency.example.yaml emergency.yaml
   ```
2. Fill in `emergency.yaml`:
   - `human_name`
   - `gps_fallback_address` (critical indoors / in purse)
   - `contacts` with real E.164 numbers (`+1...`)
   - `medical_context` (SFN, autonomic, accommodations)
3. Keep `dry_run: true` until tested with **your phone** as a contact.
4. Enable in `config.yaml`:
   ```yaml
   emergency:
     enabled: true
     dry_run: true
     config_path: ./emergency.yaml
   ```

---

## Triggers

| Trigger | Result |
|---------|--------|
| **Hold red button** 2s | EMS — contacts SMS + 911 (no cancel window) |
| `emergency` / `sos` | EMS with spoken cancel window |
| `call 911` | EMS |
| `call 988` / crisis keywords | Mental health line |
| `contacts only` | SMS GPS to list only |

---

## Call sequence (EMS)

1. Read GPS (up to 15s). Use `gps_fallback_address` if no fix.  
2. SMS each contact with Google Maps link + medical context.  
3. Optional voice call to contacts who have `voice_call: true`.  
4. Dial **911** and play `voice_ems` script context (when not dry-run).

**988** uses `voice_mental_health` script — separate from EMS.

---

## Hardware

| Part | Role |
|------|------|
| SIM7600G-H (or similar) | LTE voice, SMS, GNSS |
| Voice-capable SIM | 911 / 988 routing |
| GPIO red button | BCM pin 27 default, active low |
| External LTE antenna | Better GPS + signal in purse |

`cellular.driver: sim7600` and `serial_port: /dev/ttyUSB1` in `emergency.yaml`.

---

## Testing (safe order)

1. `dry_run: true` — say `emergency`, check console log  
2. Add your cell as only contact — `dry_run: false` — say `contacts only`  
3. Verify SMS + map link outdoors (GPS fix)  
4. Verify indoor fallback address in SMS  
5. Only then consider live 911 test (many areas allow non-emergency test calls to dispatch non-emergency line — check local policy)

**Never** spam 911 for software testing.

---

## Limits (honest)

| Limit | Mitigation |
|-------|------------|
| DIY ≠ certified medical alert | Treat as best-effort; button + scripts |
| Indoor GPS weak | `gps_fallback_address` |
| E911 auto-location | Read GPS in voice script; SMS map link |
| False triggers | Hold-to-activate button; dry_run default |

---

## Logs

Escalations append to `brain/data/local/emergency_log.json` (last 50 events).

---

## Voice commands

```
emergency
call 911
call 988
contacts only
cancel
```

Purse build: [purse-portable.md](./purse-portable.md)
