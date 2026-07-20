from __future__ import annotations

from datetime import datetime, timedelta

from typing import Protocol

from ..config import RobotConfig
from ..content.tasks import tasks_for_tier
from ..data.store import DataStore


class NudgeChannel(Protocol):
    def say(self, text: str, force: bool = False) -> None: ...


class DailyTasksSkill:
    """Tier-aware nudges for minimum daily completes — hygiene, water, meds, food."""

    def __init__(self, min_minutes_between: int = 60) -> None:
        self.min_minutes_between = min_minutes_between

    def _slot_key(self, task: dict, time_str: str) -> str:
        if task.get("kind") == "once":
            return "*"
        return time_str

    def pending(self, store: DataStore, tier: str) -> list[dict]:
        now_hm = datetime.now().strftime("%H:%M")
        out = []
        for task in tasks_for_tier(tier):
            for time_str in task.get("times", []):
                if now_hm < time_str:
                    continue
                slot = self._slot_key(task, time_str)
                if not store.is_task_done(task["id"], slot):
                    out.append({**task, "slot": slot, "due": time_str})
        return out

    def list_status(self, store: DataStore, tier: str) -> str:
        pending = self.pending(store, tier)
        if not pending:
            return "Minimum daily completes are done for your tier. Rest is optional."
        labels = [p["label"] for p in pending[:5]]
        extra = len(pending) - 5
        msg = "Still open: " + ", ".join(labels)
        if extra > 0:
            msg += f", and {extra} more."
        return msg

    def mark_done(self, store: DataStore, task_id: str, tier: str) -> bool:
        tasks = {t["id"]: t for t in tasks_for_tier(tier)}
        if task_id not in tasks:
            return False
        task = tasks[task_id]
        now_hm = datetime.now().strftime("%H:%M")
        slot = "*"
        if task.get("kind") == "slots":
            # mark earliest overdue slot
            for time_str in task.get("times", []):
                if now_hm >= time_str and not store.is_task_done(task_id, time_str):
                    slot = time_str
                    break
            else:
                slot = task.get("times", ["*"])[-1]
        store.mark_task_done(task_id, slot)
        return True

    def maybe_nudge(
        self,
        channel: NudgeChannel,
        store: DataStore,
        config: RobotConfig,
    ) -> str | None:
        """Return nudge text if one was sent, else None."""
        if not config.daily_tasks_enabled:
            return None

        tier = config.tier
        if tier == "black" and not config.daily_tasks_black_nudge:
            return None
        if not config.proactive and tier in ("green", "yellow"):
            return None
        if tier == "red" and not config.daily_tasks_red_nudge:
            return None

        now = datetime.now()
        now_hm = now.strftime("%H:%M")

        # A single global cooldown prevents a second task from speaking
        # immediately after another reminder. Reduced-cognitive-load behavior
        # matters more than maximizing reminder throughput.
        last_any = store.last_nudged_any()
        if last_any and now - last_any < timedelta(minutes=self.min_minutes_between):
            return None

        for task in tasks_for_tier(tier):
            for time_str in task.get("times", []):
                if now_hm < time_str:
                    continue
                slot = self._slot_key(task, time_str)
                if store.is_task_done(task["id"], slot):
                    continue
                last = store.last_nudged(task["id"], slot)
                if last and now - last < timedelta(minutes=self.min_minutes_between):
                    continue

                msg = self._nudge_text(task, tier)
                channel.say(msg, force=tier != "black" or task["id"] in ("water", "meds", "bathroom"))
                store.mark_nudged(task["id"], slot)
                return msg
        return None

    def _nudge_text(self, task: dict, tier: str) -> str:
        label = task["label"]
        base = task.get("nudge", label)
        if tier == "red":
            return f"Minimum: {label.lower()}. {base}"
        if tier == "black":
            if task["id"] == "water":
                return "Sip water when you can."
            if task["id"] == "bathroom":
                return "Bathroom if you're able."
            if task["id"] == "meds":
                return "Meds, if due."
            return base
        if tier == "yellow":
            return f"Yellow day — {base}"
        return base

    def run_interactive(self, channel: NudgeChannel, store: DataStore, tier: str) -> None:
        channel.say(self.list_status(store, tier), force=True)
        pending = self.pending(store, tier)
        if pending:
            channel.say(
                "Reply: done teeth, done water, done bathroom, done meds.",
                force=True,
            )
