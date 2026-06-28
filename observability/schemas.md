# Observability — Database Schemas

The Notion workspace is the runtime; this file is the schema source of truth. If the Notion database drifts, update it from here.

---

## Flare Log

Structured event stream of nervous-system flares. Log first, analyze later.

| Field | Type | Notes |
| :--- | :--- | :--- |
| `Summary` | title | One-line description |
| `Time` | datetime | When the flare started |
| `Severity` | select 1–10 | Color-graded gray→red |
| `Primary Symptom` | select | Burning, Itch, Autonomic spike, Brain fog, Pain, Hijack-feeling, Numbness, GI, Insomnia |
| `Body Region` | multi-select | Hands, Feet, Face, Whole body, Gut, Legs, Chest, Head |
| `Suspected Trigger` | multi-select | Heat, Cold, Standing, Food, Screen, Stress, Sleep debt, Hormonal, Sensory load, Unknown |
| `Doing What` | text | One line of what you were doing at onset |
| `Script Run` | select | reset-60s, reset-5min, reset-deep, shutdown, none |
| `Time to Recover` | text | Filled in retroactively |
| `Hours Slept` | number | Last night |
| `Last Meal Hours Ago` | number | At time of onset |
| `Notes` | text | Free-form |

**Logging rule:** every flare ≥ 4 severity. ≥ 6 is non-negotiable, even retroactively.

---

## Daily Vitals

60-second morning baseline. Low cardinality, high frequency.

| Field | Type | Notes |
| :--- | :--- | :--- |
| `Date Label` | title | YYYY-MM-DD or human label |
| `Date` | date | |
| `Tier` | select | Green, Yellow, Red, Black |
| `Sleep Hours` | number | |
| `Sleep Quality` | select 1–5 | |
| `Morning Pain` | number 1–10 | |
| `Morning Energy` | number 1–10 | |
| `Autonomic State` | select | Calm, Edgy, Activated, Hijacked |
| `Cycle Day` | number | Optional |
| `Notable` | text | One sentence max |

**Logging rule:** every morning, even on black days. Especially on black days.

---

## Known Triggers

Triggers with evidence. Suspects move here once confirmed. Cleared items stay with notes.

| Field | Type | Notes |
| :--- | :--- | :--- |
| `Trigger` | title | |
| `Status` | select | Confirmed, Suspect, Cleared |
| `Category` | select | Environmental, Dietary, Sensory, Postural, Hormonal, Cognitive, Substance |
| `Severity Typical` | select | Low, Moderate, High, Severe |
| `Mechanism` | text | What's happening biologically (best guess) |
| `Evidence Count` | number | Flare Log entries supporting this |
| `First Logged` | date | |
| `Mitigation` | text | What works |
| `Notes` | text | |

**Promotion rule:** 3+ flares with the same suspected trigger → move from Suspect to Confirmed.

### v0.1 seed entries (add manually in Notion)

- **Commercial baker's yeast** — Confirmed, Substance, Moderate. Mannoproteins / β-glucans in dry yeast trigger skin itch. Avoid all skin contact. Use wild starter only.
- **Dry flour on skin** — Confirmed, Environmental, Low–Moderate. Particulate irritation; SFN amplifies. Pour from container, never scoop with bare hands.
- **Prolonged standing** — Confirmed, Postural, High. Autonomic activation from baroreceptor load. Saddle stool deployed for kitchen work.
- **Sleep debt < 6 hrs** — Suspect, Cognitive, High. Pattern observation; needs flare-log correlation.

---

## Kit Inventory

Every tool and accommodation, where it lives, and what it's for.

| Field | Type | Notes |
| :--- | :--- | :--- |
| `Item` | title | |
| `Category` | select | Seating, Kitchen, Sensory, Sleep, Medical, Clothing, Tech, Mobility |
| `Location` | text | Where it lives |
| `Used For` | text | When/why to reach for it |
| `Status` | select | In use, Backup, Need replacement, Wishlist |
| `Notes` | text | |

### v0.1 seed entries (add manually in Notion)

- **Saddle stool** — Seating, Kitchen, In use. For all seated kitchen work including bread.
- **78°F proofing box** — Kitchen, Counter, In use. Sourdough starter home.
- **Long-handled wooden spoon** — Kitchen, Drawer, In use. Mixing dough without hand contact.
- **Silicone spatula** — Kitchen, Drawer, In use. Primary tool for starter feeds.
- **Loop Quiet earplugs (or equivalent)** — Sensory, Pocket carry, In use. Sensory overload runbook.
