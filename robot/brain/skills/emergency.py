from __future__ import annotations

import json
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING

from ..data.store import DataStore
from ..emergency.cellular import CellularModem, GpsFix, create_cellular
from ..emergency.settings import EmergencySettings, load_emergency_settings

if TYPE_CHECKING:
    from ..voice.orchestrator import VoiceOrchestrator


class EmergencyMode(str, Enum):
    EMS = "ems"
    MENTAL = "mental"
    CONTACTS_ONLY = "contacts_only"


class EmergencySkill:
    def __init__(self, settings: EmergencySettings | None = None) -> None:
        self.settings = settings or load_emergency_settings()
        self.modem: CellularModem = create_cellular(
            self.settings.cellular_driver,
            self.settings.cellular_port,
            self.settings.cellular_baud,
        )

    def escalate(
        self,
        mode: EmergencyMode,
        voice: VoiceOrchestrator | None = None,
        store: DataStore | None = None,
        *,
        skip_confirm: bool = False,
    ) -> dict:
        """Notify contacts, then call EMS or 988. Returns action log."""
        if not self.settings.enabled:
            msg = "Emergency system disabled in config."
            if voice:
                voice.say(msg, force=True)
            return {"ok": False, "error": msg}

        if voice and not skip_confirm and not self.settings.dry_run:
            voice.say(
                f"Emergency {mode.value}. Calling contacts and services in "
                f"{self.settings.cancel_window_seconds} seconds. Say cancel to stop.",
                force=True,
            )

        gps = self.modem.get_gps()
        log = self._run_escalation(mode, gps, store)
        if voice:
            if self.settings.dry_run:
                voice.say("Dry run — logged emergency actions only. No real calls.", force=True)
            elif log.get("ok"):
                voice.say("Emergency sequence started. I'm staying on the line.", force=True)
        return log

    def _run_escalation(
        self,
        mode: EmergencyMode,
        gps: GpsFix,
        store: DataStore | None,
    ) -> dict:
        actions: list[dict] = []
        lat = gps.latitude if gps.fix_valid else ""
        lon = gps.longitude if gps.fix_valid else ""
        address_line = (
            self.settings.gps_fallback_address
            if not gps.fix_valid
            else gps.describe()
        )

        for contact in self.settings.contacts:
            if not contact.sms_first:
                continue
            body = self.settings.script(
                "sms_contact",
                name=contact.name,
                human_name=self.settings.human_name or "user",
                lat=lat or "unknown",
                lon=lon or "unknown",
                address_line=address_line,
                medical_context=self.settings.medical_context,
            )
            if not body:
                body = (
                    f"{contact.name}: EMERGENCY ({self.settings.human_name}). "
                    f"{gps.describe(self.settings.gps_fallback_address)}"
                )
            ok = self._sms(contact.phone, body)
            actions.append({"action": "sms", "to": contact.phone, "ok": ok})

        if mode in (EmergencyMode.EMS, EmergencyMode.MENTAL):
            for contact in self.settings.contacts:
                if not contact.voice_call:
                    continue
                ok = self._dial(contact.phone)
                actions.append({"action": "call_contact", "to": contact.phone, "ok": ok})

        if mode == EmergencyMode.EMS:
            script = self.settings.script(
                "voice_ems",
                human_name=self.settings.human_name or "user",
                lat=lat or "unknown",
                lon=lon or "unknown",
                address_line=address_line,
                medical_context=self.settings.medical_context,
            )
            ok = self._dial(self.settings.ems_number)
            actions.append({
                "action": "call_ems",
                "to": self.settings.ems_number,
                "ok": ok,
                "script": script[:200],
            })
        elif mode == EmergencyMode.MENTAL:
            script = self.settings.script(
                "voice_mental_health",
                human_name=self.settings.human_name or "user",
            )
            ok = self._dial(self.settings.mental_health_number)
            actions.append({
                "action": "call_mental_health",
                "to": self.settings.mental_health_number,
                "ok": ok,
                "script": script[:200],
            })

        record = {
            "ok": True,
            "mode": mode.value,
            "dry_run": self.settings.dry_run,
            "gps": {
                "valid": gps.fix_valid,
                "lat": gps.latitude,
                "lon": gps.longitude,
                "maps": gps.maps_url,
            },
            "actions": actions,
            "time": datetime.now().isoformat(),
        }
        if store:
            self._persist_log(store, record)
        return record

    def _sms(self, phone: str, body: str) -> bool:
        if self.settings.dry_run:
            print(f"   [emergency:dry_run] SMS → {phone}")
            return True
        return self.modem.send_sms(phone, body)

    def _dial(self, phone: str) -> bool:
        if self.settings.dry_run:
            print(f"   [emergency:dry_run] DIAL {phone}")
            return True
        return self.modem.dial(phone)

    def _persist_log(self, store: DataStore, record: dict) -> None:
        path = store.data_dir / "emergency_log.json"
        rows: list[dict] = []
        if path.exists():
            rows = json.loads(path.read_text())
        rows.insert(0, record)
        path.write_text(json.dumps(rows[:50], indent=2, default=str))
