from health_analytics.profile import build_profile

def test_profile_is_reproducible_and_synthetic():
    result = build_profile()
    assert result["synthetic_data"] is True
    assert result["row_count"] > 0
    assert result["duplicate_encounter_ids"] == 0
    assert result["column_count"] == 7
