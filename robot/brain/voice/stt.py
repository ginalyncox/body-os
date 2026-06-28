from __future__ import annotations

from abc import ABC, abstractmethod


class SpeechToText(ABC):
    @abstractmethod
    def listen(self, prompt: str = "") -> str:
        ...


class ConsoleSTT(SpeechToText):
    """Simulation — reads typed input as 'speech'."""

    def listen(self, prompt: str = "") -> str:
        if prompt:
            print(f"   [{prompt}]")
        try:
            return input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            return "quit"


def create_stt(engine: str) -> SpeechToText:
    if engine == "console":
        return ConsoleSTT()
    return ConsoleSTT()
