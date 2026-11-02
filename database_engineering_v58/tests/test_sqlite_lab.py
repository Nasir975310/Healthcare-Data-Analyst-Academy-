from pathlib import Path
import subprocess,sys,json,sqlite3

def test_database_lab_builds_models_and_queries(tmp_path):
    base=Path(__file__).resolve().parents[1]
    subprocess.run([sys.executable,str(base/"scripts/run_sqlite_lab.py"),"--output-dir",str(tmp_path)],check=True,capture_output=True,text=True)
    r=json.loads((tmp_path/"lab_results.json").read_text())
    assert r["synthetic_encounters"]==60 and r["synthetic_patients"]==30
    assert r["transaction_rollback_test"] and r["check_constraint_test"]
    assert r["reconciliation"]["operational_equals_fact"]
    assert len(r["monthly_window_function_rows"])>0
    with sqlite3.connect(tmp_path/"database_engineering_lab.sqlite") as c:
        assert c.execute("select count(*) from fact_encounter").fetchone()[0]==60
        assert c.execute("select count(*) from v_department_summary").fetchone()[0]==4
