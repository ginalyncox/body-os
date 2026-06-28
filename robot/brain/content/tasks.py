from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

TASKS_PATH = Path(__file__).resolve().parent / "daily_tasks.json"


def load_task_definitions() -> list[dict[str, Any]]:
    with open(TASKS_PATH) as f:
        return json.load(f)["tasks"]


def tasks_for_tier(tier: str) -> list[dict[str, Any]]:
    return [t for t in load_task_definitions() if tier in t.get("tiers", [])]
