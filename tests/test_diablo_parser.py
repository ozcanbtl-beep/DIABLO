from diablo_parser import parse_game_text


def test_extracts_explicit_character_values():
    result = parse_game_text(
        "Wizard Level 60 Paragon 120 Combat Rating 3456 Resonance 800 "
        "Strength 123 Intelligence 456"
    )
    assert result["character_class_candidates"] == ["Wizard"]
    assert result["level"] == 60
    assert result["paragon_level"] == 120
    assert result["combat_rating"] == 3456
    assert result["resonance"] == 800
    assert result["primary_attributes"] == {"strength": 123, "intelligence": 456}
    assert result["needs_manual_review"] is True


def test_missing_values_stay_unknown():
    result = parse_game_text("A legendary item was found")
    assert result["combat_rating"] is None
    assert result["character_class_candidates"] == []
    assert result["primary_attributes"] == {}


def test_detects_equipment_slots():
    result = parse_game_text("Head Chest Main Hand Off Hand")
    assert result["equipment_slots_mentioned"] == ["Head", "Chest", "Main Hand", "Off Hand"]
