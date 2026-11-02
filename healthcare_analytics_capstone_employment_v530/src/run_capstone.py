"""Run a deterministic, synthetic healthcare analytics capstone.
Uses only Python standard library. Writes SQLite warehouse and CSV/JSON QA outputs.
"""
from pathlib import Path
import csv, sqlite3, json, hashlib
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data"; OUT=ROOT/"reports"; OUT.mkdir(exist_ok=True)
def load(name):
    with (DATA/name).open(newline="",encoding="utf-8") as f: return list(csv.DictReader(f))
def unique(rows,key):
    vals=[r[key] for r in rows]; return len(vals)==len(set(vals))
def main():
    p,e,o,m=map(load,["patients.csv","encounters.csv","observations.csv","medications.csv"])
    pids={r["patient_id"] for r in p}; eids={r["encounter_id"] for r in e}
    quality={
      "patient_primary_key_unique":unique(p,"patient_id"),
      "encounter_primary_key_unique":unique(e,"encounter_id"),
      "observation_primary_key_unique":unique(o,"observation_id"),
      "medication_primary_key_unique":unique(m,"medication_id"),
      "encounters_with_unknown_patient":[r["encounter_id"] for r in e if r["patient_id"] not in pids],
      "observations_with_unknown_encounter":[r["observation_id"] for r in o if r["encounter_id"] not in eids],
      "medications_with_unknown_encounter":[r["medication_id"] for r in m if r["encounter_id"] not in eids],
      "missing_patient_region":[r["patient_id"] for r in p if not r["region"].strip()],
    }
    db=OUT/"capstone_warehouse.sqlite"
    if db.exists(): db.unlink()
    con=sqlite3.connect(db)
    con.executescript("""
    PRAGMA foreign_keys=ON;
    CREATE TABLE dim_patient(patient_id TEXT PRIMARY KEY, gender TEXT, birth_date TEXT, region TEXT);
    CREATE TABLE stg_encounter(encounter_id TEXT PRIMARY KEY, patient_id TEXT, encounter_date TEXT, encounter_type TEXT, status TEXT);
    CREATE TABLE fact_encounter(encounter_id TEXT PRIMARY KEY, patient_id TEXT NOT NULL REFERENCES dim_patient(patient_id), encounter_date TEXT, encounter_type TEXT, status TEXT);
    CREATE TABLE fact_observation(observation_id TEXT PRIMARY KEY, encounter_id TEXT NOT NULL REFERENCES fact_encounter(encounter_id), measure TEXT, value REAL, unit TEXT);
    CREATE TABLE fact_medication(medication_id TEXT PRIMARY KEY, encounter_id TEXT NOT NULL REFERENCES fact_encounter(encounter_id), medication TEXT, drug_class TEXT, is_active INTEGER);
    """)
    con.executemany("INSERT INTO dim_patient VALUES(:patient_id,:gender,:birth_date,:region)",p)
    con.executemany("INSERT INTO stg_encounter VALUES(:encounter_id,:patient_id,:encounter_date,:encounter_type,:status)",e)
    accepted_e=[r for r in e if r["patient_id"] in pids]
    con.executemany("INSERT INTO fact_encounter VALUES(:encounter_id,:patient_id,:encounter_date,:encounter_type,:status)",accepted_e)
    con.executemany("INSERT INTO fact_observation VALUES(:observation_id,:encounter_id,:measure,:value,:unit)",[r for r in o if r["encounter_id"] in {x["encounter_id"] for x in accepted_e}])
    con.executemany("INSERT INTO fact_medication VALUES(:medication_id,:encounter_id,:medication,:drug_class,:is_active)",[r for r in m if r["encounter_id"] in {x["encounter_id"] for x in accepted_e}])
    con.commit()
    kpi={
      "patient_count":len(p),
      "encounter_count":len(e),
      "completed_encounters":sum(r["status"]=="Completed" for r in e),
      "cancelled_encounters":sum(r["status"]=="Cancelled" for r in e),
      "medication_orders":len(m),
      "unique_medications":len({r["medication"] for r in m}),
      "mean_systolic_bp":round(sum(float(r["value"]) for r in o if r["measure"]=="Systolic BP")/sum(r["measure"]=="Systolic BP" for r in o),2),
      "mean_diastolic_bp":round(sum(float(r["value"]) for r in o if r["measure"]=="Diastolic BP")/sum(r["measure"]=="Diastolic BP" for r in o),2),
      "systolic_readings_ge_140":sum(r["measure"]=="Systolic BP" and float(r["value"])>=140 for r in o)
    }
    checks=con.execute("PRAGMA foreign_key_check").fetchall()
    integrity=con.execute("PRAGMA integrity_check").fetchone()[0]
    result={"synthetic_data":True,"quality":quality,"kpis":kpi,"sqlite":{"integrity_check":integrity,"foreign_key_violations":len(checks),"rejected_encounter_rows":len(e)-len(accepted_e)}}
    (OUT/"capstone_results.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    with (OUT/"kpi_summary.csv").open("w",newline="",encoding="utf-8") as f:
      w=csv.writer(f);w.writerow(["metric","value"]);w.writerows(kpi.items())
    con.close()
    return result
if __name__=="__main__":
    print(json.dumps(main(),indent=2))
