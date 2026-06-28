from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class BatteryStatus:
    percent: float
    voltage: float
    charging: bool
    current_ma: float = 0.0

    @property
    def is_low(self) -> bool:
        return self.percent < 25 and not self.charging

    @property
    def is_critical(self) -> bool:
        return self.percent < 15 and not self.charging

    @property
    def is_ok(self) -> bool:
        return self.percent >= 40 or self.charging


class BatteryMonitor(ABC):
    @abstractmethod
    def read(self) -> BatteryStatus:
        ...


class MockBattery(BatteryMonitor):
    """Simulate battery for development."""

    def __init__(self, percent: float = 85.0, charging: bool = False) -> None:
        self._percent = percent
        self._charging = charging

    def read(self) -> BatteryStatus:
        return BatteryStatus(
            percent=self._percent,
            voltage=11.2 + (self._percent / 100) * 1.4,
            charging=self._charging,
            current_ma=1500 if self._charging else -300,
        )

    def set_percent(self, percent: float) -> None:
        self._percent = max(0, min(100, percent))

    def set_charging(self, charging: bool) -> None:
        self._charging = charging


class INA219Battery(BatteryMonitor):
    """Read battery via INA219 on I²C (Raspberry Pi)."""

    def __init__(self, address: int = 0x40, max_voltage: float = 12.6) -> None:
        self.max_voltage = max_voltage
        self._ina = None
        try:
            import board
            import busio
            from adafruit_ina219 import INA219
            i2c = busio.I2C(board.SCL, board.SDA)
            self._ina = INA219(i2c, addr=address)
        except Exception as exc:
            print(f"   [battery: INA219 not available ({exc})]")

    def read(self) -> BatteryStatus:
        if not self._ina:
            return MockBattery(50).read()
        voltage = self._ina.bus_voltage + self._ina.shunt_voltage
        current = self._ina.current
        pct = max(0, min(100, (voltage / self.max_voltage) * 100))
        charging = current > 100
        return BatteryStatus(percent=pct, voltage=voltage, charging=charging, current_ma=current)


def create_battery(driver: str, mock_percent: float = 85.0, mock_charging: bool = False) -> BatteryMonitor:
    if driver == "ina219":
        return INA219Battery()
    return MockBattery(percent=mock_percent, charging=mock_charging)
