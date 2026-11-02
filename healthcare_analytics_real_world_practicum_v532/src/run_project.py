"""Reproducible synthetic hospital analytics practicum (Python standard library only)."""
from pathlib import Path
import csv, sqlite3, json, hashlib, datetime
ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/"data"/"raw"; OUT=ROOT/"deliverables"; OUT.mkdir(exist_ok=True)
def read_csv(name):
    with (RAW/name).open(newline="",encoding="utf-8") as f: return list(csv.DictReader(f))
def dump_json(name,obj):
    (OUT/name).write_text(json.dumps(obj,indent=2),encoding="utf-8")
def write_csv(name,headers,rows):
    with (OUT/name).open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f);w.writerow(headers);w.writerows(rows)
def main():
    patients=read_csv("patients.csv"); encounters=read_csv("encounters.csv")
    observations=read_csv("observations.csv"); medications=read_csv("medications.csv")
    pids={r["patient_id"] for r in patients}; eids={r["encounter_id"] for r in encounters}
    def dupes(rows,key):
        seen=set(); dup=set()
        for r in rows:
            v=r[key]
            if v in seen: dup.add(v)
            seen.add(v)
        return sorted(dup)
    quality={
      "source_rows":{"patients":len(patients),"encounters":len(encounters),"observations":len(observations),"medications":len(medications)},
      "duplicate_keys":{"patients":dupes(patients,"patient_id"),"encounters":dupes(encounters,"encounter_id"),"observations":dupes(observations,"observation_id"),"medications":dupes(medications,"medication_id")},
      "encounters_with_unknown_patient":[r["encounter_id"] for r in encounters if r["patient_id"] not in pids],
      "observations_with_unknown_encounter":[r["observation_id"] for r in observations if r["encounter_id"] not in eids],
      "medications_with_unknown_encounter":[r["medication_id"] for r in medications if r["encounter_id"] not in eids],
      "invalid_encounter_dates":[r["encounter_id"] for r in encounters if not valid_date(r["encounter_date"])],
      "invalid_observation_values":[r["observation_id"] for r in observations if not is_number(r["value"])],
      "unknown_observation_units":[r["observation_id"] for r in observations if r["unit"] not in {"mmHg"}]
    }
    db=OUT/"hospital_analytics.sqlite"
    if db.exists(): db.unlink()
    con=sqlite3.connect(db); con.execute("PRAGMA foreign_keys=ON")
    con.executescript("""
    CREATE TABLE dim_patient(patient_id TEXT PRIMARY KEY,gender TEXT,birth_date TEXT,residence TEXT,region TEXT);
    CREATE TABLE stg_encounter(encounter_id TEXT PRIMARY KEY,patient_id TEXT,encounter_date TEXT,encounter_type TEXT,status TEXT);
    CREATE TABLE fact_encounter(encounter_id TEXT PRIMARY KEY,patient_id TEXT NOT NULL REFERENCES dim_patient(patient_id),encounter_date TEXT,encounter_type TEXT,status TEXT);
    CREATE TABLE fact_observation(observation_id TEXT PRIMARY KEY,encounter_id TEXT NOT NULL REFERENCES fact_encounter(encounter_id),measure TEXT,value REAL,unit TEXT);
    CREATE TABLE fact_medication(medication_id TEXT PRIMARY KEY,encounter_id TEXT NOT NULL REFERENCES fact_encounter(encounter_id),medication TEXT,drug_class TEXT,is_active INTEGER);
    """)
    con.executemany("INSERT INTO dim_patient VALUES(:patient_id,:gender,:birth_date,:residence,:region)",patients)
    con.executemany("INSERT INTO stg_encounter VALUES(:encounter_id,:patient_id,:encounter_date,:encounter_type,:status)",encounters)
    accepted=[r for r in encounters if r["patient_id"] in pids and valid_date(r["encounter_date"])]
    con.executemany("INSERT INTO fact_encounter VALUES(:encounter_id,:patient_id,:encounter_date,:encounter_type,:status)",accepted)
    accepted_ids={r["encounter_id"] for r in accepted}
    valid_obs=[r for r in observations if r["encounter_id"] in accepted_ids and is_number(r["value"]) and r["unit"]=="mmHg"]
    valid_meds=[r for r in medications if r["encounter_id"] in accepted_ids]
    con.executemany("INSERT INTO fact_observation VALUES(:observation_id,:encounter_id,:measure,:value,:unit)",valid_obs)
    con.executemany("INSERT INTO fact_medication VALUES(:medication_id,:encounter_id,:medication,:drug_class,:is_active)",valid_meds)
    con.commit()
    # Aggregate facts independently to avoid observation x medication fanout.
    kpis={
      "patients":con.execute("SELECT COUNT(*) FROM dim_patient").fetchone()[0],
      "source_encounters":len(encounters),
      "curated_encounters":con.execute("SELECT COUNT(*) FROM fact_encounter").fetchone()[0],
      "completed_encounters":con.execute("SELECT COUNT(*) FROM fact_encounter WHERE status='Completed'").fetchone()[0],
      "cancelled_encounters":con.execute("SELECT COUNT(*) FROM fact_encounter WHERE status='Cancelled'").fetchone()[0],
      "scheduled_encounters":con.execute("SELECT COUNT(*) FROM fact_encounter WHERE status='Scheduled'").fetchone()[0],
      "medication_orders":con.execute("SELECT COUNT(*) FROM fact_medication").fetchone()[0],
      "mean_systolic_bp":round(con.execute("SELECT AVG(value) FROM fact_observation WHERE measure='Systolic BP'").fetchone()[0],2),
      "mean_diastolic_bp":round(con.execute("SELECT AVG(value) FROM fact_observation WHERE measure='Diastolic BP'").fetchone()[0],2)
    }
    monthly=con.execute("SELECT substr(encounter_date,1,7),COUNT(*),SUM(status='Completed'),SUM(status='Cancelled'),SUM(status='Scheduled') FROM fact_encounter GROUP BY 1 ORDER BY 1").fetchall()
    drug=con.execute("SELECT drug_class,COUNT(*) FROM fact_medication GROUP BY 1 ORDER BY 2 DESC").fetchall()
    by_type=con.execute("SELECT encounter_type,COUNT(*) FROM fact_encounter GROUP BY 1 ORDER BY 2 DESC").fetchall()
    fk=con.execute("PRAGMA foreign_key_check").fetchall()
    integrity=con.execute("PRAGMA integrity_check").fetchone()[0]
    quality["curation"]={"accepted_encounters":len(accepted),"rejected_encounters":len(encounters)-len(accepted),"accepted_observations":len(valid_obs),"rejected_observations":len(observations)-len(valid_obs),"accepted_medications":len(valid_meds),"rejected_medications":len(medications)-len(valid_meds)}
    quality["warehouse"]={"integrity_check":integrity,"foreign_key_violations":len(fk)}
    dump_json("data_quality_report.json",quality); dump_json("kpi_summary.json",kpis)
    write_csv("monthly_encounters.csv",["year_month","encounters","completed","cancelled","scheduled"],monthly)
    write_csv("medication_class_utilization.csv",["drug_class","orders"],drug)
    write_csv("encounters_by_type.csv",["encounter_type","encounters"],by_type)
    # Source file manifest
    manifest={}
    for f in sorted(RAW.glob("*.csv")):
        manifest[f.name]=hashlib.sha256(f.read_bytes()).hexdigest()
    dump_json("source_manifest.json",manifest)
    con.close()
    return {"kpis":kpis,"quality":quality}
def valid_date(s):
    try: datetime.date.fromisoformat(s); return True
    except (ValueError,TypeError): return False
def is_number(s):
    try: float(s); return True
    except (ValueError,TypeError): return False
if __name__=="__main__": print(json.dumps(main(),indent=2))
