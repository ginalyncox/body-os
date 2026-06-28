from __future__ import annotations

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
    tts_engine: str = "edge"
    stt_engine: str = "console"
    voice_rate: int = 150
    voice_volume: float = 0.8
    voice_id: str = "en-US-JennyNeural"
    voice_hybrid: bool = True
    motor_driver: str = "mock"
    motor_allowed_tiers: list[str] = field(default_factory=lambda: ["green", "yellow"])
    motor_max_speed: float = 0.3
    motor_gpio_pins: dict[str, int] = field(default_factory=dict)
    motor_serial_port: str = "/dev/ttyUSB0"
    motor_serial_baud: int = 115200
    waypoints: dict[str, dict[str, float]] = field(default_factory=dict)
    data_dir: Path = field(default_factory=lambda: ROOT / "brain" / "data" / "local")
    crisis_keywords: list[str] = field(default_factory=list)
    sync_enabled: bool = True
    sync_host: str = "0.0.0.0"
    sync_port: int = 8765
    autonomy_enabled: bool = True
    autonomy_interval: int = 30
    proactive: bool = True
    mutual_care: bool = True
    roll_when_charging: bool = True
    schedule_morning: str = "08:00"
    battery_driver: str = "mock"
    battery_mock_percent: float = 85.0
    battery_mock_charging: bool = False
    life_context_path: Path | None = None
    daily_tasks_enabled: bool = True
    daily_tasks_min_interval: int = 60
    daily_tasks_red_nudge: bool = True
    daily_tasks_black_nudge: bool = False
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
        sync = raw.get("sync", raw.get("companion", {}))
        autonomy = raw.get("autonomy", {})
        battery = raw.get("battery", {})
        schedule = raw.get("schedule", {})
        daily = raw.get("daily_tasks", {})

        data_dir = Path(raw.get("companion", {}).get("data_dir", "./brain/data/local"))
        if not data_dir.is_absolute():
            data_dir = ROOT / data_dir

        return cls(
            name=robot.get("name", "Scout"),
            wake_words=[w.lower() for w in robot.get("wake_words", ["scout"])],
            personality=robot.get("personality", "sre"),
            tier=raw.get("tier", "green"),
            tts_engine=voice.get("tts_engine", "edge"),
            stt_engine=voice.get("stt_engine", "console"),
            voice_rate=int(voice.get("rate", 150)),
            voice_volume=float(voice.get("volume", 0.8)),
            voice_id=voice.get("voice", "en-US-JennyNeural"),
            voice_hybrid=bool(voice.get("hybrid", True)),
            motor_driver=motor.get("driver", "mock"),
            motor_allowed_tiers=motor.get("allowed_tiers", ["green", "yellow"]),
            motor_max_speed=float(motor.get("max_speed", 0.3)),
            motor_gpio_pins=motor.get("gpio_pins", {}),
            motor_serial_port=motor.get("serial_port", "/dev/ttyUSB0"),
            motor_serial_baud=int(motor.get("serial_baud", 115200)),
            waypoints=motor.get("waypoints", {}),
            data_dir=data_dir,
            crisis_keywords=crisis,
            sync_enabled=bool(sync.get("enabled", True)),
            sync_host=sync.get("host", "0.0.0.0"),
            sync_port=int(sync.get("port", 8765)),
            autonomy_enabled=bool(autonomy.get("enabled", True)),
            autonomy_interval=int(autonomy.get("check_interval_seconds", 30)),
            proactive=bool(autonomy.get("proactive", True)),
            mutual_care=bool(autonomy.get("mutual_care", True)),
            roll_when_charging=bool(autonomy.get("roll_when_charging", True)),
            schedule_morning=schedule.get("morning_vitals", "08:00"),
            battery_driver=battery.get("driver", "mock"),
            battery_mock_percent=float(battery.get("mock_percent", 85)),
            battery_mock_charging=bool(battery.get("mock_charging", False)),
            life_context_path=ROOT / "life-context.yaml" if (ROOT / "life-context.yaml").exists() else None,
            daily_tasks_enabled=bool(daily.get("enabled", True)),
            daily_tasks_min_interval=int(daily.get("min_minutes_between", 60)),
            daily_tasks_red_nudge=bool(daily.get("nudge_on_red", True)),
            daily_tasks_black_nudge=bool(daily.get("nudge_on_black", False)),
            raw=raw,
        )

    def motor_config(self) -> Any:
        from .motor import MotorConfig
        return MotorConfig(
            driver=self.motor_driver,
            waypoints=self.waypoints,
            max_speed=self.motor_max_speed,
            gpio_pins=self.motor_gpio_pins or None,
            serial_port=self.motor_serial_port,
            serial_baud=self.motor_serial_baud,
        )

    def tier_rate(self) -> int:
        mult = {"green": 1.0, "yellow": 0.95, "red": 0.8, "black": 0.7}
        return int(self.voice_rate * mult.get(self.tier, 1.0))

    def motor_allowed(self) -> bool:
        return self.tier in self.motor_allowed_tiers

    def save_tier(self, tier: str) -> None:
        self.tier = tier
        path = DEFAULT_CONFIG if DEFAULT_CONFIG.exists() else EXAMPLE_CONFIG
        if path.exists():
            with open(path) as f:
                raw = yaml.safe_load(f) or {}
            raw["tier"] = tier
            with open(path, "w") as f:
                yaml.dump(raw, f, default_flow_style=False)
