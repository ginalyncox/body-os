from __future__ import annotations

import asyncio
import os
import shutil
import subprocess
import tempfile
from abc import ABC, abstractmethod


class TextToSpeech(ABC):
    @abstractmethod
    def speak(self, text: str, rate: int = 150, volume: float = 0.8) -> None:
        ...


class ConsoleTTS(TextToSpeech):
    """Print speech — always available."""

    def __init__(self, name: str = "Scout") -> None:
        self.name = name

    def speak(self, text: str, rate: int = 150, volume: float = 0.8) -> None:
        print(f"\n🤖 {self.name}: {text}\n")


def _play_audio(path: str, volume: float = 0.8) -> bool:
    """Try multiple players; return True if audio played."""
    vol_flag = []
    if shutil.which("ffplay"):
        r = subprocess.run(
            ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", path],
            check=False,
        )
        if r.returncode == 0:
            return True
    if shutil.which("mpg123"):
        r = subprocess.run(["mpg123", "-q", path], check=False)
        if r.returncode == 0:
            return True
    if shutil.which("aplay") and path.endswith(".wav"):
        subprocess.run(["aplay", "-q", path], check=False)
        return True
    # Python fallback
    try:
        import pygame
        pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(max(0.0, min(1.0, volume)))
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        return True
    except Exception:
        pass
    return False


class EdgeTTS(TextToSpeech):
    """Microsoft Edge TTS — free, natural voice. Needs network for synthesis."""

    def __init__(self, voice: str = "en-US-JennyNeural", name: str = "Scout") -> None:
        self.voice = voice
        self.name = name
        self._fallback = ConsoleTTS(name=name)

    def speak(self, text: str, rate: int = 150, volume: float = 0.8) -> None:
        try:
            import edge_tts
        except ImportError:
            print("edge-tts not installed; using console. pip install edge-tts")
            self._fallback.speak(text, rate, volume)
            return

        async def _synth() -> str:
            pct = max(-50, min(50, int((rate - 150) / 1.5)))
            fd, path = tempfile.mkstemp(suffix=".mp3")
            os.close(fd)
            comm = edge_tts.Communicate(text, self.voice, rate=f"{pct:+d}%")
            await comm.save(path)
            return path

        try:
            path = asyncio.run(_synth())
            if not _play_audio(path, volume):
                self._fallback.speak(text, rate, volume)
            try:
                os.remove(path)
            except OSError:
                pass
        except Exception as exc:
            print(f"Edge TTS failed ({exc}); using console.")
            self._fallback.speak(text, rate, volume)


class Pyttsx3TTS(TextToSpeech):
    """Offline system TTS."""

    def __init__(self, name: str = "Scout") -> None:
        self.name = name
        self._fallback = ConsoleTTS(name=name)
        try:
            import pyttsx3
            self._engine = pyttsx3.init()
        except Exception:
            self._engine = None

    def speak(self, text: str, rate: int = 150, volume: float = 0.8) -> None:
        if not self._engine:
            self._fallback.speak(text, rate, volume)
            return
        self._engine.setProperty("rate", rate)
        self._engine.setProperty("volume", volume)
        self._engine.say(text)
        self._engine.runAndWait()


class HybridTTS(TextToSpeech):
    """Speaks aloud via Edge/offline engine AND prints to console."""

    def __init__(self, primary: TextToSpeech, name: str = "Scout") -> None:
        self.primary = primary
        self.console = ConsoleTTS(name=name)

    def speak(self, text: str, rate: int = 150, volume: float = 0.8) -> None:
        self.console.speak(text, rate, volume)
        # Primary already falls back to console on failure — avoid double print
        if not isinstance(self.primary, ConsoleTTS):
            self.primary.speak(text, rate, volume)


def create_tts(
    engine: str,
    name: str = "Scout",
    voice: str = "en-US-JennyNeural",
    hybrid: bool = True,
) -> TextToSpeech:
    primary: TextToSpeech
    if engine == "edge":
        primary = EdgeTTS(voice=voice, name=name)
    elif engine == "pyttsx3":
        primary = Pyttsx3TTS(name=name)
    else:
        primary = ConsoleTTS(name=name)

    if hybrid and engine != "console":
        return HybridTTS(primary, name=name)
    return primary
