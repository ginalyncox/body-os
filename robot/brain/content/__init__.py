from __future__ import annotations

import json
from pathlib import Path

FLOWS_PATH = Path(__file__).resolve().parent / "flows.json"


def load_flows() -> dict:
    with open(FLOWS_PATH) as f:
        return json.load(f)
