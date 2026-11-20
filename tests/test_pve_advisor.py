from pve_advisor import analyze_pve_profile


def test_pve_report_uses_only_recorded_profile_facts():
    profile = {
        "character": {"class": "Druid", "paragon_level": 1635, "combat_rating": 62000},
        "combat_stats": {"damage": 27000, "life": 338000},
        "combat_preferences": {"activities": ["PvE", "PvP"]},
        "skills": {
            "player_reported_names": ["Heyelan", "Ateşli Hortum", "Kuduz Kudret", "Kuzgun Sürüsü"],
            "combination_notes": ["Ateşli Hortum is combined with Kuzgun Sürüsü."],
            "role_notes": ["Heyelan is used as a basic attack."]
        },
        "equipment_overview": {
            "purple_primary_weapon": {
                "name": "Ebedi Döngü", "type": "Asa",
                "upgrade_tier": "purple", "combat_rating": 3301
            },
            "purple_chest_armor": {
                "name": "Verimlilik Ceketi",
                "upgrade_tier": "purple", "combat_rating": 3287
            }
        },
        "equipment": [],
        "legendary_gems": [],
        "set_bonuses": [],
    }

    report = analyze_pve_profile(profile)
    assert report["mode"] == "PvE"
    assert report["pve_enabled_in_preferences"] is True
    assert report["character"]["damage"] == 27000
    assert report["player_reported_skills"][0] == "Heyelan"
    assert report["known_upgraded_equipment"][0]["name"] == "Ebedi Döngü"
    assert any("set bonuses" in item for item in report["missing_information"])
    assert "optimal build" in report["assessment"]


def test_pve_report_handles_missing_sections_without_crashing():
    report = analyze_pve_profile({"character": {}, "skills": {}})
    assert report["mode"] == "PvE"
    assert report["player_reported_skills"] == []
    assert report["pve_enabled_in_preferences"] is False
    assert report["missing_information"]
