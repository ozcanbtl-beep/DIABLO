"""Validate and summarize a manually captured Diablo Immortal character profile.

No game memory access, network calls, account access, or gameplay automation.
The tool reports supplied values only; it does not invent build rankings.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ATTRIBUTE_NAMES = ("strength", "intelligence", "fortitude", "vitality", "willpower")
CHARACTER_NUMBER_FIELDS = ("level", "paragon_level", "combat_rating", "resonance")
CHARACTER_TEXT_FIELDS = ("name", "class")
EQUIPMENT_SLOTS = (
    "Head", "Chest", "Shoulders", "Legs", "Main Hand", "Off Hand",
    "Neck", "Ring", "Hands", "Waist", "Feet",
)
ITEM_RARITIES = ("Normal", "Magic", "Rare", "Legendary", "Set")
CHARACTER_CLASSES = (
    "Barbarian", "Blood Knight", "Crusader", "Demon Hunter", "Druid",
    "Monk", "Necromancer", "Tempest", "Wizard",
)


def load_profile(profile_path: str | Path) -> dict[str, Any]:
    """Load a profile JSON object from disk."""
    path = Path(profile_path)
    if not path.is_file():
        raise FileNotFoundError(f"Profile not found: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Profile root must be a JSON object.")
    return data


def _validate_non_negative_number(value: Any) -> bool:
    return value is None or (
        not isinstance(value, bool)
        and isinstance(value, (int, float))
        and value >= 0
    )


def _validate_optional_text_fields(item: dict[str, Any], fields: tuple[str, ...],
                                   prefix: str, problems: list[str]) -> None:
    for field in fields:
        value = item.get(field)
        if value is not None and not isinstance(value, str):
            problems.append(f"{prefix}.{field} must be text or null.")


def validate_profile(profile: dict[str, Any]) -> list[str]:
    """Return human-readable validation problems; empty means structurally valid."""
    problems: list[str] = []
    if not isinstance(profile, dict):
        return ["profile must be an object."]
    if profile.get("game") != "Diablo Immortal":
        problems.append('game must be "Diablo Immortal".')

    character = profile.get("character")
    if not isinstance(character, dict):
        problems.append("character must be an object.")
        character = {}
    _validate_optional_text_fields(character, CHARACTER_TEXT_FIELDS, "character", problems)
    class_name = character.get("class")
    if class_name and class_name not in CHARACTER_CLASSES:
        problems.append("character.class must be a recognized Diablo Immortal class or empty.")

    for field in CHARACTER_NUMBER_FIELDS:
        value = character.get(field)
        if not _validate_non_negative_number(value):
            problems.append(f"character.{field} must be a non-negative number or null.")

    attributes = character.get("primary_attributes", {})
    if not isinstance(attributes, dict):
        problems.append("character.primary_attributes must be an object.")
    else:
        for name in ATTRIBUTE_NAMES:
            if not _validate_non_negative_number(attributes.get(name)):
                problems.append(f"primary attribute {name} must be a non-negative number or null.")

    for field in ("equipment", "legendary_gems", "set_bonuses"):
        if field in profile and not isinstance(profile[field], list):
            problems.append(f"{field} must be a list.")

    equipment = profile.get("equipment", [])
    if isinstance(equipment, list):
        for index, item in enumerate(equipment):
            prefix = f"equipment[{index}]"
            if not isinstance(item, dict):
                problems.append(f"{prefix} must be an object.")
                continue
            if not isinstance(item.get("slot", ""), str):
                problems.append(f"{prefix}.slot must be text.")
            elif item.get("slot") and item["slot"] not in EQUIPMENT_SLOTS:
                problems.append(f"{prefix}.slot must be a recognized equipment slot.")
            _validate_optional_text_fields(
                item, ("name", "rarity", "set_name", "gem_name", "notes"),
                prefix, problems
            )
            if item.get("rarity") and item["rarity"] not in ITEM_RARITIES:
                problems.append(f"{prefix}.rarity must be a recognized rarity or empty.")

    gems = profile.get("legendary_gems", [])
    if isinstance(gems, list):
        for index, gem in enumerate(gems):
            prefix = f"legendary_gems[{index}]"
            if not isinstance(gem, dict):
                problems.append(f"{prefix} must be an object.")
                continue
            _validate_optional_text_fields(gem, ("name", "notes"), prefix, problems)
            rank = gem.get("rank")
            if rank is not None and (
                isinstance(rank, bool) or not isinstance(rank, int) or rank < 0
            ):
                problems.append(f"{prefix}.rank must be a non-negative integer or null.")
            awakened = gem.get("awakened")
            if awakened is not None and not isinstance(awakened, bool):
                problems.append(f"{prefix}.awakened must be true, false, or null.")

    bonuses = profile.get("set_bonuses", [])
    if isinstance(bonuses, list):
        for index, bonus in enumerate(bonuses):
            prefix = f"set_bonuses[{index}]"
            if not isinstance(bonus, dict):
                problems.append(f"{prefix} must be an object.")
                continue
            _validate_optional_text_fields(bonus, ("set_name", "bonus", "notes"), prefix, problems)
            pieces = bonus.get("pieces")
            if pieces is not None and (
                isinstance(pieces, bool) or not isinstance(pieces, int) or pieces < 0
            ):
                problems.append(f"{prefix}.pieces must be a non-negative integer or null.")

    notes = profile.get("notes")
    if notes is not None and not isinstance(notes, str):
        problems.append("notes must be text or null.")
    return problems


def summarize_profile(profile: dict[str, Any]) -> dict[str, Any]:
    """Return a safe, factual summary of the values supplied in a profile."""
    problems = validate_profile(profile)
    character = profile.get("character", {}) if isinstance(profile, dict) else {}
    if not isinstance(character, dict):
        character = {}
    attributes = character.get("primary_attributes", {})
    if not isinstance(attributes, dict):
        attributes = {}
    known_attributes = {
        key: value for key, value in attributes.items()
        if key in ATTRIBUTE_NAMES and value is not None
    }

    def count_entries(field: str) -> int | None:
        value = profile.get(field, []) if isinstance(profile, dict) else []
        return len(value) if isinstance(value, list) else None

    equipment = profile.get("equipment", []) if isinstance(profile, dict) else []
    gems = profile.get("legendary_gems", []) if isinstance(profile, dict) else []
    bonuses = profile.get("set_bonuses", []) if isinstance(profile, dict) else []
    return {
        "valid": not problems,
        "problems": problems,
        "character": {
            "name": character.get("name") or "Not provided",
            "class": character.get("class") or "Not provided",
            **{field: character.get(field) for field in CHARACTER_NUMBER_FIELDS},
        },
        "known_primary_attributes": known_attributes,
        "equipment_count": count_entries("equipment"),
        "equipment_slots_recorded": [
            item.get("slot") for item in equipment
            if isinstance(item, dict) and item.get("slot")
        ] if isinstance(equipment, list) else [],
        "legendary_gem_count": count_entries("legendary_gems"),
        "legendary_gems_recorded": [
            {"name": gem.get("name") or "Not provided", "rank": gem.get("rank")}
            for gem in gems if isinstance(gem, dict)
        ] if isinstance(gems, list) else [],
        "set_bonus_entries": count_entries("set_bonuses"),
        "analysis_limits": [
            "Only manually supplied values are summarized.",
            "Unknown values should remain null; do not guess missing stats.",
            "No build score or recommendation is generated without verified game rules and complete item data.",
        ],
    }
