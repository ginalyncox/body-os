from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from ..config import ROOT


@dataclass
class EmergencyContact:
    name: str
    phone: str
    sms_first: bool = True
    voice_call: bool = True


@dataclass
class EmergencySettings:
    enabled: bool = False
    dry_run: bool = True
    button_enabled: bool = True
    button_gpio: int = 27
    button_hold_seconds: float = 2.0
    button_active_low: bool = True
    cancel_window_seconds: int = 10
    gps_fallback_address: str = ""
    human_name: str = ""
    medical_context: str = ""
    cellular_driver: str = "mock"
    cellular_port: str = "/dev/ttyUSB1"
    cellular_baud: int = 115200
    ems_number: str = "911"
    mental_health_number: str = "988"
    contacts: list[EmergencyContact] = field(default_factory=list)
    scripts: dict[str, str] = field(default_factory=dict)

    def script(self, key: str, **kwargs: Any) -> str:
        template = self.scripts.get(key, "")
        if not template:
            return ""
        return template.format(**kwargs).strip()


def load_emergency_settings(path: Path | None = None) -> EmergencySettings:
    candidates = [
        path,
        ROOT / "emergency.yaml",
        ROOT / "emergency.example.yaml",
    ]
    raw: dict[str, Any] = {}
    for candidate in candidates:
        if candidate and candidate.exists():
            with open(candidate) as f:
                raw = yaml.safe_load(f) or {}
            break

    button = raw.get("button", {})
    cell = raw.get("cellular", {})
    numbers = raw.get("numbers", {})
    contacts = [
        EmergencyContact(
            name=c.get("name", "Contact"),
            phone=c.get("phone", ""),
            sms_first=bool(c.get("sms_first", True)),
            voice_call=bool(c.get("voice_call", True)),
        )
        for c in raw.get("contacts", [])
        if c.get("phone")
    ]

    return EmergencySettings(
        enabled=bool(raw.get("enabled", False)),
        dry_run=bool(raw.get("dry_run", True)),
        button_enabled=bool(button.get("enabled", True)),
        button_gpio=int(button.get("gpio", 27)),
        button_hold_seconds=float(button.get("hold_seconds", 2)),
        button_active_low=bool(button.get("active_low", True)),
        cancel_window_seconds=int(raw.get("cancel_window_seconds", 10)),
        gps_fallback_address=str(raw.get("gps_fallback_address", "")),
        human_name=str(raw.get("human_name", "")),
        medical_context=str(raw.get("medical_context", "")).strip(),
        cellular_driver=str(cell.get("driver", "mock")),
        cellular_port=str(cell.get("serial_port", "/dev/ttyUSB1")),
        cellular_baud=int(cell.get("serial_baud", 115200)),
        ems_number=str(numbers.get("ems", "911")),
        mental_health_number=str(numbers.get("mental_health", "988")),
        contacts=contacts,
        scripts=dict(raw.get("scripts", {})),
    )
