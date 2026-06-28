# CBT-CP → Robot Skills Mapping

How the VA **Cognitive Behavioral Therapy for Chronic Pain** Veteran Guidebook and Therapist Manual map to robot behaviors. This robot supports your treatment; it does not replace a trained clinician.

---

## Session map

| CBT-CP Session | Topic | Robot skill | Trigger |
|----------------|-------|-------------|---------|
| 1 | Interview & Assessment | `morning` vitals check-in | Daily AM schedule |
| 2 | Pain education & orientation | Spoken pain-cycle summary on request | *"explain pain cycle"* |
| 3 | Goal planning | SMART goal storage + weekly check | *"goals"* / Sunday PM |
| 4 | Exercise & pacing | `pacing` timer + activity log | *"pacing start …"* |
| 5 | Relaxation training | Guided breath in all reset scripts | `reset`, `reset-deep` |
| 6–7 | Pleasant activities | Suggestion prompts on green days | Tier = green, idle |
| 8–9 | Cognitive coping | `doom-loop` runbook + reframe prompts | Crisis keywords / *"doom loop"* |
| 10 | Sleep | `shutdown` script + sleep hygiene reminders | Evening schedule |
| 11–12 | Discharge / booster | Export summary for clinician | *"export week"* |

---

## Pacing (Session 4) — core student skill

CBT-CP time-based pacing: activity → timer → **stop before flare**.

```
You:  "Scout, pacing start study 25"
Scout: "25 minutes, study. I'll tell you at 20 — start stopping then."
  ... at 20 min ...
Scout: "Five minutes left. Wind down, don't sprint."
  ... at 25 min ...
Scout: "Timer. Stop at good enough. Log how you feel — pain 1 to 10?"
You:  "4"
Scout: "Logged. Pacing win."
```

Robot stores pacing sessions in local JSON for weekly review (companion sync in v0.3).

---

## Cognitive coping (Sessions 8–9)

Integrated into `doom-loop` runbook:

1. Name the loop (spoken)
2. Body check (eat, drink, sleep, bathroom)
3. One body need
4. Change input channel
5. **No debate with thoughts**
6. 988 if needed

Robot never argues content of thoughts — matches manual's behavioral approach.

---

## Relaxation (Session 5)

All reset scripts use CBT-CP-compatible breathing:

| Script | Pattern | Duration |
|--------|---------|----------|
| reset-60s | Physiological sigh × 4 | 60 s |
| reset-5min | 4 in / 6 out + body scan | 5 min |
| reset-deep | 4 in / 8 out | 20–60 min |
| hijacked runbook | Physiological sigh × 6 | ~2 min |

Robot counts breaths aloud and waits between steps.

---

## body-os + CBT-CP together

```
                    ┌─────────────────┐
                    │   Daily tier    │
                    │  (body-os)      │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
   Protocol rules      CBT-CP skills        Runbooks/scripts
   (allowed/forbidden) (pacing, coping)     (incident response)
```

**Example — yellow day study session:**
- body-os: max 90 min deep work, then reset
- CBT-CP: pacing timer with stop-before-flare
- Robot: runs both — 90 min cap AND 25 min pacing chunks with check-ins

---

## What requires a human clinician

- Initial assessment and diagnosis
- Medication changes
- Trauma processing
- Interpreting questionnaire scores (PCS, PHQ-9, etc.)
- Deciding if CBT-CP is right for you

The guidebook states it should only be used with a trained clinician. This robot implements **skills practice** between sessions, not the full 12-session protocol.
