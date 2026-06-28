from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = ROOT / "config.yaml"
EXAMPLE_CONFIG = ROOT / "config.example.yaml"


@dataclass
class RobotConfig:
    name: str = "Scout"
    wake_words: list[str] = field(default_factory=lambda: ["scout", "hey scout"])
    personality: str = "sre"
    tier: str = "green"
    tts_engine: str = "console"
    stt_engine: str = "console"
    voice_rate: int = 150
    voice_volume: float = 0.8
    motor_driver: str = "mock"
    motor_allowed_tiers: list[str] = field(default_factory=lambda: ["green", "yellow"])
    motor_max_speed: float = 0.3
    waypoints: dict[str, dict[str, float]] = field(default_factory=dict)
    data_dir: Path = field(default_factory=lambda: ROOT / "brain" / "data" / "local")
    crisis_keywords: list[str] = field(default_factory=list)
    raw: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def load(cls, path: Path | None = None) -> RobotConfig:
        cfg_path = path or DEFAULT_CONFIG
        if not cfg_path.exists():
            cfg_path = EXAMPLE_CONFIG

        with open(cfg_path) as f:
            raw = yaml.safe_load(f) or {}

        flows_path = Path(__file__).parent / "content" / "flows.json"
        crisis: list[str] = []
        if flows_path.exists():
            import json
            with open(flows_path) as ff:
                crisis = json.load(ff).get("crisis_keywords", [])

        robot = raw.get("robot", {})
        voice = raw.get("voice", {})
        motor = raw.get("motor", {})

        data_dir = Path(raw.get("companion", {}).get("data_dir", "./brain/data/local"))
        if not data_dir.is_absolute():
            data_dir = ROOT / data_dir

        return cls(
            name=robot.get("name", "Scout"),
            wake_words=[w.lower() for w in robot.get("wake_words", ["scout"])],
            personality=robot.get("personality", "sre"),
            tier=raw.get("tier", "green"),
            tts_engine=voice.get("ts_engine", voice.get("tts_engine", "console")),
            stt_engine=voice.get("stt_engine", "console"),
            voice_rate=int(voice.get("rate", 150)),
            voice_volume=float(voice.get("volume", 0.8)),
            motor_driver=motor.get("driver", "mock"),
            motor_allowed_tiers=motor.get("allowed_tiers", ["green", "yellow"]),
            motor_max_speed=float(motor.get("max_speed", 0.3)),
            waypoints=motor.get("waypoints", {}),
            data_dir=data_dir,
            crisis_keywords=crisis,
            raw=raw,
        )

    def tier_rate(self) -> int:
        """Slow speech on harder days."""
        mult = {"green": 1.0, "yellow": 0.95, "red": 0.8, "black": 0.7}
        return int(self.voice_rate * mult.get(self.tier, 1.0))

    def motor_allowed(self) -> bool:
        return self.tier in self.motor_allowed_tiers

    def save_tier(self, tier: str) -> None:
        self.tier = tier
        if DEFAULT_CONFIG.exists():
            with open(DEFAULT_CONFIG) as f:
                raw = yaml.safe_load(f) or {}
            raw["tier"] = tier
            with open(DEFAULT_CONFIG, "w") as f:
                yaml.dump(raw, f, default_flow_style=False)
