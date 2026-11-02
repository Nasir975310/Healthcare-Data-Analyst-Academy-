import json, sqlite3, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from hda_project.pipeline import run_pipeline, PROCESSED, QUARANTINE, REPORTS

def test_end_to_end_pipeline_reconciles():
    result=run_pipeline()
    assert result["raw_rows"] == 241
    assert result["accepted_rows"] + result["quarantined_rows"] == 241
    assert result["quarantined_rows"] > 0
    assert result["synthetic_data"] is True
    with sqlite3.connect(PROCESSED/"hospital_analytics.sqlite") as conn:
        rows, unique_ids = conn.execute("SELECT COUNT(*), COUNT(DISTINCT encounter_id) FROM encounters").fetchone()
    assert rows == result["accepted_rows"]
    assert unique_ids == rows

def test_outputs_are_created():
    run_pipeline()
    for p in [PROCESSED/"clean_encounters.csv",PROCESSED/"quality_report.json",
              QUARANTINE/"quarantined_encounters.csv",PROCESSED/"department_summary.csv",
              PROCESSED/"disposition_summary.csv",REPORTS/"project_report.md",
              REPORTS/"department_encounters.png"]:
        assert p.exists() and p.stat().st_size > 0

def test_quality_rules_find_planted_errors():
    result=run_pipeline()
    issues=result["issue_counts_nonexclusive"]
    assert issues["duplicate_encounter_id"] == 1
    assert issues["invalid_date"] >= 2
    assert issues["invalid_length_of_stay"] >= 2
    assert issues["invalid_department"] >= 2
