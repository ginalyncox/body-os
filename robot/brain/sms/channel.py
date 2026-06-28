from __future__ import annotations

from ..config import RobotConfig


class TextChannel:
    """Captures router output for SMS replies (no microphone)."""

    def __init__(self, config: RobotConfig) -> None:
        self.config = config
        self.messages: list[str] = []

    def say(self, text: str, force: bool = False) -> None:
        if not force and self.config.tier == "black":
            return
        self.messages.append(text)

    def ask(self, prompt: str) -> str:
        self.messages.append(prompt)
        return ""

    def listen(self) -> str:
        return ""
