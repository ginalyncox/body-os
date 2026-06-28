from __future__ import annotations

import threading
import time
from datetime import datetime, timedelta

from ..config import RobotConfig
from ..data.store import DataStore
from ..state import SessionState
from ..voice.orchestrator import VoiceOrchestrator


class PacingSkill:
    """CBT-CP Session 4 — time-based pacing with stop-before-flare."""

    def __init__(self) -> None:
        self._timer: threading.Timer | None = None
        self._warn_timer: threading.Timer | None = None

    def start(
        self,
        voice: VoiceOrchestrator,
        store: DataStore,
        config: RobotConfig,
        state: SessionState,
        activity: str,
        minutes: int,
    ) -> None:
        if config.tier in ("red", "black"):
            voice.say("Not starting pacing on a red or black day.", force=True)
            return

        state.pacing_active = True
        state.pacing_label = activity
        state.pacing_end = datetime.now() + timedelta(minutes=minutes)

        voice.say(
            f"{minutes} minutes for {activity}. "
            f"I'll warn you at {max(1, minutes - 5)} — start stopping then.",
            force=True,
        )

        warn_at = max(0, (minutes - 5) * 60)

        def warn() -> None:
            if state.pacing_active:
                voice.say("Five minutes left. Wind down, don't sprint.", force=True)

        def finish() -> None:
            if not state.pacing_active:
                return
            state.pacing_active = False
            voice.say("Timer. Stop at good enough. Pain one to ten?", force=True)
            pain_raw = voice.listen()
            try:
                pain = int(pain_raw)
            except ValueError:
                pain = -1
            store.add_pacing({
                "activity": activity,
                "minutes": minutes,
                "end_pain": pain,
                "tier": config.tier,
            })
            voice.say("Pacing session logged.", force=True)

        if warn_at > 0:
            self._warn_timer = threading.Timer(warn_at, warn)
            self._warn_timer.daemon = True
            self._warn_timer.start()

        self._timer = threading.Timer(minutes * 60, finish)
        self._timer.daemon = True
        self._timer.start()

    def stop(self, voice: VoiceOrchestrator, state: SessionState) -> None:
        state.pacing_active = False
        if self._timer:
            self._timer.cancel()
        if self._warn_timer:
            self._warn_timer.cancel()
        voice.say("Pacing stopped early.", force=True)
