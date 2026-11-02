import importlib.util, tempfile, pathlib, csv, json
SCRIPT=pathlib.Path(__file__).parents[1]/"scripts/run_pipeline.py"
spec=importlib.util.spec_from_file_location("pipeline",SCRIPT); pipeline=importlib.util.module_from_spec(spec); spec.loader.exec_module(pipeline)
def test_pipeline_reconciles_fixture(tmp_path):
    result=pipeline.run(SCRIPT.parents[1]/"data/inbound/encounters.csv",tmp_path)
    assert result["rows_read"]==10
    assert result["accepted_this_run"]==10
    assert result["quarantined_this_run"]==0
    assert result["warehouse_rows_after_run"]==10
    assert (tmp_path/"quality_report.html").exists()
def test_quarantine_bad_rows(tmp_path):
    source=tmp_path/"bad.csv"
    source.write_text("encounter_id,patient_id,department_id,encounter_date,encounter_type,discharge_status,los_days,charge_inr\nX1,P1,D1,not-a-date,OPD,Discharged,-2,-1\nX1,P1,D1,2026-01-01,OPD,Discharged,0,1\n")
    result=pipeline.run(source,tmp_path/"out")
    assert result["accepted_this_run"]==0
    assert result["quarantined_this_run"]==2
    assert result["status"]=="PASS_WITH_QUARANTINE"
