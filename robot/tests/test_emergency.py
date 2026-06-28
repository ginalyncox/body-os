"""Tests for emergency escalation."""

import unittest
from pathlib import Path

from brain.emergency.cellular import MockCellular
from brain.emergency.settings import load_emergency_settings
from brain.skills.emergency import EmergencyMode, EmergencySkill


class EmergencyTest(unittest.TestCase):
    def test_load_settings(self) -> None:
        path = Path(__file__).resolve().parent.parent / "emergency.example.yaml"
        settings = load_emergency_settings(path)
        self.assertTrue(settings.enabled)
        self.assertEqual(settings.ems_number, "911")
        self.assertEqual(settings.mental_health_number, "988")

    def test_dry_run_escalation(self) -> None:
        path = Path(__file__).resolve().parent.parent / "emergency.example.yaml"
        settings = load_emergency_settings(path)
        settings.dry_run = True
        settings.contacts = settings.contacts[:1] if settings.contacts else []
        skill = EmergencySkill(settings)
        skill.modem = MockCellular()
        log = skill.escalate(EmergencyMode.CONTACTS_ONLY)
        self.assertTrue(log["ok"])
        self.assertTrue(log["dry_run"])
        self.assertTrue(log["gps"]["valid"])

    def test_gps_maps_url(self) -> None:
        modem = MockCellular(40.0, -75.0)
        fix = modem.get_gps()
        self.assertIn("40", fix.maps_url or "")


if __name__ == "__main__":
    unittest.main()
