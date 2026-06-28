from __future__ import annotations

from dataclasses import dataclass

from .gpio import GPIOMotor, GPIOPinMap
from .mock import MockMotor, MotorDriver
from .serial import SerialConfig, SerialMotor


@dataclass
class MotorConfig:
    driver: str = "mock"
    waypoints: dict[str, dict[str, float]] | None = None
    max_speed: float = 0.3
    gpio_pins: dict[str, int] | None = None
    serial_port: str = "/dev/ttyUSB0"
    serial_baud: int = 115200


def create_motor(config: MotorConfig | None = None, waypoints: dict | None = None) -> MotorDriver:
    cfg = config or MotorConfig()
    wps = cfg.waypoints or waypoints or {}

    if cfg.driver == "gpio":
        pins = GPIOPinMap(**cfg.gpio_pins) if cfg.gpio_pins else None
        return GPIOMotor(pins=pins, waypoints=wps, max_speed=cfg.max_speed)

    if cfg.driver == "serial":
        return SerialMotor(
            config=SerialConfig(port=cfg.serial_port, baud=cfg.serial_baud),
            waypoints=wps,
        )

    if cfg.driver == "mock":
        return MockMotor(wps)

    print(f"Motor driver '{cfg.driver}' unknown; using mock.")
    return MockMotor(wps)


__all__ = [
    "MotorDriver",
    "MockMotor",
    "GPIOMotor",
    "SerialMotor",
    "MotorConfig",
    "GPIOPinMap",
    "create_motor",
]
