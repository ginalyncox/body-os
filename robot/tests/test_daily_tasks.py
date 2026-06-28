"""Tests for daily task nudges."""

import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

from brain.config import RobotConfig
from brain.content.tasks import tasks_for_tier
from brain.data.store import DataStore
from brain.skills.daily_tasks import DailyTasksSkill


class DailyTasksTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(__file__).parent / "_tmp_daily"
        self.tmp.mkdir(exist_ok=True)
        self.store = DataStore(self.tmp)

    def tearDown(self) -> None:
        import shutil
        if self.tmp.exists():
            shutil.rmtree(self.tmp)

    def test_red_tier_includes_hygiene(self) -> None:
        ids = {t["id"] for t in tasks_for_tier("red")}
        self.assertIn("teeth", ids)
        self.assertIn("bathroom", ids)
        self.assertNotIn("reset_mid", ids)

    def test_black_tier_floor_only(self) -> None:
        ids = {t["id"] for t in tasks_for_tier("black")}
        self.assertEqual(ids, {"vitals", "water", "meds", "bathroom", "shutdown"})

    def test_mark_and_check_done(self) -> None:
        self.store.mark_task_done("teeth", "09:00")
        self.assertTrue(self.store.is_task_done("teeth", "09:00"))
        self.assertFalse(self.store.is_task_done("teeth", "21:00"))

    def test_nudge_cooldown_blocks_repeat(self) -> None:
        skill = DailyTasksSkill(min_minutes_between=60)
        self.store.mark_nudged("water", "09:00")
        last = self.store.last_nudged("water", "09:00")
        self.assertIsNotNone(last)
        with patch("brain.skills.daily_tasks.datetime") as mock_dt:
            from datetime import timedelta
            mock_dt.now.return_value = last + timedelta(minutes=30)
            mock_dt.strftime = datetime.strftime
            config = RobotConfig(tier="red", daily_tasks_enabled=True, daily_tasks_red_nudge=True)
            voice = MagicMock()
            self.assertFalse(skill.maybe_nudge(voice, self.store, config))
            voice.say.assert_not_called()

    def test_mark_done_via_skill(self) -> None:
        skill = DailyTasksSkill()
        with patch("brain.skills.daily_tasks.datetime") as mock_dt:
            mock_dt.now.return_value = datetime(2026, 6, 28, 12, 0)
            mock_dt.strftime = datetime.strftime
            self.assertTrue(skill.mark_done(self.store, "water", "red"))
        self.assertTrue(self.store.is_task_done("water", "09:00"))


if __name__ == "__main__":
    unittest.main()
