from __future__ import annotations

from ..config import RobotConfig
from .stt import SpeechToText, create_stt
from .tts import TextToSpeech, create_tts


class VoiceOrchestrator:
    def __init__(self, config: RobotConfig) -> None:
        self.config = config
        self.tts: TextToSpeech = create_tts(config.tts_engine, config.name)
        self.stt: SpeechToText = create_stt(config.stt_engine)

    def say(self, text: str, force: bool = False) -> None:
        if not force and self.config.tier == "black":
            # Black day: only speak if forced (crisis, explicit flow)
            return
        self.tts.speak(text, rate=self.config.tier_rate(), volume=self.config.voice_volume)

    def ask(self, prompt: str) -> str:
        self.say(prompt, force=True)
        return self.stt.listen()

    def listen(self) -> str:
        return self.stt.listen()
