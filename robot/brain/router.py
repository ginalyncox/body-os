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
from .skills.shutdown import ShutdownSkill
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

    def _check_crisis(self, text: str) -> bool:
        lower = text.lower()
        keywords = self.config.crisis_keywords or load_flows().get("crisis_keywords", [])
        if any(k in lower for k in keywords):
            CrisisSkill().run(self.voice)
            return True
        return False

    def _help_text(self) -> str:
        name = self.config.name
        return (
            f"I'm {name}. Commands: morning, flare, reset, reset5, deep, shutdown, "
            "hijacked, pain, itch, sensory, doom, pacing start ACTIVITY MINUTES, "
            "tier green|yellow|red|black, come here, go kitchen|desk|bedroom, "
            "status, help, quit."
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
            if v:
                self.voice.say(
                    f"{tier.capitalize()} day. Pain {v.get('morning_pain')}, "
                    f"energy {v.get('morning_energy')}. "
                    f"This week: {gy} green or yellow days toward SLO of five.",
                    force=True,
                )
            else:
                self.voice.say(f"{tier.capitalize()} day. No vitals logged yet. Say morning.", force=True)
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
