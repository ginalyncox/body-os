from __future__ import annotations

import threading
import time
from typing import Callable

from .settings import EmergencySettings


class EmergencyButtonMonitor:
    """Watch GPIO emergency button — hold triggers EMS escalation."""

    def __init__(
        self,
        settings: EmergencySettings,
        on_trigger: Callable[[], None],
    ) -> None:
        self.settings = settings
        self.on_trigger = on_trigger
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._gpio = None

    def start(self) -> None:
        if not self.settings.enabled or not self.settings.button_enabled:
            return
        if self._thread and self._thread.is_alive():
            return
        try:
            import RPi.GPIO as GPIO  # type: ignore[import-untyped]
            self._gpio = GPIO
            GPIO.setmode(GPIO.BCM)
            pull = GPIO.PUD_UP if self.settings.button_active_low else GPIO.PUD_DOWN
            GPIO.setup(self.settings.button_gpio, GPIO.IN, pull_up_down=pull)
        except Exception as exc:
            print(f"   [emergency:button] GPIO unavailable ({exc}) — voice only")
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        print(f"   [emergency:button] monitoring GPIO {self.settings.button_gpio}")

    def stop(self) -> None:
        self._stop.set()
        if self._gpio:
            try:
                self._gpio.cleanup(self.settings.button_gpio)
            except Exception:
                pass

    def _pressed(self) -> bool:
        if not self._gpio:
            return False
        level = self._gpio.input(self.settings.button_gpio)
        if self.settings.button_active_low:
            return level == 0
        return level == 1

    def _run(self) -> None:
        hold = self.settings.button_hold_seconds
        while not self._stop.wait(0.05):
            if not self._pressed():
                continue
            start = time.time()
            while self._pressed() and time.time() - start < hold:
                time.sleep(0.05)
            if time.time() - start >= hold:
                print("   [emergency:button] held — triggering EMS")
                self.on_trigger()
                time.sleep(5)
