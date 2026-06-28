from __future__ import annotations

import time
from dataclasses import dataclass

from .mock import MotorDriver


@dataclass
class SerialConfig:
    port: str = "/dev/ttyUSB0"
    baud: int = 115200
    timeout: float = 2.0


class SerialMotor(MotorDriver):
    """
    Motor controller over serial (Arduino/ESP32 firmware).
    Protocol (newline-terminated):
      STOP
      GOTO <waypoint>
      COME
      PING → PONG
    """

    def __init__(
        self,
        config: SerialConfig | None = None,
        waypoints: dict | None = None,
    ) -> None:
        self.config = config or SerialConfig()
        self.waypoints = waypoints or {}
        self._moving = False
        self._ser = None
        self._connect()

    def _connect(self) -> None:
        try:
            import serial
            self._ser = serial.Serial(
                self.config.port,
                self.config.baud,
                timeout=self.config.timeout,
            )
            time.sleep(0.5)
            resp = self._cmd("PING")
            print(f"   [serial: connected {self.config.port} → {resp}]")
        except Exception as exc:
            print(f"   [serial: not connected ({exc}) — commands will log only]")
            self._ser = None

    def _cmd(self, line: str) -> str:
        if not self._ser:
            print(f"   [serial: {line}]")
            return "OK"
        self._ser.write(f"{line}\n".encode())
        self._ser.flush()
        try:
            return self._ser.readline().decode().strip()
        except Exception:
            return ""

    def stop(self) -> None:
        self._moving = False
        self._cmd("STOP")

    def go_to(self, waypoint: str) -> bool:
        key = waypoint.lower().replace(" ", "_")
        if key not in self.waypoints and key != "user":
            print(f"   [serial: unknown waypoint '{waypoint}']")
            return False
        self._moving = True
        cmd = "COME" if key == "user" else f"GOTO {key}"
        resp = self._cmd(cmd)
        self._moving = False
        return resp.upper() in ("OK", "DONE", "PONG", "")

    def dock_creep(self) -> None:
        self._cmd("DOCK")

    def come_here(self) -> bool:
        return self.go_to("user")

    @property
    def is_moving(self) -> bool:
        return self._moving
