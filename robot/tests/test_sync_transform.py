"""Tests for robot brain."""

import unittest

from brain.data.sync_transform import (
    companion_bundle_to_robot,
    flare_to_companion,
    robot_bundle_to_companion,
    vitals_to_companion,
    vitals_to_robot,
)


class SyncTransformTest(unittest.TestCase):
    def test_vitals_roundtrip(self) -> None:
        companion = {
            "date": "2026-06-28",
            "tier": "yellow",
            "sleepHours": 6.5,
            "sleepQuality": 3,
            "morningPain": 4,
            "morningEnergy": 5,
            "autonomicState": "Edgy",
            "id": "abc",
            "createdAt": "2026-06-28T08:00:00",
        }
        robot = vitals_to_robot(companion)
        self.assertEqual(robot["sleep_hours"], 6.5)
        self.assertEqual(robot["morning_pain"], 4)
        back = vitals_to_companion(robot)
        self.assertEqual(back["sleepHours"], 6.5)
        self.assertEqual(back["tier"], "yellow")

    def test_bundle_merge_shape(self) -> None:
        bundle = {
            "vitals": [{"date": "2026-06-28", "tier": "green", "sleepHours": 7, "morningPain": 2, "morningEnergy": 7, "autonomicState": "Calm", "sleepQuality": 4}],
            "flares": [{"summary": "test", "severity": 5, "primarySymptom": "Pain", "time": "2026-06-28T12:00:00"}],
            "postmortems": [],
        }
        robot = companion_bundle_to_robot(bundle)
        self.assertEqual(robot["vitals"][0]["morning_pain"], 2)
        companion_back = robot_bundle_to_companion({
            "vitals": robot["vitals"],
            "flares": robot["flares"],
            "postmortems": [],
        })
        self.assertEqual(companion_back["flares"][0]["primarySymptom"], "Pain")


if __name__ == "__main__":
    unittest.main()
