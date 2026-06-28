from __future__ import annotations

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class GpsFix:
    latitude: float | None
    longitude: float | None
    fix_valid: bool
    raw: str = ""

    @property
    def maps_url(self) -> str | None:
        if self.latitude is None or self.longitude is None:
            return None
        return f"https://maps.google.com/?q={self.latitude:.6f},{self.longitude:.6f}"

    def describe(self, fallback_address: str = "") -> str:
        if self.fix_valid and self.latitude is not None and self.longitude is not None:
            return f"GPS {self.latitude:.5f}, {self.longitude:.5f}"
        if fallback_address:
            return f"Last known address: {fallback_address}"
        return "GPS unavailable"


class CellularModem(ABC):
    @abstractmethod
    def get_gps(self, timeout_seconds: float = 15.0) -> GpsFix:
        ...

    @abstractmethod
    def send_sms(self, phone: str, body: str) -> bool:
        ...

    @abstractmethod
    def dial(self, phone: str) -> bool:
        ...

    @abstractmethod
    def hang_up(self) -> None:
        ...


class MockCellular(CellularModem):
    """Development — logs actions, returns fixed GPS."""

    def __init__(self, lat: float = 37.7749, lon: float = -122.4194) -> None:
        self._lat = lat
        self._lon = lon
        self._log: list[str] = []

    def get_gps(self, timeout_seconds: float = 15.0) -> GpsFix:
        _ = timeout_seconds
        return GpsFix(latitude=self._lat, longitude=self._lon, fix_valid=True, raw="mock")

    def send_sms(self, phone: str, body: str) -> bool:
        self._log.append(f"SMS {phone}: {body[:80]}...")
        print(f"   [cell:mock] SMS → {phone}")
        return True

    def dial(self, phone: str) -> bool:
        self._log.append(f"DIAL {phone}")
        print(f"   [cell:mock] DIAL {phone}")
        return True

    def hang_up(self) -> None:
        print("   [cell:mock] HANG UP")


class Sim7600Cellular(CellularModem):
    """
    SIM7600 / SIM7070 class LTE HAT over serial AT commands.
    Requires pyserial on the Pi. Test with dry_run before live 911 tests.
    """

    def __init__(self, port: str, baud: int = 115200) -> None:
        self.port = port
        self.baud = baud
        self._serial = None
        try:
            import serial
            self._serial = serial.Serial(port, baud, timeout=2)
            self._at("AT")
        except Exception as exc:
            print(f"   [cell:sim7600] open failed ({exc}) — falling back to mock behavior")
            self._serial = None

    def _at(self, cmd: str, wait: float = 0.3) -> str:
        if not self._serial:
            return ""
        self._serial.write(f"{cmd}\r\n".encode())
        time.sleep(wait)
        out = self._serial.read_all().decode(errors="replace")
        return out

    def get_gps(self, timeout_seconds: float = 15.0) -> GpsFix:
        if not self._serial:
            return GpsFix(None, None, False, "no serial")
        deadline = time.time() + timeout_seconds
        while time.time() < deadline:
            raw = self._at("AT+CGPSINFO")
            fix = _parse_cgpsinfo(raw)
            if fix.fix_valid:
                return fix
            raw = self._at("AT+CGNSINF")
            fix = _parse_cgnsinf(raw)
            if fix.fix_valid:
                return fix
            time.sleep(1)
        return GpsFix(None, None, False, "timeout")

    def send_sms(self, phone: str, body: str) -> bool:
        if not self._serial:
            return False
        self._at('AT+CMGF=1')
        self._at(f'AT+CMGS="{phone}"', wait=0.5)
        self._serial.write(body.encode() + b"\x1a")
        time.sleep(2)
        return True

    def dial(self, phone: str) -> bool:
        if not self._serial:
            return False
        self._at(f"ATD{phone};", wait=1.0)
        return True

    def hang_up(self) -> None:
        if self._serial:
            self._at("ATH")


def _parse_cgnsinf(raw: str) -> GpsFix:
    for line in raw.splitlines():
        if line.startswith("+CGNSINF:"):
            parts = [p.strip() for p in line.split(":", 1)[1].split(",")]
            if len(parts) < 4:
                return GpsFix(None, None, False, raw)
            try:
                valid = parts[1] == "1"
                lat = float(parts[2]) if parts[2] else None
                lon = float(parts[3]) if parts[3] else None
                return GpsFix(lat, lon, valid and lat is not None, raw)
            except ValueError:
                return GpsFix(None, None, False, raw)
    return GpsFix(None, None, False, raw)


def _parse_cgpsinfo(raw: str) -> GpsFix:
    for line in raw.splitlines():
        if line.startswith("+CGPSINFO:") and "," in line:
            parts = [p.strip() for p in line.split(":", 1)[1].split(",")]
            if len(parts) < 2 or not parts[0]:
                return GpsFix(None, None, False, raw)
            try:
                lat = _nmea_to_decimal(parts[0], parts[1])
                lon = _nmea_to_decimal(parts[2], parts[3])
                return GpsFix(lat, lon, True, raw)
            except (ValueError, IndexError):
                return GpsFix(None, None, False, raw)
    return GpsFix(None, None, False, raw)


def _nmea_to_decimal(value: str, hemisphere: str) -> float:
    if not value:
        raise ValueError("empty")
    dot = value.find(".")
    degrees = float(value[: dot - 2]) if dot > 2 else float(value)
    minutes = float(value[dot - 2 :]) if dot > 2 else 0.0
    decimal = degrees + minutes / 60.0
    if hemisphere in ("S", "W"):
        decimal = -decimal
    return decimal


def create_cellular(driver: str, port: str, baud: int) -> CellularModem:
    if driver == "sim7600":
        return Sim7600Cellular(port, baud)
    return MockCellular()
