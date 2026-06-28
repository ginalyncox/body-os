from __future__ import annotations

from ..voice.orchestrator import VoiceOrchestrator


class CrisisSkill:
    def run(self, voice: VoiceOrchestrator) -> None:
        voice.say(
            "I hear you. Nine eight eight is available — call or text, twenty-four seven. "
            "I'm staying quiet unless you want me.",
            force=True,
        )
