from __future__ import annotations

import math
import time
from dataclasses import dataclass

from .mock import MotorDriver


@dataclass
class GPIOPinMap:
    """L298N dual H-bridge pin mapping (BCM numbering)."""
    ena: int = 18
    in1: int = 23
    in2: int = 24
    enb: int = 19
    in3: int = 27
    in4: int = 22
    stby: int | None = None  # optional standby pin


class GPIOMotor(MotorDriver):
    """
    Raspberry Pi GPIO motor driver for L298N-style boards.
    Waypoint navigation uses timed dead reckoning (no lidar in v0.2).
  Install on Pi: pip install RPi.GPIO
    """

    def __init__(
        self,
        pins: GPIOPinMap | None = None,
        waypoints: dict | None = None,
        max_speed: float = 0.3,
        pwm_frequency: int = 1000,
    ) -> None:
        self.pins = pins or GPIOPinMap()
        self.waypoints = waypoints or {}
        self.max_speed = max(0.05, min(max_speed, 0.5))
        self.pwm_frequency = pwm_frequency
        self._moving = False
        self._x = 0.0
        self._y = 0.0
        self._heading = 0.0  # radians, 0 = +x
        self._gpio = None
        self._pwm_a = None
        self._pwm_b = None
        self._setup_gpio()

    def _setup_gpio(self) -> None:
        try:
            import RPi.GPIO as GPIO
            self._gpio = GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            for pin in (self.pins.in1, self.pins.in2, self.pins.in3, self.pins.in4):
                GPIO.setup(pin, GPIO.OUT)
            GPIO.setup(self.pins.ena, GPIO.OUT)
            GPIO.setup(self.pins.enb, GPIO.OUT)
            if self.pins.stby is not None:
                GPIO.setup(self.pins.stby, GPIO.OUT)
                GPIO.output(self.pins.stby, GPIO.HIGH)
            self._pwm_a = GPIO.PWM(self.pins.ena, self.pwm_frequency)
            self._pwm_b = GPIO.PWM(self.pins.enb, self.pwm_frequency)
            self._pwm_a.start(0)
            self._pwm_b.start(0)
            print("   [gpio: motor driver initialized]")
        except ImportError:
            print("   [gpio: RPi.GPIO not available — motor commands will log only]")
        except Exception as exc:
            print(f"   [gpio: init failed ({exc}) — motor commands will log only]")

    def _duty(self) -> float:
        return min(100.0, self.max_speed / 0.5 * 100.0)

    def _set_left(self, forward: bool, duty: float) -> None:
        if not self._gpio:
            return
        GPIO = self._gpio
        GPIO.output(self.pins.in1, GPIO.HIGH if forward else GPIO.LOW)
        GPIO.output(self.pins.in2, GPIO.LOW if forward else GPIO.HIGH)
        if self._pwm_a:
            self._pwm_a.ChangeDutyCycle(duty)

    def _set_right(self, forward: bool, duty: float) -> None:
        if not self._gpio:
            return
        GPIO = self._gpio
        GPIO.output(self.pins.in3, GPIO.HIGH if forward else GPIO.LOW)
        GPIO.output(self.pins.in4, GPIO.LOW if forward else GPIO.HIGH)
        if self._pwm_b:
            self._pwm_b.ChangeDutyCycle(duty)

    def _drive(self, left_fwd: bool, right_fwd: bool, seconds: float) -> None:
        duty = self._duty()
        self._set_left(left_fwd, duty)
        self._set_right(right_fwd, duty)
        time.sleep(seconds)
        self.stop()

    def _rotate(self, direction: str, seconds: float) -> None:
        if direction == "left":
            self._drive(False, True, seconds)
        else:
            self._drive(True, False, seconds)

    def stop(self) -> None:
        self._moving = False
        if self._gpio and self._pwm_a and self._pwm_b:
            self._pwm_a.ChangeDutyCycle(0)
            self._pwm_b.ChangeDutyCycle(0)
            GPIO = self._gpio
            for pin in (self.pins.in1, self.pins.in2, self.pins.in3, self.pins.in4):
                GPIO.output(pin, GPIO.LOW)
        print("   [gpio: STOP]")

    def _navigate_to(self, tx: float, ty: float) -> bool:
        dx = tx - self._x
        dy = ty - self._y
        dist = math.hypot(dx, dy)
        if dist < 0.05:
            return True

        target_angle = math.atan2(dy, dx)
        turn = target_angle - self._heading
        while turn > math.pi:
            turn -= 2 * math.pi
        while turn < -math.pi:
            turn += 2 * math.pi

        # ~2.5 rad/s turn rate at full duty — tune on your hardware
        turn_time = abs(turn) / 2.5
        if abs(turn) > 0.1:
            self._moving = True
            self._rotate("left" if turn > 0 else "right", turn_time)
            self._heading = target_angle

        drive_time = dist / self.max_speed
        self._moving = True
        self._drive(True, True, drive_time)
        self._x, self._y = tx, ty
        self._moving = False
        return True

    def go_to(self, waypoint: str) -> bool:
        key = waypoint.lower().replace(" ", "_")
        if key == "user":
            print("   [gpio: come_here — drive forward 1.5s placeholder; tune waypoints]")
            self._drive(True, True, 1.5)
            return True
        if key not in self.waypoints:
            print(f"   [gpio: unknown waypoint '{waypoint}']")
            return False
        wp = self.waypoints[key]
        tx = float(wp.get("x", 0))
        ty = float(wp.get("y", 0))
        print(f"   [gpio: navigating to {waypoint} ({tx}, {ty})]")
        return self._navigate_to(tx, ty)

    def dock_creep(self) -> None:
        if not self._gpio:
            print("   [gpio: dock creep — reverse 3s]")
            time.sleep(0.5)
            return
        self._drive(False, False, 3.0)

    def come_here(self) -> bool:
        return self.go_to("user")

    @property
    def is_moving(self) -> bool:
        return self._moving

    def cleanup(self) -> None:
        self.stop()
        if self._gpio:
            self._pwm_a.stop()
            self._pwm_b.stop()
            self._gpio.cleanup()
