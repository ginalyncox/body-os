from __future__ import annotations

import threading
import time
from datetime import datetime

from ..battery import BatteryMonitor, create_battery
from ..config import RobotConfig
from ..data.store import DataStore
from ..motor import MotorDriver
from ..skills.dock import DockSkill
from ..state import SessionState
from ..voice.orchestrator import VoiceOrchestrator


class CareLoop:
    """
    Layer 4 mutual care — monitors Scout's battery and your vitals/tier.
    Runs in a background thread when autonomy is enabled.
    """

    def __init__(
        self,
        config: RobotConfig,
        store: DataStore,
        battery: BatteryMonitor,
        motor: MotorDriver,
        voice: VoiceOrchestrator,
        state: SessionState,
    ) -> None:
        self.config = config
        self.store = store
        self.battery = battery
        self.motor = motor
        self.voice = voice
        self.state = state
        self.dock = DockSkill()
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._vitals_date = ""
        self._asked_vitals_today = False
        self._asked_dock_today = False

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        print("   [autonomy] mutual care loop started")

    def stop(self) -> None:
        self._stop.set()

    def _run(self) -> None:
        interval = self.config.autonomy_interval
        while not self._stop.wait(interval):
            try:
                self._tick()
            except Exception as exc:
                print(f"   [autonomy] tick error: {exc}")

    def _reset_daily_flags(self) -> None:
        today = datetime.now().strftime("%Y-%m-%d")
        if self._vitals_date != today:
            self._vitals_date = today
            self._asked_vitals_today = False
            self._asked_dock_today = False

    def _tick(self) -> None:
        self._reset_daily_flags()
        status = self.battery.read()
        self.state.battery_percent = status.percent
        self.state.charging = status.charging
        tier = self.config.tier

        if self.store.today_vitals():
            self._asked_vitals_today = True

        # Scout cares for itself — battery
        if status.is_critical and not status.charging:
            print(f"   [battery] critical {status.percent:.0f}%")
            self.dock.seek(
                self.voice, self.motor, self.config, self.state,
                silent=tier == "black",
            )
            return

        if status.is_low and not status.charging and not self._asked_dock_today:
            if self.config.mutual_care and self.config.roll_when_charging:
                print(f"   [battery] low {status.percent:.0f}% — seeking dock")
                self.dock.seek(self.voice, self.motor, self.config, self.state)
            elif not self._asked_dock_today:
                self.voice.say(
                    f"I'm at {status.percent:.0f} percent. Dock me when you can.",
                    force=tier != "black",
                )
            self._asked_dock_today = True

        if status.charging:
            self._asked_dock_today = False
            return

        # Your care — morning vitals (green/yellow only)
        if not self.config.proactive or tier in ("red", "black"):
            return

        now_hm = datetime.now().strftime("%H:%M")
        if (
            not self._asked_vitals_today
            and now_hm >= self.config.schedule_morning
            and not self.store.today_vitals()
        ):
            self.voice.say("Your turn — 60 second vitals? I'll wait.", force=True)
            self._asked_vitals_today = True


def build_care_loop(router: object) -> CareLoop:
    from ..battery import create_battery
    battery = create_battery(
        router.config.battery_driver,
        router.config.battery_mock_percent,
        router.config.battery_mock_charging,
    )
    return CareLoop(
        router.config,
        router.store,
        battery,
        router.motor,
        router.voice,
        router.state,
    )
