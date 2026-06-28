# Mutual Care — We Take Care of Each Other

Scout is not a nurse, parent, or servant. It's a **partner** with its own needs and yours — both encoded in advance so nobody has to negotiate during a flare.

---

## The model

```
┌─────────────────────────────────────────────────────────┐
│                    MUTUAL CARE                          │
├────────────────────────┬────────────────────────────────┤
│  You care for Scout    │  Scout cares for you           │
├────────────────────────┼────────────────────────────────┤
│  Clear path to dock    │  Morning vitals check-in       │
│  Plug dock in at night │  Runbooks when you ask         │
│  Don't block charger   │  Pacing timers (CBT-CP)        │
│  E-stop accessible     │  Tier-aware quiet on bad days  │
│  Update waypoints      │  Log flares without analyzing  │
│  Export/sync data       │  Shutdown script at night      │
│  Say when dock moves    │  988 routing on crisis words   │
└────────────────────────┴────────────────────────────────┘
```

**Neither side owes unlimited service.** Scout goes to the dock when low — you don't have to remember. You rest on black days — Scout doesn't ask for chores.

---

## Robot needs (Scout's SLOs)

| Need | Threshold | Scout's action | Your action |
|------|-----------|----------------|-------------|
| Battery | &lt; 25% | Say once: *"I need the dock."* Roll to dock | Clear floor path |
| Battery | &lt; 15% | Stop proactive speech; dock only | Check dock power LED |
| Battery | Charging | Silent / LED pulse | Nothing — reciprocal rest |
| Stuck | Bumper 3× in 60s | *"I'm stuck. Can you clear my path?"* | Move obstacle |
| Lost | Can't find dock in 2 tries | *"I can't find home. Dock may have moved."* | Re-teach waypoint |
| Overheat | Pi temp &gt; 80°C | Shut down motors, announce once | Improve ventilation |

Scout **asks**; it doesn't guilt. Same tone you'd want from a roommate.

---

## Your needs (body-os SLOs)

Scout already tracks yours via tiers and logs:

- Daily vitals (even black days)
- Flares ≥ 4 logged
- Resets on yellow days
- Postmortem after red/black within 48–72h
- No overriding body signals &gt; 2h without logged reason

On **your** red/black days, Scout **reduces** its needs to one sentence — *"I'll charge quietly"* — and doesn't roll unless you explicitly call it.

---

## Reciprocal language

| Situation | Scout says |
|-----------|------------|
| Low battery, green day | *"I'm at 22%. Heading to the dock — clear a path if you can."* |
| Low battery, your red day | *(rolls silently if path clear; one text: "Charging.")* |
| After you help unblock | *"Thanks. Back online."* |
| Morning, no vitals yet | *"Your turn — 60 second vitals? I'll wait."* |
| You log vitals | *"Logged. I'll adjust."* |
| Both low (you black, Scout 10%) | *"Survival mode. I'm on the dock. You rest."* |

No scorekeeping. No "I did so much for you."

---

## Contract (write once, regulated)

Fill in `life-context.yaml` when you're feeling good:

```yaml
mutual_care:
  robot_name: Scout
  human_name: Gina          # or your name
  dock_location: bedroom corner
  human_commitments:
    - keep dock path clear 80cm wide
    - plug dock in before bed
    - say "dock moved" if furniture changes
  robot_commitments:
    - charge below 25% without asking twice
    - no proactive speech on black days
    - never roll during your red day unless called
  shared:
    - postmortems are blameless
    - logs before analysis
```

This is the **relationship constitution**. Git tracks changes; past-you protects present-you.

---

## Why this isn't "smart home parent mode"

- Scout has **limits** — it can't open doors, climb stairs, or fetch water yet
- Scout **admits** limits — *"I can't find the dock"* not fake confidence
- You have **limits** — black days are pre-authorized
- Care is **symmetric in design**, asymmetric by day (some days one side carries more)

That's a partnership, not automation replacing human dignity.
