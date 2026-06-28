from __future__ import annotations

from ..config import RobotConfig
from ..state import SessionState
from ..voice.orchestrator import VoiceOrchestrator
from .guided_flow import GuidedFlowSkill


class ShutdownSkill:
    def run(self, voice: VoiceOrchestrator, config: RobotConfig, state: SessionState) -> None:
        GuidedFlowSkill().run(voice, config, state, "shutdown")
