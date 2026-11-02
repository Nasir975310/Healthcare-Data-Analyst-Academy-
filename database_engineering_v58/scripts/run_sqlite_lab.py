#!/usr/bin/env python3
"""Execute operational and dimensional database labs using Python's sqlite3."""
import argparse,json,sqlite3,hashlib
from pathlib import Path
from datetime import date,timedelta

def main():
 p=argparse.ArgumentParser();p.add_argument("--output-dir",default="output");a=p.parse_args()
 out=Path(a.output_dir).resolve();out.mkdir(parents=True,exist_ok=True);db=out/"database_engineering_lab.sqlite"
 if db.exists():db.unlink()
 con=sqlite3.connect(db);con.execute("PRAGMA foreign_keys=ON")
 con.executescript((Path(__file__).resolve().parents[1]/"sql/sqlite/operational_schema.sql").read_text())
 con.executescript((Path(__file__).resolve().parents[1]/"sql/sqlite/star_schema.sql").read_text())
 departments=["Cardiology","Medicine","Emergency","Nephrology"]
 con.executemany("INSERT INTO departments(department_name) VALUES(?)",[(x,) for x in departments])
 con.executemany("INSERT INTO dim_department(department_name) VALUES(?)",[(x,) for x in departments])
 dimdept={r[1]:r[0] for r in con.execute("SELECT department_key,department_name FROM dim_department")}
 for i in range(1,31):
  token=f"SYN-P{i:03d}";con.execute("INSERT INTO patients(patient_token) VALUES(?)",(token,))
 patients={r[1]:r[0] for r in con.execute("SELECT patient_key,patient_token FROM patients")}
 deptids={r[1]:r[0] for r in con.execute("SELECT department_id,department_name FROM departments")}
 start=date(2026,1,1);records=[]
 for i in range(1,61):
  dt=start+timedelta(days=(i-1)*5)
  dep=departments[(i-1)%len(departments)];token=f"SYN-P{((i-1)%30)+1:03d}"
  los=float((i%7)+1);orders=(i%9)+1;disp=["Discharged","Admitted","Transferred"][i%3]
  records.append((f"SYNTH-{i:03d}",patients[token],deptids[dep],dt.isoformat(),los,disp))
  con.execute("INSERT INTO encounters(encounter_id,patient_key,department_id,admit_date,los_days,disposition) VALUES(?,?,?,?,?,?)",
      (f"SYNTH-{i:03d}",patients[token],deptids[dep],dt.isoformat(),los,disp))
  datekey=int(dt.strftime("%Y%m%d"))
  con.execute("INSERT OR IGNORE INTO dim_date VALUES(?,?,?,?)",(datekey,dt.isoformat(),dt.year,dt.month))
  con.execute("INSERT INTO fact_encounter(encounter_id,date_key,department_key,encounter_count,los_days,order_count) VALUES(?,?,?,?,?,?)",
      (f"SYNTH-{i:03d}",datekey,dimdept[dep],1,los,orders))
 con.commit()
 # Transaction rollback test: failed constraint should leave row count unchanged.
 before=con.execute("SELECT COUNT(*) FROM encounters").fetchone()[0]
 rollback_ok=False
 try:
  con.execute("BEGIN")
  con.execute("INSERT INTO encounters(encounter_id,patient_key,department_id,admit_date,los_days,disposition) VALUES(?,?,?,?,?,?)",
              ("SYNTH-001",patients["SYN-P001"],deptids["Medicine"],"2026-01-01",1,"Discharged"))
  con.commit()
 except sqlite3.IntegrityError:
  con.rollback();rollback_ok=True
 after=con.execute("SELECT COUNT(*) FROM encounters").fetchone()[0]
 # Constraint test
 constraint_ok=False
 try:
  con.execute("INSERT INTO encounters(encounter_id,patient_key,department_id,admit_date,los_days,disposition) VALUES(?,?,?,?,?,?)",
              ("BAD-LOS",patients["SYN-P001"],deptids["Medicine"],"2026-01-01",-1,"Discharged"))
 except sqlite3.IntegrityError:con.rollback();constraint_ok=True
 # Query plan before/after candidate index
 query="SELECT department_id,COUNT(*) FROM encounters WHERE admit_date BETWEEN ? AND ? GROUP BY department_id"
 plan_before=[r[3] for r in con.execute("EXPLAIN QUERY PLAN "+query,("2026-01-01","2026-12-31"))]
 con.execute("CREATE INDEX idx_encounters_admit_department ON encounters(admit_date,department_id)")
 plan_after=[r[3] for r in con.execute("EXPLAIN QUERY PLAN "+query,("2026-01-01","2026-12-31"))]
 dept_summary=con.execute("SELECT * FROM v_department_summary ORDER BY department_name").fetchall()
 monthly=con.execute("""SELECT d.department_name,dt.year,dt.month,SUM(f.encounter_count),ROUND(AVG(f.los_days),2),
 LAG(SUM(f.encounter_count)) OVER(PARTITION BY d.department_name ORDER BY dt.year,dt.month)
 FROM fact_encounter f JOIN dim_department d USING(department_key) JOIN dim_date dt USING(date_key)
 GROUP BY d.department_name,dt.year,dt.month ORDER BY d.department_name,dt.year,dt.month""").fetchall()
 reconciliation={"operational_encounters":after,"fact_rows":con.execute("SELECT COUNT(*) FROM fact_encounter").fetchone()[0],
                "unique_encounter_ids":con.execute("SELECT COUNT(DISTINCT encounter_id) FROM fact_encounter").fetchone()[0],
                "operational_equals_fact":after==con.execute("SELECT COUNT(*) FROM fact_encounter").fetchone()[0]}
 result={"database":str(db),"synthetic_encounters":after,"synthetic_patients":len(patients),"departments":len(departments),
         "transaction_rollback_test":rollback_ok and before==after,"check_constraint_test":constraint_ok,
         "reconciliation":reconciliation,"department_summary":[list(r) for r in dept_summary],
         "monthly_window_function_rows":[list(r) for r in monthly],"query_plan_before_index":plan_before,
         "query_plan_after_index":plan_after,"index_created":True,
         "limitations":["SQLite is used for executable local practice; PostgreSQL scripts require a PostgreSQL server.",
                        "Synthetic records are not clinical data or hospital performance.","EXPLAIN output is workload- and engine-specific."]}
 con.close()
 (out/"lab_results.json").write_text(json.dumps(result,indent=2))
 h=hashlib.sha256(db.read_bytes()).hexdigest()
 (out/"database_manifest.json").write_text(json.dumps({"database_file":db.name,"sha256":h,"bytes":db.stat().st_size,
 "results_file":"lab_results.json","synthetic_only":True},indent=2))
 print(json.dumps(result,indent=2))
if __name__=="__main__":main()
