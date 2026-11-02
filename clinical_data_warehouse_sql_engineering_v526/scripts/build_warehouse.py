#!/usr/bin/env python3
"""Build a synthetic clinical star-schema warehouse from v5.25 FHIR ETL outputs."""
import argparse,csv,hashlib,json,sqlite3
from pathlib import Path
from datetime import datetime,date

def rows(path):
    with open(path,newline="",encoding="utf-8") as f: return list(csv.DictReader(f))
def as_num(v):
    if v in ("",None): return None
    try: return float(v)
    except (TypeError,ValueError): return None
def date_key(value):
    if not value: return None
    try: return int(value[:10].replace("-",""))
    except Exception: return None
def create_schema(db):
    db.executescript("""
    PRAGMA foreign_keys=ON;
    CREATE TABLE dim_date(date_key INTEGER PRIMARY KEY, full_date TEXT UNIQUE, year INTEGER, month INTEGER, day INTEGER, quarter INTEGER);
    CREATE TABLE dim_patient(patient_key INTEGER PRIMARY KEY, patient_id TEXT NOT NULL, gender TEXT, birth_date TEXT, valid_from TEXT NOT NULL, valid_to TEXT, is_current INTEGER NOT NULL, version INTEGER NOT NULL, UNIQUE(patient_id,version));
    CREATE TABLE dim_encounter(encounter_key INTEGER PRIMARY KEY, encounter_id TEXT UNIQUE NOT NULL, patient_id TEXT NOT NULL, status TEXT, class_code TEXT, start_datetime TEXT, end_datetime TEXT);
    CREATE TABLE dim_terminology(terminology_key INTEGER PRIMARY KEY, source_system TEXT, source_code TEXT, display TEXT, mapped_system TEXT, mapped_concept TEXT, mapping_status TEXT, UNIQUE(source_system,source_code));
    CREATE TABLE fact_observation(observation_key INTEGER PRIMARY KEY, observation_id TEXT UNIQUE, patient_key INTEGER, encounter_key INTEGER, date_key INTEGER, terminology_key INTEGER, value_numeric REAL, unit TEXT, FOREIGN KEY(patient_key) REFERENCES dim_patient(patient_key), FOREIGN KEY(encounter_key) REFERENCES dim_encounter(encounter_key), FOREIGN KEY(date_key) REFERENCES dim_date(date_key), FOREIGN KEY(terminology_key) REFERENCES dim_terminology(terminology_key));
    CREATE TABLE fact_medication_request(medication_key INTEGER PRIMARY KEY, medication_request_id TEXT UNIQUE, patient_key INTEGER, encounter_key INTEGER, authored_date_key INTEGER, status TEXT, medication_display TEXT, source_system TEXT, source_code TEXT, FOREIGN KEY(patient_key) REFERENCES dim_patient(patient_key), FOREIGN KEY(encounter_key) REFERENCES dim_encounter(encounter_key), FOREIGN KEY(authored_date_key) REFERENCES dim_date(date_key));
    CREATE TABLE mart_encounter_summary(encounter_id TEXT PRIMARY KEY, patient_id TEXT, encounter_date TEXT, encounter_status TEXT, observation_count INTEGER, medication_request_count INTEGER, distinct_observation_concepts INTEGER, systolic_mean REAL, diastolic_mean REAL);
    CREATE TABLE mart_patient_cohort(patient_id TEXT PRIMARY KEY, qualifying_encounters INTEGER, first_qualifying_encounter TEXT, last_qualifying_encounter TEXT);
    CREATE INDEX ix_obs_patient_date ON fact_observation(patient_key,date_key);
    CREATE INDEX ix_obs_concept_date ON fact_observation(terminology_key,date_key);
    CREATE INDEX ix_med_patient_date ON fact_medication_request(patient_key,authored_date_key);
    """)
def load_date(db, raw):
    if not raw: return None
    d=raw[:10]
    try: dt=date.fromisoformat(d)
    except ValueError: return None
    k=int(dt.strftime("%Y%m%d"))
    db.execute("INSERT OR IGNORE INTO dim_date VALUES(?,?,?,?,?,?)",(k,dt.isoformat(),dt.year,dt.month,dt.day,(dt.month-1)//3+1))
    return k
def run(input_dir, output_db, cohort_status="finished"):
    src=Path(input_dir); output=Path(output_db); output.parent.mkdir(parents=True,exist_ok=True)
    for name in ["patients.csv","encounters.csv","observations.csv","medications.csv"]:
        if not (src/name).exists(): raise FileNotFoundError(f"Missing {src/name}; run v5.25 FHIR ETL first.")
    patients=rows(src/"patients.csv"); encounters=rows(src/"encounters.csv")
    observations=rows(src/"observations.csv"); medications=rows(src/"medications.csv")
    if output.exists(): output.unlink()
    db=sqlite3.connect(output); create_schema(db)
    patient_current={}
    for p in patients:
        db.execute("INSERT INTO dim_patient(patient_id,gender,birth_date,valid_from,valid_to,is_current,version) VALUES(?,?,?,?,?,?,?)",
          (p["patient_id"],p.get("gender"),p.get("birth_date"),"1900-01-01",None,1,1))
        patient_current[p["patient_id"]]=db.execute("SELECT patient_key FROM dim_patient WHERE patient_id=? AND is_current=1",(p["patient_id"],)).fetchone()[0]
    encounter_keys={}
    for e in encounters:
        db.execute("INSERT INTO dim_encounter(encounter_id,patient_id,status,class_code,start_datetime,end_datetime) VALUES(?,?,?,?,?,?)",
          (e["encounter_id"],e["patient_id"],e.get("status"),e.get("class_code"),e.get("start"),e.get("end")))
        encounter_keys[e["encounter_id"]]=db.execute("SELECT encounter_key FROM dim_encounter WHERE encounter_id=?",(e["encounter_id"],)).fetchone()[0]
        load_date(db,e.get("start"))
    term_keys={}
    for o in observations:
        key=(o.get("source_system") or "",o.get("source_code") or "")
        db.execute("""INSERT OR IGNORE INTO dim_terminology(source_system,source_code,display,mapped_system,mapped_concept,mapping_status)
          VALUES(?,?,?,?,?,?)""",(key[0],key[1],o.get("display"),o.get("mapped_system"),o.get("mapped_concept"),"mapped_illustrative" if o.get("mapped_concept") else "unmapped"))
        term_keys[key]=db.execute("SELECT terminology_key FROM dim_terminology WHERE source_system=? AND source_code=?",key).fetchone()[0]
        dkey=load_date(db,o.get("effective_datetime"))
        db.execute("""INSERT INTO fact_observation(observation_id,patient_key,encounter_key,date_key,terminology_key,value_numeric,unit)
          VALUES(?,?,?,?,?,?,?)""",(o["observation_id"],patient_current.get(o["patient_id"]),encounter_keys.get(o["encounter_id"]),dkey,term_keys[key],as_num(o.get("value")),o.get("unit")))
    for m in medications:
        dkey=load_date(db,m.get("authored_on"))
        db.execute("""INSERT INTO fact_medication_request(medication_request_id,patient_key,encounter_key,authored_date_key,status,medication_display,source_system,source_code)
          VALUES(?,?,?,?,?,?,?,?)""",(m["medication_request_id"],patient_current.get(m["patient_id"]),encounter_keys.get(m["encounter_id"]),dkey,m.get("status"),m.get("medication_display"),m.get("source_system"),m.get("source_code")))
    # Encounter mart aggregates child facts independently to preserve fact grain.
    db.execute("""
      INSERT INTO mart_encounter_summary
      SELECT e.encounter_id,e.patient_id,substr(e.start_datetime,1,10),e.status,
        COALESCE(o.n,0),COALESCE(m.n,0),COALESCE(o.concepts,0),o.sbp,o.dbp
      FROM dim_encounter e
      LEFT JOIN (
        SELECT f.encounter_key,COUNT(*) n,COUNT(DISTINCT t.mapped_concept) concepts,
          AVG(CASE WHEN t.source_code='8480-6' THEN f.value_numeric END) sbp,
          AVG(CASE WHEN t.source_code='8462-4' THEN f.value_numeric END) dbp
        FROM fact_observation f LEFT JOIN dim_terminology t ON t.terminology_key=f.terminology_key
        GROUP BY f.encounter_key
      ) o ON o.encounter_key=e.encounter_key
      LEFT JOIN (SELECT encounter_key,COUNT(*) n FROM fact_medication_request GROUP BY encounter_key) m
        ON m.encounter_key=e.encounter_key
    """)
    db.execute("""INSERT INTO mart_patient_cohort
      SELECT patient_id,COUNT(*),MIN(encounter_date),MAX(encounter_date)
      FROM mart_encounter_summary WHERE encounter_status=? GROUP BY patient_id""",(cohort_status,))
    db.commit()
    counts={}
    for t in ["dim_date","dim_patient","dim_encounter","dim_terminology","fact_observation","fact_medication_request","mart_encounter_summary","mart_patient_cohort"]:
        counts[t]=db.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    fk=db.execute("PRAGMA foreign_key_check").fetchall()
    integrity=db.execute("PRAGMA integrity_check").fetchone()[0]
    db.close()
    manifest={"database":output.name,"sha256":hashlib.sha256(output.read_bytes()).hexdigest(),"table_counts":counts,
      "foreign_key_violations":len(fk),"integrity_check":integrity,"cohort_status_filter":cohort_status,
      "grain":{"fact_observation":"one row per source Observation","fact_medication_request":"one row per MedicationRequest",
               "mart_encounter_summary":"one row per Encounter","mart_patient_cohort":"one row per qualifying Patient"}}
    (output.parent/"warehouse_manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
    print(json.dumps(manifest,indent=2))
if __name__=="__main__":
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument("--input-dir",required=True); ap.add_argument("--output-db",required=True); ap.add_argument("--cohort-status",default="finished")
    a=ap.parse_args(); run(a.input_dir,a.output_db,a.cohort_status)
