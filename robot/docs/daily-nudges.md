# Daily task nudges

Scout reminds you about **minimum daily completes** — including hygiene on hard days — without guilt or parenting tone. Peer-level mutual care: small wins count.

---

## What gets nudged

Tasks come from body-os tier protocols (`protocols/*.md`). Examples:

| Task | Green / yellow | Red | Black |
|------|----------------|-----|-------|
| Vitals | ✓ | ✓ | ✓ |
| Water (slots) | ✓ | ✓ | ✓ |
| Meds | ✓ | ✓ | ✓ |
| Bathroom | ✓ | ✓ | ✓ |
| Brush teeth | ✓ | ✓ (once OK) | — |
| Wash face | ✓ | ✓ | — |
| Meals | ✓ | ✓ | — |
| Midday reset | green/yellow | — | — |
| Reset-deep | ✓ | ✓ | — |
| Shutdown | ✓ | ✓ | ✓ |

Edit schedules in `brain/content/daily_tasks.json`.

---

## How nudges work

1. **Autonomy loop** (`care_loop.py`) checks every 30s (configurable).
2. For each task whose scheduled time has passed and isn't marked done, Scout may speak once.
3. **Cooldown:** same task won't repeat within `min_minutes_between` (default 60 min).
4. **Tier behavior:**
   - **Green / yellow:** full schedule, conversational nudges.
   - **Red:** survival floor wording — bathroom, teeth once, water, meds.
   - **Black:** silent by default; only water/meds/bathroom if you enable `nudge_on_black`.

Nudges pause while Scout is seeking the charging dock.

---

## Voice commands

| Command | Action |
|---------|--------|
| `tasks` | List what's still open for your tier |
| `done teeth` | Mark brush-teeth slot done |
| `done water` | Mark current water slot done |
| `done bathroom` | Mark bathroom slot done |
| `done meds` | Mark meds done |
| `morning` | Vitals check-in (auto-marks vitals) |

Aliases: `done brush`, `done sip`, `done wc`, etc.

---

## Companion app

Home screen shows **Daily minimums** — tap **Done** to check off. Syncs with the robot via `/api/sync` (`dailyCompletions` field).

---

## Configuration

```yaml
daily_tasks:
  enabled: true
  min_minutes_between: 60
  nudge_on_red: true
  nudge_on_black: false
```

Run with autonomy:

```bash
cd robot && python3 -m brain --autonomy
```

---

## Design notes (CBT-CP aligned)

- **No shame language** — "even a quick brush counts on a hard day."
- **Minimum viable** — red/black shrink the list, not your worth.
- **Mutual care** — Scout also seeks the dock when low; you keep paths clear.
- **Logs before analysis** — completions are data, not grades.
