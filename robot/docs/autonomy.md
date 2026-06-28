# Autonomy — How Scout Acts Without You

Autonomy here means **executing pre-written protocols on a schedule and on sensor triggers** — not improvising therapy or making medical decisions.

---

## Four layers (bottom = fastest)

```
Layer 4  Mutual care loop     "We both need something"
Layer 3  Scheduled protocols  morning vitals, shutdown, pacing
Layer 2  Tier-gated proactive nudges (green/yellow only)
Layer 1  Reflexes             estop, bumper, low battery → dock
```

Lower layers always win. On a black day, Layer 2–4 shrink; Layer 1 (safety + charge) still runs.

---

## Layer 1 — Reflexes (milliseconds)

| Trigger | Action |
|---------|--------|
| E-stop pressed | Cut motor power immediately |
| Bumper hit | Stop, back up 10 cm |
| Battery &lt; 25% | Interrupt non-critical task → seek dock |
| Battery &lt; 15% | Abort speech mid-sentence → seek dock |
| Pi overheating | Stop motors |

No LLM. No debate.

---

## Layer 2 — Tier-gated proactive (minutes)

Only when `tier` is **green** or **yellow**:

| Time | Action |
|------|--------|
| Schedule `morning_vitals` | *"Your turn — vitals?"* (once) |
| Schedule `midday_reset` | Green only: *"5-minute reset?"* |
| Schedule `shutdown` | Run shutdown script offer |
| Pacing timer end | CBT-CP stop prompt |
| 90 min work (yellow) | *"Yellow day — reset?"* |

**Red/black:** Layer 2 disabled except pacing timer completion (soft chime only).

---

## Layer 3 — Scheduled protocols

Configured in `config.yaml` → `schedule:`.

Autonomy loop wakes every 30s, checks:
1. Current tier allows action?
2. Already done today? (check store)
3. Battery OK to roll? (if rolling needed)
4. Execute or skip

---

## Layer 4 — Mutual care loop

Every 5 minutes the brain checks **both** sides:

```python
# Pseudocode — implemented in brain/autonomy/care_loop.py
if scout.battery < 25% and not scout.charging:
    scout.seek_dock(priority="high")

if human.tier == "black":
    scout.quiet_mode = True

if scout.charging and human.tier in ("red", "black"):
  pass  # both resting — no prompts

if not human.vitals_today and hour >= morning_hour:
    scout.ask_vitals_once()
```

---

## Autonomy modes (`config.yaml`)

```yaml
autonomy:
  enabled: true
  check_interval_seconds: 30
  proactive: true          # Layer 2
  mutual_care: true        # Layer 4
  roll_when_charging: true # Scout goes to dock alone
```

| Mode | Behavior |
|------|----------|
| `proactive: false` | Only responds to wake word |
| `mutual_care: false` | No battery self-care |
| `roll_when_charging: false` | Announce low battery but wait for you |

On **your red days**, set `roll_when_charging: false` if floor clutter is risky — Scout asks instead of rolling.

---

## What autonomy is NOT (yet)

| Not v0.3 | Future |
|----------|--------|
| SLAM / full house mapping | v0.4 lidar waypoints |
| Wake word always listening | v0.3 Porcupine |
| Fetching objects | Needs arm or tray |
| Deciding your medical care | Never |

---

## Simulation

```bash
python3 -m brain --autonomy   # runs care loop in background
```

Watch logs for `[autonomy]` and `[battery]` lines. Test low battery:

```bash
# In config: battery.mock_percent: 20
```

Scout should announce dock need and simulate `go dock`.
