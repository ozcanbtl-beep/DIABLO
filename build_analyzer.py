"""Validate and summarize a manually captured Diablo Immortal character profile.

No game memory access, network calls, account access, or gameplay automation.
The tool reports only supplied values; it does not invent build rankings.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ATTRIBUTE_NAMES = (
    "strength", "intelligence", "fortitude", "vitality", "willpower"
)


def load_profile(profile_path: str | Path) -> dict[str, Any]:
    path = Path(profile_path)
    if not path.is_file():
        raise FileNotFoundError(f"Profile not found: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Profile root must be a JSON object.")
    return data


def validate_profile(profile: dict[str, Any]) -> list[str]:
    """Return human-readable validation problems; empty means structurally valid."""
    problems: list[str] = []
    if profile.get("game") != "Diablo Immortal":
        problems.append('game must be "Diablo Immortal".')

    character = profile.get("character")
    if not isinstance(character, dict):
        problems.append("character must be an object.")
        character = {}

    attributes = character.get("primary_attributes", {})
    if not isinstance(attributes, dict):
        problems.append("character.primary_attributes must be an object.")
    else:
        for name in ATTRIBUTE_NAMES:
            value = attributes.get(name)
            if value is not None and (
                isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0
            ):
                problems.append(f"primary attribute {name} must be a non-negative number or null.")

    for field in ("equipment", "legendary_gems", "set_bonuses"):
        if field in profile and not isinstance(profile[field], list):
            problems.append(f"{field} must be a list.")

    for index, item in enumerate(profile.get("equipment", [])):
        if not isinstance(item, dict):
            problems.append(f"equipment[{index}] must be an object.")
        elif not isinstance(item.get("slot", ""), str):
            problems.append(f"equipment[{index}].slot must be text.")

    for index, gem in enumerate(profile.get("legendary_gems", [])):
        if not isinstance(gem, dict):
            problems.append(f"legendary_gems[{index}] must be an object.")
        elif gem.get("rank") is not None and (
            isinstance(gem["rank"], bool)
            or not isinstance(gem["rank"], int)
            or gem["rank"] < 0
        ):
            problems.append(f"legendary_gems[{index}].rank must be a non-negative integer or null.")

    return problems


def summarize_profile(profile: dict[str, Any]) -> dict[str, Any]:
    problems = validate_profile(profile)
    character = profile.get("character", {})
    attributes = character.get("primary_attributes", {})
    known_attributes = {
        key: value for key, value in attributes.items()
        if key in ATTRIBUTE_NAMES and value is not None
    }
    return {
        "valid": not problems,
        "problems": problems,
        "character": {
            "name": character.get("name") or "Not provided",
            "class": character.get("class") or "Not provided",
            "level": character.get("level"),
            "paragon_level": character.get("paragon_level"),
            "combat_rating": character.get("combat_rating"),
            "resonance": character.get("resonance"),
        },
        "known_primary_attributes": known_attributes,
        "equipment_count": len(profile.get("equipment", []))
            if isinstance(profile.get("equipment", []), list) else None,
        "legendary_gem_count": len(profile.get("legendary_gems", []))
            if isinstance(profile.get("legendary_gems", []), list) else None,
        "set_bonus_entries": len(profile.get("set_bonuses", []))
            if isinstance(profile.get("set_bonuses", []), list) else None,
        "analysis_limits": [
            "Only manually supplied values are summarized.",
            "No build score or recommendation is generated without verified game rules and complete item data."
        ],
    }
