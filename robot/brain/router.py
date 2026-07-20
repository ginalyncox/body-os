from __future__ import annotations

from .config import RobotConfig
from .data.store import DataStore
from .motor import create_motor
from .skills.crisis import CrisisSkill
from .skills.flare_log import FlareLogSkill
from .skills.guided_flow import GuidedFlowSkill
from .skills.morning_vitals import MorningVitalsSkill
from .content import load_flows
from .skills.pacing import PacingSkill
from .skills.dock import DockSkill
from .skills.shutdown import ShutdownSkill
from .skills.emergency import EmergencySkill, EmergencyMode
from .emergency.settings import load_emergency_settings
from .emergency.button import EmergencyButtonMonitor
from .sms.channel import TextChannel
from .sms.client import SmsClient
from .state import SessionState
from .voice.orchestrator import VoiceOrchestrator

FLOW_ALIASES = {
    "reset": "reset-60s",
    "reset60": "reset-60s",
    "reset5": "reset-5min",
    "reset5min": "reset-5min",
    "deep": "reset-deep",
    "resetdeep": "reset-deep",
    "hijack": "hijacked",
    "pain": "pain-spike",
    "itch": "itch-flare",
    "sensory": "sensory-overload",
    "doom": "doom-loop",
    "doomloop": "doom-loop",
}

TASK_ALIASES = {
    "vitals": "vitals",
    "morning": "vitals",
    "water": "water",
    "sip": "water",
    "meds": "meds",
    "medication": "meds",
    "bathroom": "bathroom",
    "wc": "bathroom",
    "teeth": "teeth",
    "brush": "teeth",
    "face": "face",
    "wash": "face",
    "breakfast": "meal_am",
    "meal_am": "meal_am",
    "lunch": "meal_mid",
    "meal_mid": "meal_mid",
    "dinner": "meal_pm",
    "meal_pm": "meal_pm",
    "reset_mid": "reset_mid",
    "reset_deep": "reset_deep",
    "shutdown_task": "shutdown",
}


class Router:
    def __init__(self, config: RobotConfig) -> None:
        self.config = config
        self.state = SessionState()
        self.state.set_tier(config.tier)
        self.voice = VoiceOrchestrator(config)
        self.store = DataStore(config.data_dir)
        self.motor = create_motor(config.motor_config())
        self.pacing = PacingSkill()
        self.flows = GuidedFlowSkill()
        from .battery import create_battery
        self.battery = create_battery(
            config.battery_driver,
            config.battery_mock_percent,
            config.battery_mock_charging,
        )
        self.dock = DockSkill()
        self.daily_tasks = DailyTasksSkill()
        self.sms = SmsClient(config)
        self._emergency: EmergencySkill | None = None

    def emergency_skill(self) -> EmergencySkill:
        if self._emergency is None:
            settings = load_emergency_settings(self.config.emergency_config_path)
            settings.enabled = settings.enabled or self.config.emergency_enabled
            settings.dry_run = self.config.emergency_dry_run
            self._emergency = EmergencySkill(settings)
        return self._emergency

    def trigger_emergency_button(self) -> None:
        self.emergency_skill().escalate(
            EmergencyMode.EMS,
            self.voice,
            self.store,
            skip_confirm=True,
        )

    def _sms_help_text(self) -> str:
        name = self.config.name
        return (
            f"{name} SMS: tasks, done teeth|water|bathroom|meds, "
            "morning 7 5 4 edgy, tier red, status, help. Crisis: 988."
        )

    def handle_sms(self, text: str) -> list[str]:
        """Process inbound SMS; returns reply lines to send back."""
        channel = TextChannel(self.config)
        voice = self.voice
        self.voice = channel  # type: ignore[assignment]
        try:
            lower = text.strip().lower()
            tokens = lower.split()
            if tokens and tokens[0] == "morning":
                run_morning_sms(tokens, channel, self.store, self.config, self.state)
            elif tokens and tokens[0] == "flare" and len(tokens) >= 3:
                try:
                    severity = int(tokens[1])
                except ValueError:
                    severity = 5
                summary = " ".join(tokens[2:])
                self.store.add_flare({
                    "summary": summary[:120],
                    "severity": severity,
                    "primary_symptom": "Pain",
                    "body_regions": [],
                    "suspected_triggers": [],
                    "script_run": "none",
                })
                channel.say(f"Flare logged {severity}/10: {summary[:80]}", force=True)
            elif lower in ("help", "?"):
                channel.say(self._sms_help_text(), force=True)
            else:
                self.handle(text)
        finally:
            self.voice = voice

        if not channel.messages and self.config.tier != "black":
            channel.messages.append("Didn't catch that. Text help for commands.")
        return channel.messages

    def send_sms(self, text: str) -> bool:
        return self.sms.send(text)

    def nudge_via_sms(self, msg: str) -> bool:
        if not self.config.sms_enabled or not self.config.sms_nudges:
            return False
        return self.send_sms(f"{self.config.name}: {msg}")

    def _check_crisis(self, text: str) -> bool:
        lower = text.lower()
        keywords = self.config.crisis_keywords or load_flows().get("crisis_keywords", [])
        if any(k in lower for k in keywords):
            if self.config.emergency_enabled:
                self.voice.say(
                    "I hear you. Starting crisis line sequence.",
                    force=True,
                )
                self.emergency_skill().escalate(
                    EmergencyMode.MENTAL,
                    self.voice,
                    self.store,
                    skip_confirm=True,
                )
            else:
                CrisisSkill().run(self.voice)
            return True
        return False

    def _help_text(self) -> str:
        name = self.config.name
        return (
            f"I'm {name}. Commands: morning, flare, reset, reset5, deep, shutdown, "
            "tasks, done teeth|water|bathroom|meds, "
            "hijacked, pain, itch, sensory, doom, pacing start ACTIVITY MINUTES, "
            "tier green|yellow|red|black, emergency, call 911, call 988, "
            "status, battery, dock, help, quit."
        )

    def handle(self, text: str) -> bool:
        """Process one utterance. Returns False to exit main loop."""
        text = text.strip()
        if not text:
            return True
        if self._check_crisis(text):
            return True

        lower = text.lower()
        tokens = lower.split()

        if lower in ("quit", "exit", "bye"):
            self.voice.say("Shutting down. Rest if you can.", force=True)
            self.motor.stop()
            return False

        if lower in ("help", "?"):
            self.voice.say(self._help_text(), force=True)
            return True

        if lower in ("cancel", "abort"):
            self.voice.say("Cancelled.", force=True)
            return True

        if lower in ("emergency", "scout emergency", "sos"):
            self.emergency_skill().escalate(
                EmergencyMode.EMS, self.voice, self.store,
            )
            return True

        if lower in ("call 911", "911"):
            self.emergency_skill().escalate(
                EmergencyMode.EMS, self.voice, self.store,
            )
            return True

        if lower in ("call 988", "988", "crisis line"):
            self.emergency_skill().escalate(
                EmergencyMode.MENTAL, self.voice, self.store,
            )
            return True

        if lower == "contacts only":
            self.emergency_skill().escalate(
                EmergencyMode.CONTACTS_ONLY, self.voice, self.store,
            )
            return True

        if lower == "tasks":
            self.daily_tasks.run_interactive(self.voice, self.store, self.config.tier)
            return True

        if tokens[0] == "done" and len(tokens) >= 2:
            task_key = TASK_ALIASES.get(tokens[1], tokens[1])
            if self.daily_tasks.mark_done(self.store, task_key, self.config.tier):
                self.voice.say(f"Marked {task_key} done. Nice.", force=True)
            else:
                self.voice.say(
                    "I don't know that task for your tier. Say tasks to see what's open.",
                    force=True,
                )
            return True

        if lower == "morning":
            MorningVitalsSkill().run(self.voice, self.store, self.config, self.state)
            return True

        if lower == "flare":
            FlareLogSkill().run(self.voice, self.store, self.config, self.state)
            return True

        if lower == "shutdown":
            ShutdownSkill().run(self.voice, self.config, self.state)
            return True

        if lower == "status":
            v = self.store.today_vitals()
            tier = self.config.tier
            gy = self.store.week_green_yellow_count()
            bat = self.battery.read()
            bat_str = f"Battery {bat.percent:.0f}%"
            if bat.charging:
                bat_str += ", charging"
            if v:
                self.voice.say(
                    f"{tier.capitalize()} day. Pain {v.get('morning_pain')}, "
                    f"energy {v.get('morning_energy')}. {bat_str}. "
                    f"This week: {gy} green or yellow days toward SLO of five.",
                    force=True,
                )
            else:
                self.voice.say(
                    f"{tier.capitalize()} day. No vitals logged yet. {bat_str}. Say morning.",
                    force=True,
                )
            return True

        if lower == "battery":
            bat = self.battery.read()
            if bat.charging:
                self.voice.say(f"Charging. {bat.percent:.0f} percent.", force=True)
            elif bat.is_low:
                self.voice.say(
                    f"{bat.percent:.0f} percent. I should get to the dock.",
                    force=True,
                )
            else:
                self.voice.say(f"{bat.percent:.0f} percent. I'm good.", force=True)
            return True

        if lower in ("dock", "go dock", "charge"):
            self.dock.seek(self.voice, self.motor, self.config, self.state)
            return True

        if tokens[0] == "tier" and len(tokens) >= 2:
            tier = tokens[1]
            if tier in ("green", "yellow", "red", "black"):
                self.state.set_tier(tier)
                self.config.save_tier(tier)
                self.voice.say(f"Tier set to {tier}.", force=True)
            return True

        if lower.startswith("pacing"):
            if "stop" in lower:
                self.pacing.stop(self.voice, self.state)
            elif "start" in lower and len(tokens) >= 4:
                # pacing start study 25
                activity = tokens[2]
                try:
                    minutes = int(tokens[3])
                except ValueError:
                    minutes = 25
                self.pacing.start(self.voice, self.store, self.config, self.state, activity, minutes)
            else:
                self.voice.say("Say: pacing start ACTIVITY MINUTES — or pacing stop.", force=True)
            return True

        if lower in ("come here", "come to me", "come"):
            if not self.config.motor_allowed():
                self.voice.say("I won't roll on red or black days unless you really need me.", force=True)
                return True
            self.voice.say("On my way.", force=True)
            self.motor.come_here()
            self.voice.say("Here.", force=True)
            return True

        if tokens[0] == "go" and len(tokens) >= 2:
            dest = " ".join(tokens[1:])
            if not self.config.motor_allowed():
                self.voice.say("Rolling is paused for your current tier.", force=True)
                return True
            self.voice.say(f"Heading to {dest}.", force=True)
            ok = self.motor.go_to(dest)
            if ok:
                self.voice.say(f"At {dest}.", force=True)
            return True

        # Guided flows
        flow_key = lower.replace(" ", "-")
        flow_id = FLOW_ALIASES.get(flow_key.replace("-", ""), FLOW_ALIASES.get(flow_key, flow_key))
        flow_ids = [f["id"] for f in load_flows()["flows"]]
        if flow_id in flow_ids:
            self.flows.run(self.voice, self.config, self.state, flow_id)
            return True

        # Wake word passthrough
        for wake in self.config.wake_words:
            if lower.startswith(wake):
                rest = lower[len(wake):].strip()
                if rest:
                    return self.handle(rest)
                if self.config.tier == "red":
                    self.voice.say("Here. Water, reset-deep, or quiet?", force=True)
                elif self.config.tier == "black":
                    pass  # silent unless repeated
                else:
                    self.voice.say("Yeah?", force=True)
                return True

        if self.config.tier == "black":
            return True  # silent on unknown input

        self.voice.say("Didn't catch that. Say help for commands.", force=True)
        return True

    def greeting(self) -> None:
        name = self.config.name
        tier = self.config.tier
        self.voice.say(
            f"{name} online. {tier.capitalize()} day mode. "
            f"Say help, or morning for vitals.",
            force=True,
        )
