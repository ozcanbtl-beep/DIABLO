import json
from pathlib import Path

import pytest

from build_analyzer import load_profile, summarize_profile, validate_profile


def base_profile():
    return {
        "game": "Diablo Immortal",
        "character": {
            "name": "Test",
            "class": "Wizard",
            "level": 60,
            "paragon_level": 300,
            "combat_rating": 25000,
            "resonance": 1000,
            "primary_attributes": {
                "strength": None, "intelligence": 120, "fortitude": None,
                "vitality": None, "willpower": None
            }
        },
        "equipment": [{"slot": "Head", "name": "Example item", "rarity": "Legendary"}],
        "legendary_gems": [{"name": "Example gem", "rank": 2, "awakened": False}],
        "set_bonuses": [{"set_name": "Example set", "pieces": 2, "bonus": "Example bonus"}]
    }


def test_valid_profile_and_summary(tmp_path: Path) -> None:
    profile = base_profile()
    path = tmp_path / "profile.json"
    path.write_text(json.dumps(profile), encoding="utf-8")

    loaded = load_profile(path)
    summary = summarize_profile(loaded)

    assert validate_profile(loaded) == []
    assert summary["valid"] is True
    assert summary["known_primary_attributes"]["intelligence"] == 120
    assert summary["equipment_count"] == 1
    assert summary["equipment_slots_recorded"] == ["Head"]
    assert summary["legendary_gems_recorded"][0]["rank"] == 2
    assert summary["set_bonus_entries"] == 1


def test_invalid_attribute_and_character_stat_are_reported() -> None:
    profile = base_profile()
    profile["character"]["primary_attributes"]["strength"] = -1
    profile["character"]["combat_rating"] = True
    problems = validate_profile(profile)
    assert any("strength" in problem for problem in problems)
    assert any("combat_rating" in problem for problem in problems)


def test_unknown_class_slot_rarity_and_bad_gem_fields_are_reported() -> None:
    profile = base_profile()
    profile["character"]["class"] = "Unknown"
    profile["equipment"][0]["slot"] = "Helmet"
    profile["equipment"][0]["rarity"] = "Mythic"
    profile["legendary_gems"][0]["rank"] = -2
    profile["legendary_gems"][0]["awakened"] = "yes"
    problems = validate_profile(profile)
    assert any("character.class" in problem for problem in problems)
    assert any("equipment[0].slot" in problem for problem in problems)
    assert any("equipment[0].rarity" in problem for problem in problems)
    assert any("rank" in problem for problem in problems)
    assert any("awakened" in problem for problem in problems)


def test_malformed_lists_do_not_crash_summary() -> None:
    profile = base_profile()
    profile["equipment"] = "not a list"
    summary = summarize_profile(profile)
    assert summary["valid"] is False
    assert summary["equipment_count"] is None


def test_non_object_list_entries_are_reported() -> None:
    profile = base_profile()
    profile["equipment"] = ["bad entry"]
    profile["legendary_gems"] = [None]
    profile["set_bonuses"] = [3]
    problems = validate_profile(profile)
    assert any("equipment[0]" in problem for problem in problems)
    assert any("legendary_gems[0]" in problem for problem in problems)
    assert any("set_bonuses[0]" in problem for problem in problems)


def test_missing_profile_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_profile(tmp_path / "missing.json")


def test_non_object_json_raises(tmp_path: Path) -> None:
    path = tmp_path / "bad.json"
    path.write_text("[]", encoding="utf-8")
    with pytest.raises(ValueError, match="JSON object"):
        load_profile(path)
