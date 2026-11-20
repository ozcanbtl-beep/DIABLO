import json
from pathlib import Path

from build_analyzer import load_profile, summarize_profile, validate_profile


def test_template_profile_is_valid(tmp_path: Path) -> None:
    profile = {
        "game": "Diablo Immortal",
        "character": {
            "name": "Test",
            "class": "Wizard",
            "primary_attributes": {
                "strength": None, "intelligence": 120, "fortitude": None,
                "vitality": None, "willpower": None
            }
        },
        "equipment": [{"slot": "Head", "name": "Example item"}],
        "legendary_gems": [{"name": "Example gem", "rank": 2}],
        "set_bonuses": []
    }
    path = tmp_path / "profile.json"
    path.write_text(json.dumps(profile), encoding="utf-8")

    loaded = load_profile(path)
    summary = summarize_profile(loaded)

    assert validate_profile(loaded) == []
    assert summary["valid"] is True
    assert summary["known_primary_attributes"]["intelligence"] == 120
    assert summary["equipment_count"] == 1


def test_invalid_attribute_is_reported() -> None:
    profile = {
        "game": "Diablo Immortal",
        "character": {"primary_attributes": {"strength": -1}}
    }
    assert any("strength" in problem for problem in validate_profile(profile))


def test_missing_profile_raises(tmp_path: Path) -> None:
    try:
        load_profile(tmp_path / "missing.json")
    except FileNotFoundError:
        pass
    else:
        raise AssertionError("Expected FileNotFoundError")
