from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class DataStore:
    """Local JSON persistence — mirrors companion app schemas."""

    def __init__(self, data_dir: Path) -> None:
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.vitals_path = data_dir / "vitals.json"
        self.flares_path = data_dir / "flares.json"
        self.pacing_path = data_dir / "pacing.json"
        self.postmortems_path = data_dir / "postmortems.json"
        self._ensure_files()

    def _ensure_files(self) -> None:
        for p in (self.vitals_path, self.flares_path, self.pacing_path, self.postmortems_path):
            if not p.exists():
                p.write_text("[]")

    def _read(self, path: Path) -> list[dict[str, Any]]:
        return json.loads(path.read_text())

    def _write(self, path: Path, data: list[dict[str, Any]]) -> None:
        path.write_text(json.dumps(data, indent=2, default=str))

    def add_vitals(self, entry: dict[str, Any]) -> dict[str, Any]:
        rows = self._read(self.vitals_path)
        today = entry.get("date", datetime.now().strftime("%Y-%m-%d"))
        rows = [r for r in rows if r.get("date") != today]
        entry.setdefault("id", datetime.now().isoformat())
        entry.setdefault("created_at", datetime.now().isoformat())
        rows.insert(0, entry)
        self._write(self.vitals_path, rows)
        return entry

    def today_vitals(self) -> dict[str, Any] | None:
        today = datetime.now().strftime("%Y-%m-%d")
        for row in self._read(self.vitals_path):
            if row.get("date") == today:
                return row
        return None

    def add_flare(self, entry: dict[str, Any]) -> dict[str, Any]:
        rows = self._read(self.flares_path)
        entry.setdefault("id", datetime.now().isoformat())
        entry.setdefault("time", datetime.now().isoformat())
        entry.setdefault("created_at", datetime.now().isoformat())
        rows.insert(0, entry)
        self._write(self.flares_path, rows)
        return entry

    def add_pacing(self, entry: dict[str, Any]) -> dict[str, Any]:
        rows = self._read(self.pacing_path)
        entry.setdefault("id", datetime.now().isoformat())
        entry.setdefault("created_at", datetime.now().isoformat())
        rows.insert(0, entry)
        self._write(self.pacing_path, rows)
        return entry

    def week_green_yellow_count(self) -> int:
        from datetime import timedelta
        cutoff = datetime.now() - timedelta(days=7)
        count = 0
        for row in self._read(self.vitals_path):
            try:
                d = datetime.strptime(row["date"], "%Y-%m-%d")
            except (KeyError, ValueError):
                continue
            if d >= cutoff and row.get("tier") in ("green", "yellow"):
                count += 1
        return count

    def export_all(self) -> dict[str, Any]:
        return {
            "vitals": self._read(self.vitals_path),
            "flares": self._read(self.flares_path),
            "pacing": self._read(self.pacing_path),
            "postmortems": self._read(self.postmortems_path),
        }

    def _merge_by_id(self, existing: list[dict], incoming: list[dict], id_key: str = "id") -> list[dict]:
        by_id = {r.get(id_key) or r.get("date"): r for r in existing}
        for row in incoming:
            key = row.get(id_key) or row.get("date")
            if key:
                by_id[key] = {**by_id.get(key, {}), **row}
        merged = list(by_id.values())
        merged.sort(key=lambda r: r.get("created_at", r.get("createdAt", "")), reverse=True)
        return merged

    def merge_companion_bundle(self, bundle: dict[str, Any]) -> dict[str, int]:
        """Merge companion app export into robot store. Returns counts merged."""
        from .sync_transform import companion_bundle_to_robot

        robot_data = companion_bundle_to_robot(bundle)
        counts = {"vitals": 0, "flares": 0, "postmortems": 0}

        if robot_data["vitals"]:
            merged = self._merge_by_id(self._read(self.vitals_path), robot_data["vitals"], "date")
            counts["vitals"] = len(robot_data["vitals"])
            self._write(self.vitals_path, merged)

        if robot_data["flares"]:
            merged = self._merge_by_id(self._read(self.flares_path), robot_data["flares"])
            counts["flares"] = len(robot_data["flares"])
            self._write(self.flares_path, merged)

        if robot_data.get("postmortems"):
            merged = self._merge_by_id(self._read(self.postmortems_path), robot_data["postmortems"])
            counts["postmortems"] = len(robot_data["postmortems"])
            self._write(self.postmortems_path, merged)

        return counts

    def add_postmortem(self, entry: dict[str, Any]) -> dict[str, Any]:
        rows = self._read(self.postmortems_path)
        entry.setdefault("id", datetime.now().isoformat())
        entry.setdefault("created_at", datetime.now().isoformat())
        rows.insert(0, entry)
        self._write(self.postmortems_path, rows)
        return entry
