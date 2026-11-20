"""Conservative PvE build report based only on player-confirmed profile data."""
from __future__ import annotations

from typing import Any


def analyze_pve_profile(profile: dict[str, Any]) -> dict[str, Any]:
    """Build a factual PvE report without guessing game mechanics or item rankings."""
    character = profile.get("character") or {}
    skills = profile.get("skills") or {}
    preferences = profile.get("combat_preferences") or {}
    overview = profile.get("equipment_overview") or {}

    activities = preferences.get("activities") or []
    pve_enabled = "PvE" in activities

    known_skills = skills.get("player_reported_names") or []
    combos = skills.get("combination_notes") or []
    roles = skills.get("role_notes") or []

    known_equipment: list[dict[str, Any]] = []
    for key in ("purple_primary_weapon", "purple_chest_armor"):
        item = overview.get(key)
        if isinstance(item, dict):
            known_equipment.append({
                "slot": "primary weapon" if key == "purple_primary_weapon" else "chest armor",
                "name": item.get("name"),
                "type": item.get("type"),
                "upgrade_tier": item.get("upgrade_tier"),
                "combat_rating": item.get("combat_rating"),
            })

    missing: list[str] = []
    if not pve_enabled:
        missing.append("PvE is not listed in the saved activity preferences.")
    if not known_skills:
        missing.append("No player-confirmed skills are recorded.")
    if not profile.get("legendary_gems"):
        missing.append("Legendary gem names and ranks are not recorded.")
    if not profile.get("set_bonuses"):
        missing.append("Active green set bonuses are not recorded.")
    if not profile.get("equipment"):
        missing.append("Full equipped items and their legendary essences are not recorded.")
    if not skills.get("verified_skill_variants"):
        missing.append("Exact skill variants and their selected legendary modifiers are not verified.")

    return {
        "mode": "PvE",
        "purpose": "Monster-focused build review",
        "character": {
            "class": character.get("class"),
            "paragon_level": character.get("paragon_level"),
            "combat_rating": character.get("combat_rating"),
            "damage": (profile.get("combat_stats") or {}).get("damage"),
            "life": (profile.get("combat_stats") or {}).get("life"),
        },
        "pve_enabled_in_preferences": pve_enabled,
        "player_reported_skills": known_skills,
        "player_reported_skill_roles": roles,
        "player_reported_combinations": combos,
        "known_upgraded_equipment": known_equipment,
        "assessment": (
            "The saved profile confirms a player-reported PvE skill setup. "
            "It is not enough to rank damage or declare an optimal build."
        ),
        "next_review_points": [
            "Compare the current skill combination against the player's own results on groups of monsters and single targets.",
            "Record the legendary modifiers on the equipped items before suggesting replacements.",
            "Record active set bonuses and legendary gem names/ranks before estimating build impact.",
        ],
        "missing_information": missing,
        "safety_note": "This is an offline advisory report. It does not control the game or automate combat.",
    }
