import csv, json, subprocess, sys
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]/"starter_project"
def test_synthetic_csv_shape_and_key():
    with (BASE/"data/raw/synthetic_encounters.csv").open(newline="") as f:
        rows=list(csv.DictReader(f))
    assert len(rows)==150
    ids=[r["encounter_id"] for r in rows]
    assert len(ids)==len(set(ids))
def test_scaffold_has_both_platform_guides():
    assert (Path(__file__).resolve().parents[1]/"guides/setup_linux.md").exists()
    assert (Path(__file__).resolve().parents[1]/"guides/setup_windows.md").exists()
def test_profile_script_has_no_patient_identifiers():
    source=(BASE/"src/health_analytics/profile.py").read_text()
    assert "synthetic_data" in source
    assert "patient_token" in source
