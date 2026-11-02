from pathlib import Path
import subprocess,sys,json,sqlite3

def test_pipeline_reconciles_and_quarantines(tmp_path):
    base=Path(__file__).resolve().parents[1]
    source=base/"examples/encounters.csv"
    cfg=base/"config/pipeline.json"
    subprocess.run([sys.executable,str(base/"scripts/run_pipeline.py"),"--input",str(source),"--config",str(cfg),"--output-dir",str(tmp_path),"--run-id","test-run"],check=True,capture_output=True,text=True)
    summary=json.loads((tmp_path/"run_summary_test-run.json").read_text())
    assert summary["rows_raw"]==14
    assert summary["rows_accepted"]+summary["rows_rejected"]==14
    assert summary["rows_accepted"]==7 and summary["rows_rejected"]==7
    assert summary["reconciliation"]["staging_equals_raw"]
    with sqlite3.connect(tmp_path/"healthcare_analytics.sqlite") as con:
        assert con.execute("select count(*) from staging_encounters where _run_id='test-run'").fetchone()[0]==14
        assert con.execute("select count(*) from curated_encounters").fetchone()[0]==7

def test_incremental_upsert_does_not_duplicate_primary_keys(tmp_path):
    base=Path(__file__).resolve().parents[1]
    source=base/"examples/encounters.csv";cfg=base/"config/pipeline.json"
    for run in ["one","two"]:
        subprocess.run([sys.executable,str(base/"scripts/run_pipeline.py"),"--input",str(source),"--config",str(cfg),"--output-dir",str(tmp_path),"--run-id",run],check=True,capture_output=True,text=True)
    with sqlite3.connect(tmp_path/"healthcare_analytics.sqlite") as con:
        count=con.execute("select count(*) from curated_encounters").fetchone()[0]
        runs=con.execute("select count(*) from pipeline_runs").fetchone()[0]
    assert count==7 and runs==2
