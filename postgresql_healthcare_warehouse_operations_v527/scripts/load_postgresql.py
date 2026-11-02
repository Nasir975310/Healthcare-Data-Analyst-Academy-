#!/usr/bin/env python3
"""Load v5.25 FHIR ETL CSV outputs into PostgreSQL warehouse.

Requires PostgreSQL 15+ and psycopg 3. Uses one transaction per run.
The loader implements idempotent fact upserts and patient SCD Type 2 changes.
"""
import argparse,csv,hashlib,json,os
from datetime import date,datetime,timezone
from pathlib import Path
try:
    import psycopg
except ImportError:
    psycopg=None

def readcsv(p):
    with open(p,newline="",encoding="utf-8") as f:return list(csv.DictReader(f))
def as_date(v):
    if not v:return None
    return date.fromisoformat(v[:10])
def as_ts(v):
    if not v:return None
    return datetime.fromisoformat(v.replace("Z","+00:00"))
def row_hash(gender,birth):
    raw=json.dumps([gender,birth],separators=(",",":"),ensure_ascii=False)
    return hashlib.sha256(raw.encode()).hexdigest()
def load(conn,source_dir):
    src=Path(source_dir)
    required=["patients.csv","encounters.csv","observations.csv","medications.csv"]
    for n in required:
        if not (src/n).exists():raise FileNotFoundError(src/n)
    patients=readcsv(src/required[0]); encounters=readcsv(src/required[1])
    observations=readcsv(src/required[2]); medications=readcsv(src/required[3])
    stats={"patients_seen":len(patients),"patients_inserted":0,"patients_changed":0,
           "encounters_upserted":0,"observations_upserted":0,"medications_upserted":0}
    with conn.transaction():
      with conn.cursor() as cur:
        cur.execute("SET LOCAL search_path TO hda, public")
        now=datetime.now(timezone.utc)
        # SCD2 patient loader. New source snapshot changes close old row and insert new version.
        for p in patients:
          pid=p["patient_id"]; gender=p.get("gender") or None; birth=as_date(p.get("birth_date"))
          h=row_hash(gender,birth.isoformat() if birth else None)
          cur.execute("SELECT patient_key,version,row_hash FROM dim_patient WHERE patient_id=%s AND is_current FOR UPDATE",(pid,))
          old=cur.fetchone()
          if old is None:
            cur.execute("""INSERT INTO dim_patient(patient_id,gender,birth_date,valid_from,valid_to,is_current,version,row_hash)
              VALUES(%s,%s,%s,%s,NULL,true,1,%s)""",(pid,gender,birth,now,h))
            stats["patients_inserted"]+=1
          elif old[2]!=h:
            cur.execute("UPDATE dim_patient SET is_current=false,valid_to=%s WHERE patient_key=%s",(now,old[0]))
            cur.execute("""INSERT INTO dim_patient(patient_id,gender,birth_date,valid_from,valid_to,is_current,version,row_hash)
              VALUES(%s,%s,%s,%s,NULL,true,%s,%s)""",(pid,gender,birth,now,old[1]+1,h))
            stats["patients_changed"]+=1
        # Encounter dimension upsert.
        for e in encounters:
          cur.execute("""INSERT INTO dim_encounter(encounter_id,patient_id,status,class_code,start_datetime,end_datetime)
            VALUES(%s,%s,%s,%s,%s,%s)
            ON CONFLICT(encounter_id) DO UPDATE SET patient_id=EXCLUDED.patient_id,status=EXCLUDED.status,
              class_code=EXCLUDED.class_code,start_datetime=EXCLUDED.start_datetime,end_datetime=EXCLUDED.end_datetime""",
            (e["encounter_id"],e["patient_id"],e.get("status") or None,e.get("class_code") or None,
             as_ts(e.get("start")),as_ts(e.get("end"))))
          stats["encounters_upserted"]+=1
          if e.get("start"):
            d=as_date(e["start"]); k=int(d.strftime("%Y%m%d"))
            cur.execute("""INSERT INTO dim_date(date_key,full_date,year,month,day,quarter) VALUES(%s,%s,%s,%s,%s,%s)
              ON CONFLICT(date_key) DO NOTHING""",(k,d,d.year,d.month,d.day,(d.month-1)//3+1))
        # Resolve current patient and encounter keys for source-linked fact upserts.
        for o in observations:
          d=as_date(o.get("effective_datetime")); dk=int(d.strftime("%Y%m%d")) if d else None
          if d:cur.execute("""INSERT INTO dim_date(date_key,full_date,year,month,day,quarter) VALUES(%s,%s,%s,%s,%s,%s)
            ON CONFLICT(date_key) DO NOTHING""",(dk,d,d.year,d.month,d.day,(d.month-1)//3+1))
          system=o.get("source_system") or ""; code=o.get("source_code") or ""
          mapped=o.get("mapped_concept") or None
          cur.execute("""INSERT INTO dim_terminology(source_system,source_code,display,mapped_system,mapped_concept,mapping_status)
            VALUES(%s,%s,%s,%s,%s,%s) ON CONFLICT(source_system,source_code) DO UPDATE SET
            display=EXCLUDED.display,mapped_system=EXCLUDED.mapped_system,mapped_concept=EXCLUDED.mapped_concept,mapping_status=EXCLUDED.mapping_status""",
            (system,code,o.get("display"),o.get("mapped_system"),mapped,"mapped_illustrative" if mapped else "unmapped"))
          cur.execute("""INSERT INTO fact_observation(observation_id,patient_key,encounter_key,date_key,terminology_key,value_numeric,unit)
            SELECT %s,p.patient_key,e.encounter_key,%s,t.terminology_key,%s,%s
            FROM dim_patient p JOIN dim_encounter e ON e.encounter_id=%s
            JOIN dim_terminology t ON t.source_system=%s AND t.source_code=%s
            WHERE p.patient_id=%s AND p.is_current
            ON CONFLICT(observation_id) DO UPDATE SET patient_key=EXCLUDED.patient_key,encounter_key=EXCLUDED.encounter_key,
             date_key=EXCLUDED.date_key,terminology_key=EXCLUDED.terminology_key,value_numeric=EXCLUDED.value_numeric,unit=EXCLUDED.unit""",
            (o["observation_id"],dk,float(o["value"]) if o.get("value") else None,o.get("unit"),
             o.get("encounter_id"),system,code,o.get("patient_id")))
          stats["observations_upserted"]+=1
        for m in medications:
          d=as_date(m.get("authored_on")); dk=int(d.strftime("%Y%m%d")) if d else None
          if d:cur.execute("""INSERT INTO dim_date(date_key,full_date,year,month,day,quarter) VALUES(%s,%s,%s,%s,%s,%s)
            ON CONFLICT(date_key) DO NOTHING""",(dk,d,d.year,d.month,d.day,(d.month-1)//3+1))
          cur.execute("""INSERT INTO fact_medication_request(medication_request_id,patient_key,encounter_key,authored_date_key,status,medication_display,source_system,source_code)
            SELECT %s,p.patient_key,e.encounter_key,%s,%s,%s,%s,%s FROM dim_patient p JOIN dim_encounter e ON e.encounter_id=%s
            WHERE p.patient_id=%s AND p.is_current
            ON CONFLICT(medication_request_id) DO UPDATE SET patient_key=EXCLUDED.patient_key,encounter_key=EXCLUDED.encounter_key,
             authored_date_key=EXCLUDED.authored_date_key,status=EXCLUDED.status,medication_display=EXCLUDED.medication_display,
             source_system=EXCLUDED.source_system,source_code=EXCLUDED.source_code""",
            (m["medication_request_id"],dk,m.get("status"),m.get("medication_display"),m.get("source_system"),m.get("source_code"),
             m.get("encounter_id"),m.get("patient_id")))
          stats["medications_upserted"]+=1
        cur.execute("""INSERT INTO mart_encounter_summary(encounter_id,patient_id,encounter_date,encounter_status,
          observation_count,medication_request_count,distinct_observation_concepts,systolic_mean,diastolic_mean)
          SELECT e.encounter_id,e.patient_id,e.start_datetime::date,e.status,COALESCE(o.n,0),COALESCE(m.n,0),
           COALESCE(o.concepts,0),o.sbp,o.dbp
          FROM dim_encounter e
          LEFT JOIN (SELECT f.encounter_key,COUNT(*) n,COUNT(DISTINCT t.mapped_concept) concepts,
            AVG(f.value_numeric) FILTER(WHERE t.source_code='8480-6' AND f.unit='mmHg') sbp,
            AVG(f.value_numeric) FILTER(WHERE t.source_code='8462-4' AND f.unit='mmHg') dbp
            FROM fact_observation f JOIN dim_terminology t USING(terminology_key) GROUP BY f.encounter_key) o
            ON o.encounter_key=e.encounter_key
          LEFT JOIN (SELECT encounter_key,COUNT(*) n FROM fact_medication_request GROUP BY encounter_key) m
            ON m.encounter_key=e.encounter_key
          ON CONFLICT(encounter_id) DO UPDATE SET patient_id=EXCLUDED.patient_id,encounter_date=EXCLUDED.encounter_date,
            encounter_status=EXCLUDED.encounter_status,observation_count=EXCLUDED.observation_count,
            medication_request_count=EXCLUDED.medication_request_count,distinct_observation_concepts=EXCLUDED.distinct_observation_concepts,
            systolic_mean=EXCLUDED.systolic_mean,diastolic_mean=EXCLUDED.diastolic_mean,refreshed_at=now()""")
        cur.execute("""INSERT INTO mart_patient_cohort(patient_id,qualifying_encounters,first_qualifying_encounter,last_qualifying_encounter)
          SELECT patient_id,COUNT(*),MIN(encounter_date),MAX(encounter_date) FROM mart_encounter_summary
          WHERE encounter_status='finished' GROUP BY patient_id
          ON CONFLICT(patient_id) DO UPDATE SET qualifying_encounters=EXCLUDED.qualifying_encounters,
           first_qualifying_encounter=EXCLUDED.first_qualifying_encounter,last_qualifying_encounter=EXCLUDED.last_qualifying_encounter,refreshed_at=now()""")
        cur.execute("""DELETE FROM mart_patient_cohort c WHERE NOT EXISTS
          (SELECT 1 FROM mart_encounter_summary e WHERE e.patient_id=c.patient_id AND e.encounter_status='finished')""")
        cur.execute("SELECT COUNT(*) FROM dim_patient WHERE is_current");stats["current_patient_rows"]=cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM fact_observation");stats["observation_fact_rows"]=cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM fact_medication_request");stats["medication_fact_rows"]=cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM mart_encounter_summary");stats["encounter_mart_rows"]=cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM mart_patient_cohort");stats["cohort_mart_rows"]=cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM dim_patient WHERE is_current GROUP BY patient_id HAVING COUNT(*)>1")
        stats["duplicate_current_patient_groups"]=len(cur.fetchall())
    return stats
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument("--source-dir",required=True);ap.add_argument("--dsn",default=os.getenv("HDA_PG_DSN"));ap.add_argument("--dry-run",action="store_true")
    a=ap.parse_args()
    if not a.dsn:ap.error("Provide --dsn or set HDA_PG_DSN")
    if psycopg is None:raise SystemExit("Install dependencies: python -m pip install -r postgresql_healthcare_warehouse_operations_v527/requirements.txt")
    with psycopg.connect(a.dsn) as conn:
      if a.dry_run:
        print("Connection successful. Dry run: no data changes requested.")
      else: print(json.dumps(load(conn,a.source_dir),indent=2))
if __name__=="__main__":main()
