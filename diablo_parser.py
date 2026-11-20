"""Conservative text parser for Diablo Immortal screenshot OCR.

It extracts explicit text matches only. OCR results are candidates, not verified facts.
"""
from __future__ import annotations

import re
from typing import Any

CLASS_NAMES = (
    "Barbarian", "Blood Knight", "Crusader", "Demon Hunter",
    "Druid", "Monk", "Necromancer", "Tempest", "Wizard",
)
NUMBER_PATTERNS = {
    "combat_rating": r"\bCombat\s+Rating\s*[:：]?\s*([\d,]+)",
    "resonance": r"\bResonance\s*[:：]?\s*([\d,]+)",
    "paragon_level": r"\bParagon(?:\s+Level)?\s*[:：]?\s*(\d+)",
    "level": r"\bLevel\s*[:：]?\s*(\d+)",
}
ATTRIBUTE_PATTERNS = {
    "strength": r"\bStrength\s*[:：]?\s*([\d,]+)",
    "intelligence": r"\bIntelligence\s*[:：]?\s*([\d,]+)",
    "fortitude": r"\bFortitude\s*[:：]?\s*([\d,]+)",
    "vitality": r"\bVitality\s*[:：]?\s*([\d,]+)",
    "willpower": r"\bWillpower\s*[:：]?\s*([\d,]+)",
}
EQUIPMENT_TERMS = (
    "Head", "Chest", "Shoulders", "Legs", "Main Hand", "Off Hand",
    "Neck", "Ring", "Hands", "Waist", "Feet",
)
RARITY_TERMS = ("Normal", "Magic", "Rare", "Legendary", "Set")


def _number_match(pattern: str, text: str) -> int | None:
    match = re.search(pattern, text, flags=re.IGNORECASE)
    return int(match.group(1).replace(",", "")) if match else None


def _whole_term_present(term: str, text: str) -> bool:
    return bool(re.search(rf"(?<!\w){re.escape(term)}(?!\w)", text, flags=re.IGNORECASE))


def parse_game_text(text: str) -> dict[str, Any]:
    """Extract conservative character, equipment, gem and set text candidates."""
    source = text or ""
    found_classes = [name for name in CLASS_NAMES if _whole_term_present(name, source)]
    attributes = {
        name: _number_match(pattern, source)
        for name, pattern in ATTRIBUTE_PATTERNS.items()
    }
    attributes = {key: value for key, value in attributes.items() if value is not None}
    equipment = [term for term in EQUIPMENT_TERMS if _whole_term_present(term, source)]
    rarities = [term for term in RARITY_TERMS if _whole_term_present(term, source)]
    numbers = {key: _number_match(pattern, source)
               for key, pattern in NUMBER_PATTERNS.items()}
    return {
        "character_class_candidates": found_classes,
        **numbers,
        "primary_attributes": attributes,
        "equipment_slots_mentioned": equipment,
        "item_rarity_candidates": rarities,
        "legendary_gem_section_detected": bool(re.search(
            r"\bLegendary\s+Gems?\b", source, flags=re.IGNORECASE
        )),
        "set_bonus_section_detected": bool(re.search(
            r"\bSet\s+Bonus(?:es)?\b", source, flags=re.IGNORECASE
        )),
        "needs_manual_review": True,
        "review_note": "OCR matches are unverified; compare every value with the game screen.",
    }
