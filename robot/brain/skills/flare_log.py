from __future__ import annotations

from datetime import datetime

from ..config import RobotConfig
from ..data.store import DataStore
from ..state import SessionState
from ..voice.orchestrator import VoiceOrchestrator


class FlareLogSkill:
    def run(self, voice: VoiceOrchestrator, store: DataStore, config: RobotConfig, state: SessionState) -> None:
        voice.say("Flare log. Quick version.", force=True)

        sev_raw = voice.ask("Severity one to ten?")
        try:
            severity = int(sev_raw)
        except ValueError:
            severity = 5

        if severity < 4:
            voice.say("Below logging threshold. Still rough. Want reset-60s?", force=True)
            return

        symptom = voice.ask("Primary symptom? Pain, itch, hijacked, brain fog, or other?")
        summary = voice.ask("One line summary?")

        store.add_flare({
            "summary": summary or f"{symptom} flare",
            "severity": severity,
            "primary_symptom": symptom,
            "time": datetime.now().isoformat(),
            "tier": config.tier,
        })

        state.last_flare_severity = severity
        voice.say("Logged. We'll analyze later, not now.", force=True)

        if severity >= 7:
            voice.say("Seven plus. Want me to run reset-deep or a runbook?", force=True)
