from __future__ import annotations

from abc import ABC, abstractmethod


class TextToSpeech(ABC):
    @abstractmethod
    def speak(self, text: str, rate: int = 150, volume: float = 0.8) -> None:
        ...


class ConsoleTTS(TextToSpeech):
    """Simulation — prints robot speech with prefix."""

    def __init__(self, name: str = "Scout") -> None:
        self.name = name

    def speak(self, text: str, rate: int = 150, volume: float = 0.8) -> None:
        print(f"\n🤖 {self.name}: {text}\n")


class EdgeTTS(TextToSpeech):
    """Microsoft Edge TTS — free, good quality. Requires edge-tts package."""

    def __init__(self, voice: str = "en-US-AriaNeural") -> None:
        self.voice = voice

    def speak(self, text: str, rate: int = 150, volume: float = 0.8) -> None:
        import asyncio
        import tempfile
        import subprocess

        async def _gen() -> str:
            import edge_tts
            pct = int((rate - 150) / 1.5)  # edge uses +N% or -N%
            communicate = edge_tts.Communicate(text, self.voice, rate=f"{pct:+d}%")
            path = tempfile.mktemp(suffix=".mp3")
            await communicate.save(path)
            return path

        path = asyncio.run(_gen())
        subprocess.run(["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", path], check=False)


def create_tts(engine: str, name: str = "Scout") -> TextToSpeech:
    if engine == "edge":
        try:
            return EdgeTTS()
        except ImportError:
            print("edge-tts not installed; falling back to console TTS")
    return ConsoleTTS(name=name)
