from __future__ import annotations

from typing import Any


def vitals_to_robot(entry: dict[str, Any]) -> dict[str, Any]:
    """Companion camelCase → robot snake_case."""
    return {
        "id": entry.get("id"),
        "date": entry.get("date"),
        "tier": entry.get("tier"),
        "sleep_hours": entry.get("sleepHours", entry.get("sleep_hours")),
        "sleep_quality": entry.get("sleepQuality", entry.get("sleep_quality")),
        "morning_pain": entry.get("morningPain", entry.get("morning_pain")),
        "morning_energy": entry.get("morningEnergy", entry.get("morning_energy")),
        "autonomic_state": entry.get("autonomicState", entry.get("autonomic_state")),
        "cycle_day": entry.get("cycleDay", entry.get("cycle_day")),
        "notable": entry.get("notable"),
        "created_at": entry.get("createdAt", entry.get("created_at")),
    }


def vitals_to_companion(entry: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": entry.get("id", ""),
        "date": entry.get("date", ""),
        "tier": entry.get("tier", "green"),
        "sleepHours": entry.get("sleep_hours", 7),
        "sleepQuality": entry.get("sleep_quality", 3),
        "morningPain": entry.get("morning_pain", 5),
        "morningEnergy": entry.get("morning_energy", 5),
        "autonomicState": entry.get("autonomic_state", "Calm"),
        "cycleDay": entry.get("cycle_day"),
        "notable": entry.get("notable"),
        "createdAt": entry.get("created_at", ""),
    }


def flare_to_robot(entry: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": entry.get("id"),
        "summary": entry.get("summary"),
        "time": entry.get("time"),
        "severity": entry.get("severity"),
        "primary_symptom": entry.get("primarySymptom", entry.get("primary_symptom")),
        "body_regions": entry.get("bodyRegions", entry.get("body_regions", [])),
        "suspected_triggers": entry.get("suspectedTriggers", entry.get("suspected_triggers", [])),
        "doing_what": entry.get("doingWhat", entry.get("doing_what")),
        "script_run": entry.get("scriptRun", entry.get("script_run", "none")),
        "time_to_recover": entry.get("timeToRecover", entry.get("time_to_recover")),
        "hours_slept": entry.get("hoursSlept", entry.get("hours_slept")),
        "last_meal_hours_ago": entry.get("lastMealHoursAgo", entry.get("last_meal_hours_ago")),
        "notes": entry.get("notes"),
        "created_at": entry.get("createdAt", entry.get("created_at")),
    }


def flare_to_companion(entry: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": entry.get("id", ""),
        "summary": entry.get("summary", ""),
        "time": entry.get("time", ""),
        "severity": entry.get("severity", 5),
        "primarySymptom": entry.get("primary_symptom", "Pain"),
        "bodyRegions": entry.get("body_regions", []),
        "suspectedTriggers": entry.get("suspected_triggers", []),
        "doingWhat": entry.get("doing_what"),
        "scriptRun": entry.get("script_run", "none"),
        "timeToRecover": entry.get("time_to_recover"),
        "hoursSlept": entry.get("hours_slept"),
        "lastMealHoursAgo": entry.get("last_meal_hours_ago"),
        "notes": entry.get("notes"),
        "createdAt": entry.get("created_at", ""),
    }


def postmortem_to_companion(entry: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": entry.get("id", ""),
        "date": entry.get("date", ""),
        "tierReached": entry.get("tier_reached", entry.get("tierReached", "red")),
        "peakSeverity": entry.get("peak_severity", entry.get("peakSeverity", 8)),
        "duration": entry.get("duration"),
        "timeline": entry.get("timeline", ""),
        "whatHappened": entry.get("what_happened", entry.get("whatHappened", "")),
        "triggers": entry.get("triggers", ""),
        "whatWorked": entry.get("what_worked", entry.get("whatWorked", "")),
        "whatDidntWork": entry.get("what_didnt_work", entry.get("whatDidntWork", "")),
        "pastSelfActions": entry.get("past_self_actions", entry.get("pastSelfActions", "")),
        "systemChanges": entry.get("system_changes", entry.get("systemChanges", "")),
        "sloImpact": entry.get("slo_impact", entry.get("sloImpact", "")),
        "futureNote": entry.get("future_note", entry.get("futureNote", "")),
        "createdAt": entry.get("created_at", entry.get("createdAt", "")),
    }


def companion_bundle_to_robot(bundle: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    return {
        "vitals": [vitals_to_robot(v) for v in bundle.get("vitals", [])],
        "flares": [flare_to_robot(f) for f in bundle.get("flares", [])],
        "postmortems": bundle.get("postmortems", []),
    }


def robot_bundle_to_companion(store_export: dict[str, Any]) -> dict[str, Any]:
    return {
        "version": 1,
        "vitals": [vitals_to_companion(v) for v in store_export.get("vitals", [])],
        "flares": [flare_to_companion(f) for f in store_export.get("flares", [])],
        "postmortems": [postmortem_to_companion(p) for p in store_export.get("postmortems", [])],
    }
