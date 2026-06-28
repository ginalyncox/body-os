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
        self._ensure_files()

    def _ensure_files(self) -> None:
        for p in (self.vitals_path, self.flares_path, self.pacing_path):
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
