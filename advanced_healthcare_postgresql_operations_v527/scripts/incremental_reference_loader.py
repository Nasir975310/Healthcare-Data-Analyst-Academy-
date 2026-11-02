#!/usr/bin/env python3
"""Build and validate a local reference warehouse with incremental loads and SCD2."""
import argparse,csv,hashlib,json,sqlite3
from pathlib import Path
from datetime import date

def readcsv(p):
    with open(p,newline="",encoding="utf-8") as f:return list(csv.DictReader(f))
def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def create(db):
    db.executescript("""
    PRAGMA foreign_keys=ON;
    CREATE TABLE IF NOT EXISTS dim_patient_scd2(
      patient_key INTEGER PRIMARY KEY AUTOINCREMENT, patient_id TEXT NOT NULL,
      gender TEXT, birth_date TEXT, record_hash TEXT NOT NULL,
      valid_from TEXT NOT NULL, valid_to TEXT, is_current INTEGER NOT NULL CHECK(is_current IN(0,1)),
      UNIQUE(patient_id,valid_from));
    CREATE UNIQUE INDEX IF NOT EXISTS ux_patient_current ON dim_patient_scd2(patient_id) WHERE is_current=1;
    CREATE TABLE IF NOT EXISTS dim_encounter(encounter_id TEXT PRIMARY KEY,patient_id TEXT NOT NULL,status TEXT,
      class_code TEXT,start_datetime TEXT,end_datetime TEXT);
    CREATE TABLE IF NOT EXISTS fact_observation(observation_id TEXT PRIMARY KEY,patient_id TEXT NOT NULL,encounter_id TEXT NOT NULL,
      effective_datetime TEXT,source_code TEXT,value_numeric REAL,unit TEXT);
    CREATE TABLE IF NOT EXISTS fact_medication_request(medication_request_id TEXT PRIMARY KEY,patient_id TEXT NOT NULL,
      encounter_id TEXT NOT NULL,authored_on TEXT,status TEXT,medication_display TEXT);
    CREATE TABLE IF NOT EXISTS etl_batch(batch_id TEXT PRIMARY KEY,started_at TEXT NOT NULL,completed_at TEXT,
      source_hash TEXT NOT NULL,status TEXT NOT NULL,patients_inserted INTEGER DEFAULT 0,
      patients_changed INTEGER DEFAULT 0,encounters_upserted INTEGER DEFAULT 0,
      observations_inserted INTEGER DEFAULT 0,medications_inserted INTEGER DEFAULT 0,
      error_message TEXT);
    """)
def patient_hash(p):
    raw="|".join(str(p.get(k) or "") for k in ("gender","birth_date"))
    return hashlib.sha256(raw.encode()).hexdigest()
def upsert_patient(db,p,as_of):
    h=patient_hash(p); cur=db.execute("SELECT patient_key,record_hash,valid_from FROM dim_patient_scd2 WHERE patient_id=? AND is_current=1",(p["patient_id"],)).fetchone()
    if cur is None:
        db.execute("""INSERT INTO dim_patient_scd2(patient_id,gender,birth_date,record_hash,valid_from,valid_to,is_current)
          VALUES(?,?,?,?,?,NULL,1)""",(p["patient_id"],p.get("gender"),p.get("birth_date"),h,as_of))
        return "inserted"
    if cur[1]==h:return "unchanged"
    if as_of<=cur[2]: raise ValueError(f"SCD2 effective date {as_of} must be after current version {cur[2]}")
    db.execute("UPDATE dim_patient_scd2 SET valid_to=?,is_current=0 WHERE patient_key=?",(as_of,cur[0]))
    db.execute("""INSERT INTO dim_patient_scd2(patient_id,gender,birth_date,record_hash,valid_from,valid_to,is_current)
      VALUES(?,?,?,?,?,NULL,1)""",(p["patient_id"],p.get("gender"),p.get("birth_date"),h,as_of))
    return "changed"
def load(input_dir,db_path,as_of,batch_id):
    src=Path(input_dir); out=Path(db_path); out.parent.mkdir(parents=True,exist_ok=True)
    required=["patients.csv","encounters.csv","observations.csv","medications.csv"]
    for n in required:
        if not (src/n).exists():raise FileNotFoundError(src/n)
    source_hash=hashlib.sha256("".join(digest(src/n) for n in required).encode()).hexdigest()
    patients=readcsv(src/"patients.csv"); encounters=readcsv(src/"encounters.csv")
    observations=readcsv(src/"observations.csv"); meds=readcsv(src/"medications.csv")
    db=sqlite3.connect(out); create(db)
    db.execute("INSERT INTO etl_batch(batch_id,started_at,source_hash,status) VALUES(?,?,?,'running')",(batch_id,as_of,source_hash))
    counts={"patients_inserted":0,"patients_changed":0,"encounters_upserted":0,"observations_inserted":0,"medications_inserted":0}
    try:
        for p in patients:
            result=upsert_patient(db,p,as_of)
            if result=="inserted":counts["patients_inserted"]+=1
            elif result=="changed":counts["patients_changed"]+=1
        for e in encounters:
            db.execute("""INSERT INTO dim_encounter VALUES(?,?,?,?,?,?)
              ON CONFLICT(encounter_id) DO UPDATE SET patient_id=excluded.patient_id,status=excluded.status,
              class_code=excluded.class_code,start_datetime=excluded.start_datetime,end_datetime=excluded.end_datetime""",
              (e["encounter_id"],e["patient_id"],e.get("status"),e.get("class_code"),e.get("start"),e.get("end")))
            counts["encounters_upserted"]+=1
        before=db.execute("SELECT COUNT(*) FROM fact_observation").fetchone()[0]
        for o in observations:
            db.execute("""INSERT OR IGNORE INTO fact_observation VALUES(?,?,?,?,?,?,?)""",
              (o["observation_id"],o["patient_id"],o["encounter_id"],o.get("effective_datetime"),o.get("source_code"),
               float(o["value"]) if o.get("value") not in ("",None) else None,o.get("unit")))
        counts["observations_inserted"]=db.execute("SELECT COUNT(*) FROM fact_observation").fetchone()[0]-before
        before=db.execute("SELECT COUNT(*) FROM fact_medication_request").fetchone()[0]
        for m in meds:
            db.execute("INSERT OR IGNORE INTO fact_medication_request VALUES(?,?,?,?,?,?)",
              (m["medication_request_id"],m["patient_id"],m["encounter_id"],m.get("authored_on"),m.get("status"),m.get("medication_display")))
        counts["medications_inserted"]=db.execute("SELECT COUNT(*) FROM fact_medication_request").fetchone()[0]-before
        db.execute("""UPDATE etl_batch SET completed_at=?,status='success',patients_inserted=?,patients_changed=?,
          encounters_upserted=?,observations_inserted=?,medications_inserted=? WHERE batch_id=?""",
          (as_of,*counts.values(),batch_id))
        db.commit()
    except Exception as e:
        db.rollback()
        db.execute("UPDATE etl_batch SET completed_at=?,status='failed',error_message=? WHERE batch_id=?",(as_of,str(e),batch_id))
        db.commit(); db.close(); raise
    results={
      "patients_current":db.execute("SELECT COUNT(*) FROM dim_patient_scd2 WHERE is_current=1").fetchone()[0],
      "patients_versions":db.execute("SELECT COUNT(*) FROM dim_patient_scd2").fetchone()[0],
      "encounters":db.execute("SELECT COUNT(*) FROM dim_encounter").fetchone()[0],
      "observations":db.execute("SELECT COUNT(*) FROM fact_observation").fetchone()[0],
      "medications":db.execute("SELECT COUNT(*) FROM fact_medication_request").fetchone()[0],
      "batches":db.execute("SELECT COUNT(*) FROM etl_batch").fetchone()[0]}
    fk=db.execute("PRAGMA foreign_key_check").fetchall(); integrity=db.execute("PRAGMA integrity_check").fetchone()[0]
    db.close()
    return {"batch_id":batch_id,"as_of":as_of,"source_hash":source_hash,"counts":counts,"warehouse_counts":results,
      "foreign_key_violations":len(fk),"integrity_check":integrity}
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--input-dir",required=True);p.add_argument("--database",required=True)
    p.add_argument("--as-of",required=True,help="Effective load date YYYY-MM-DD");p.add_argument("--batch-id",required=True)
    a=p.parse_args();r=load(a.input_dir,a.database,a.as_of,a.batch_id)
    out=Path(a.database).parent/"incremental_load_report.json";out.write_text(json.dumps(r,indent=2),encoding="utf-8")
    print(json.dumps(r,indent=2))
if __name__=="__main__":main()
