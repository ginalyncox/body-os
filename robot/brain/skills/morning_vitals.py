from __future__ import annotations

from datetime import datetime

from ..config import RobotConfig
from ..data.store import DataStore
from ..state import SessionState
from ..voice.orchestrator import VoiceOrchestrator


def suggest_tier(pain: int, energy: int, sleep: float, autonomic: str) -> str:
    if pain >= 9 or (autonomic == "Hijacked" and pain >= 7):
        return "black"
    if pain >= 7 or energy <= 3 or autonomic in ("Hijacked", "Activated"):
        return "red"
    if pain >= 4 or energy <= 5 or sleep < 6 or autonomic == "Edgy":
        return "yellow"
    if pain <= 3 and energy >= 6 and sleep >= 6 and autonomic == "Calm":
        return "green"
    return "yellow"


class MorningVitalsSkill:
    def run(self, voice: VoiceOrchestrator, store: DataStore, config: RobotConfig, state: SessionState) -> None:
        voice.say("Morning vitals. Sixty seconds. No analysis.", force=True)

        sleep_raw = voice.ask("Sleep hours last night?")
        try:
            sleep_hours = float(sleep_raw)
        except ValueError:
            sleep_hours = 7.0

        pain_raw = voice.ask("Morning pain, one to ten?")
        try:
            pain = int(pain_raw)
        except ValueError:
            pain = 5

        energy_raw = voice.ask("Morning energy, one to ten?")
        try:
            energy = int(energy_raw)
        except ValueError:
            energy = 5

        autonomic = voice.ask("Autonomic state? Calm, Edgy, Activated, or Hijacked?")
        if autonomic not in ("Calm", "Edgy", "Activated", "Hijacked"):
            autonomic = "Edgy"

        tier = suggest_tier(pain, energy, sleep_hours, autonomic)
        state.set_tier(tier)
        config.save_tier(tier)

        from datetime import datetime
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

        voice.say(
            f"Logged. {tier.capitalize()} day. "
            f"Pain {pain}, energy {energy}. I'll adjust how much I talk.",
            force=True,
        )

        if tier == "yellow":
            voice.say("Yellow is the dangerous tier. I'll remind you about resets, not heroics.", force=True)
        elif tier == "red":
            voice.say("Red day. I'm here when you need me. Survival floor only.", force=True)
        elif tier == "black":
            voice.say("Black day. Past-you already decided you don't have to function today.", force=True)
