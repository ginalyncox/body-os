from __future__ import annotations

import time
from abc import ABC, abstractmethod


class MotorDriver(ABC):
    @abstractmethod
    def stop(self) -> None:
        ...

    @abstractmethod
    def go_to(self, waypoint: str) -> bool:
        ...

    @abstractmethod
    def come_here(self) -> bool:
        ...

    @property
    @abstractmethod
    def is_moving(self) -> bool:
        ...


class MockMotor(MotorDriver):
    """Simulates rolling between named waypoints."""

    def __init__(self, waypoints: dict | None = None) -> None:
        self.waypoints = waypoints or {}
        self._moving = False
        self._location = "desk"

    def stop(self) -> None:
        self._moving = False
        print("   [motors: STOP]")

    def go_to(self, waypoint: str) -> bool:
        key = waypoint.lower().replace(" ", "_")
        if key not in self.waypoints and key != "user":
            print(f"   [motors: unknown waypoint '{waypoint}']")
            return False
        self._moving = True
        dest = self.waypoints.get(key, {"x": 0, "y": 0})
        print(f"   [motors: rolling to {waypoint} → {dest}]")
        self._moving = False
        self._location = key
        return True

    def come_here(self) -> bool:
        return self.go_to("user")

    def dock_creep(self) -> None:
        """Slow reverse onto charge contacts — last 20 cm."""
        print("   [motors: dock creep — reverse 3s]")
        time.sleep(0.5)

    @property
    def is_moving(self) -> bool:
        return self._moving
