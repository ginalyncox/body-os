from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class Tier(str, Enum):
    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"
    BLACK = "black"


@dataclass
class SessionState:
    """Runtime state for the current interaction."""

    tier: Tier = Tier.GREEN
    in_flow: str | None = None
    flow_step: int = 0
    pacing_active: bool = False
    pacing_label: str = ""
    pacing_end: datetime | None = None
    last_flare_severity: int | None = None
    quiet_mode: bool = False  # black day default

    def set_tier(self, tier: str) -> None:
        self.tier = Tier(tier)
        self.quiet_mode = self.tier == Tier.BLACK

    def should_speak_proactively(self) -> bool:
        return self.tier in (Tier.GREEN, Tier.YELLOW)

    def max_response_sentences(self) -> int:
        return {Tier.GREEN: 4, Tier.YELLOW: 2, Tier.RED: 1, Tier.BLACK: 1}[self.tier]
