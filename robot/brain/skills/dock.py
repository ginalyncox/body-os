from __future__ import annotations

from ..config import RobotConfig
from ..motor import MotorDriver
from ..state import SessionState
from ..voice.orchestrator import VoiceOrchestrator


class DockSkill:
    """Seek charging dock — Scout caring for itself."""

    def seek(
        self,
        voice: VoiceOrchestrator,
        motor: MotorDriver,
        config: RobotConfig,
        state: SessionState,
        *,
        silent: bool = False,
    ) -> bool:
        tier = config.tier
        human_bad_day = tier in ("red", "black")

        if not config.roll_when_charging and human_bad_day:
            if not silent:
                voice.say(
                    "I'm low on battery. I won't roll on your red day — "
                    "can you set me on the dock?",
                    force=not human_bad_day or tier == "red",
                )
            return False

        if not silent:
            if human_bad_day:
                voice.say("Charging.", force=True)
            else:
                voice.say(
                    "I'm heading to the dock. Clear a path if you can.",
                    force=True,
                )

        ok = motor.go_to("dock")
        if ok:
            state.dock_attempts = 0
            if hasattr(motor, "dock_creep"):
                motor.dock_creep()
            if not silent and not human_bad_day:
                voice.say("On the dock. Thanks for keeping the path clear.", force=True)
            return True

        state.dock_attempts += 1
        if state.dock_attempts >= 2 and not silent:
            voice.say(
                "I can't find home. The dock may have moved — "
                "check the waypoint when you're up to it.",
                force=True,
            )
        return False
