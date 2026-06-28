from __future__ import annotations

from datetime import datetime

from ..config import RobotConfig
from ..data.store import DataStore
from ..sms.channel import TextChannel
from ..state import SessionState
from .morning_vitals import suggest_tier


def run_morning_sms(
    tokens: list[str],
    channel: TextChannel,
    store: DataStore,
    config: RobotConfig,
    state: SessionState,
) -> bool:
    """
    One-line morning vitals for SMS:
    morning SLEEP PAIN ENERGY calm|edgy|activated|hijacked
  Example: morning 7 5 4 edgy
    """
    if len(tokens) < 5:
        channel.say(
            "Morning vitals format: morning SLEEP PAIN ENERGY calm|edgy|activated|hijacked\n"
            "Example: morning 7 5 4 edgy",
            force=True,
        )
        return True

    try:
        sleep_hours = float(tokens[1])
        pain = int(tokens[2])
        energy = int(tokens[3])
    except ValueError:
        channel.say("Numbers needed: morning SLEEP PAIN ENERGY autonomic", force=True)
        return True

    autonomic = tokens[4].capitalize()
    if autonomic == "Hijacked":
        autonomic = "Hijacked"
    elif autonomic not in ("Calm", "Edgy", "Activated", "Hijacked"):
        autonomic = "Edgy"

    tier = suggest_tier(pain, energy, sleep_hours, autonomic)
    state.set_tier(tier)
    config.save_tier(tier)

    store.add_vitals({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "tier": tier,
        "sleep_hours": sleep_hours,
        "sleep_quality": 3,
        "morning_pain": pain,
        "morning_energy": energy,
        "autonomic_state": autonomic,
    })
    store.mark_task_done("vitals")

    channel.say(
        f"Logged. {tier.capitalize()} day. Pain {pain}, energy {energy}.",
        force=True,
    )
    return True
