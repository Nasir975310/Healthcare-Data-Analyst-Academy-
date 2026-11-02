#!/usr/bin/env python3
"""Execute a small SQLite semantic-layer validation using synthetic fixtures."""
from pathlib import Path
import csv, sqlite3, json, argparse
ROOT = Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output", default="output/semantic_validation.json")
    args=ap.parse_args()
    rows=list(csv.DictReader((ROOT/"data/encounters.csv").open(newline="",encoding="utf-8")))
    db=sqlite3.connect(":memory:")
    db.executescript("""
    CREATE TABLE departments(department_id TEXT PRIMARY KEY, department_name TEXT NOT NULL);
    CREATE TABLE encounters(encounter_id TEXT PRIMARY KEY, patient_id TEXT NOT NULL,
      department_id TEXT NOT NULL REFERENCES departments, encounter_date TEXT NOT NULL,
      encounter_type TEXT NOT NULL, discharge_status TEXT NOT NULL,
      los_days INTEGER NOT NULL CHECK(los_days>=0), charge_inr REAL NOT NULL CHECK(charge_inr>=0));
    """)
    departments={r["department_id"]:r["department_name"] for r in rows}
    db.executemany("INSERT INTO departments VALUES(?,?)",departments.items())
    db.executemany("INSERT INTO encounters VALUES(?,?,?,?,?,?,?,?)",[
      (r["encounter_id"],r["patient_id"],r["department_id"],r["encounter_date"],
       r["encounter_type"],r["discharge_status"],int(r["los_days"]),float(r["charge_inr"])) for r in rows])
    db.executescript((ROOT/"sql/analytics_views.sql").read_text())
    total=db.execute("SELECT COUNT(*) FROM vw_encounter_semantic").fetchone()[0]
    unique=db.execute("SELECT COUNT(DISTINCT patient_id) FROM vw_encounter_semantic").fetchone()[0]
    charges=db.execute("SELECT SUM(charge_inr) FROM vw_encounter_semantic").fetchone()[0]
    assert total==len(rows)
    assert unique<=total
    assert db.execute("SELECT COUNT(*) FROM vw_encounter_semantic WHERE encounter_count<>1").fetchone()[0]==0
    result={"status":"PASS","fixture_rows":len(rows),"semantic_rows":total,
      "unique_patients":unique,"total_charges_inr":round(charges,2),
      "grain":"one row per encounter","synthetic_data":True}
    out=ROOT/args.output; out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps(result,indent=2))
if __name__=="__main__": main()
