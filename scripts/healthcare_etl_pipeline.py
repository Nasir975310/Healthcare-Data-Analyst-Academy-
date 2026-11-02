#!/usr/bin/env python3
"""Reproducible synthetic healthcare ETL training pipeline.

Extract -> validate -> transform -> load -> audit.
This is a local educational pipeline, not a production clinical system.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, logging, sqlite3, sys
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "assignments" / "data"
DEFAULT_API = ROOT / "etl" / "mock_api"
DEFAULT_DB = ROOT / "assignments" / "outputs" / "healthcare_etl_training.db"
DEFAULT_OUT = ROOT / "assignments" / "outputs" / "etl_runs"

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def read_csv_source(data_dir: Path):
    e=pd.read_csv(data_dir/"synthetic_encounters.csv",dtype={"encounter_id":"string","patient_id":"string"})
    o=pd.read_csv(data_dir/"synthetic_medication_orders.csv",dtype={"order_id":"string","encounter_id":"string"})
    return e,o

def read_mock_api(api_dir: Path):
    def pages(resource):
        paths=sorted(api_dir.glob(f"{resource.lower()}_page_*.json"))
        if not paths: raise FileNotFoundError(f"No {resource} API fixture pages found in {api_dir}")
        rows=[]; expected_total=None
        for expected_page,path in enumerate(paths,1):
            payload=json.loads(path.read_text(encoding="utf-8"))
            if payload.get("resource")!=resource: raise ValueError(f"Unexpected resource in {path}")
            if payload.get("page")!=expected_page: raise ValueError(f"Missing/out-of-order {resource} page {expected_page}")
            if expected_total is None: expected_total=payload.get("total_records")
            if payload.get("total_records")!=expected_total: raise ValueError(f"Changing total_records in {path}")
            rows.extend(payload.get("results",[]))
        if len(rows)!=expected_total: raise ValueError(f"{resource} pagination incomplete: {len(rows)} != {expected_total}")
        return pd.DataFrame(rows)
    return pages("Encounter"),pages("MedicationOrder")

def normalise(enc,orders):
    e=enc.copy(); o=orders.copy()
    for col in ["encounter_id","patient_id","department","payer_type","discharge_disposition"]:
        if col in e: e[col]=e[col].astype("string").str.strip()
    for col in ["order_id","encounter_id","drug_name","therapeutic_class","route","order_status"]:
        if col in o: o[col]=o[col].astype("string").str.strip()
    if "drug_name" in o: o["drug_name"]=o["drug_name"].str.replace(r"\s+"," ",regex=True)
    if "order_status" in o: o["order_status"]=o["order_status"].str.upper()
    for col in ["admission_date","discharge_date"]:
        e[col]=pd.to_datetime(e[col],errors="coerce").dt.strftime("%Y-%m-%d")
    o["order_date"]=pd.to_datetime(o["order_date"],errors="coerce").dt.strftime("%Y-%m-%d")
    cost_available="unit_cost_inr" in o.columns
    if "unit_cost_inr" not in o: o["unit_cost_inr"]=pd.NA
    o["unit_cost_source_available"]=cost_available
    if "prescriber_id" not in o: o["prescriber_id"]=pd.NA
    if "pharmacy_location" not in o: o["pharmacy_location"]=pd.NA
    for col in ["age_years","length_of_stay_days","readmission_30d_flag"]:
        e[col]=pd.to_numeric(e[col],errors="coerce")
    for col in ["quantity","unit_cost_inr"]:
        o[col]=pd.to_numeric(o[col],errors="coerce")
    return e,o

def validate(e,o):
    issues=[]
    def issue(dataset,field,rule,severity,count,detail):
        issues.append({"dataset":dataset,"field":field,"rule":rule,"severity":severity,"count":int(count),"detail":detail})
    issue("encounters","encounter_id","required_key","ERROR",e["encounter_id"].isna().sum()+e["encounter_id"].astype("string").str.strip().eq("").sum(),"Encounter key must be present.")
    issue("encounters","encounter_id","unique_key","ERROR",e["encounter_id"].duplicated().sum(),"Encounter key must be unique.")
    issue("encounters","admission_date","valid_date","ERROR",e["admission_date"].isna().sum(),"Admission date must parse.")
    issue("orders","order_id","required_key","ERROR",o["order_id"].isna().sum()+o["order_id"].astype("string").str.strip().eq("").sum(),"Order key must be present.")
    issue("orders","order_id","unique_key","ERROR",o["order_id"].duplicated().sum(),"Order key must be unique.")
    issue("orders","order_date","valid_date","ERROR",o["order_date"].isna().sum(),"Order date must parse.")
    issue("orders","quantity","positive_quantity","ERROR",(o["quantity"].isna()|(o["quantity"]<=0)).sum(),"Quantity must be present and > 0.")
    issue("orders","encounter_id","orphan_reference","WARNING",(~o["encounter_id"].isin(e["encounter_id"])).sum(),"Order references an encounter key not present in the encounter extract.")
    if bool(o["unit_cost_source_available"].any()):
        issue("orders","unit_cost_inr","missing_cost","WARNING",o["unit_cost_inr"].isna().sum(),"Cost missing; monetary total cannot be calculated for this row.")
    else:
        issue("orders","unit_cost_inr","source_field_not_supplied","INFO",1,"Source extract does not include unit_cost_inr; monetary value is not calculated.")
    issue("orders","therapeutic_class","missing_class","WARNING",o["therapeutic_class"].isna().sum()+o["therapeutic_class"].astype("string").str.strip().eq("").sum(),"Therapeutic class missing; do not infer without a reference mapping.")
    return issues

def setup_db(db: Path):
    db.parent.mkdir(parents=True,exist_ok=True)
    con=sqlite3.connect(db)
    con.executescript("""
    PRAGMA foreign_keys=ON;
    CREATE TABLE IF NOT EXISTS raw_encounters(
      encounter_id TEXT PRIMARY KEY, payload_json TEXT NOT NULL, ingested_at TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS raw_medication_orders(
      order_id TEXT PRIMARY KEY, payload_json TEXT NOT NULL, ingested_at TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS mart_encounters(
      encounter_id TEXT PRIMARY KEY, patient_id TEXT, admission_date TEXT, discharge_date TEXT,
      age_years REAL, department TEXT, payer_type TEXT, length_of_stay_days REAL,
      discharge_disposition TEXT, readmission_30d_flag REAL);
    CREATE TABLE IF NOT EXISTS mart_medication_orders(
      order_id TEXT PRIMARY KEY, encounter_id TEXT, order_date TEXT, drug_name TEXT,
      therapeutic_class TEXT, route TEXT, order_status TEXT, quantity REAL,
      unit_cost_inr REAL, line_total_inr REAL);
    CREATE TABLE IF NOT EXISTS quarantine_orders(
      order_id TEXT PRIMARY KEY, encounter_id TEXT, reason TEXT, payload_json TEXT, run_id TEXT);
    CREATE TABLE IF NOT EXISTS data_quality_results(
      run_id TEXT, dataset TEXT, field TEXT, rule TEXT, severity TEXT, issue_count INTEGER, detail TEXT);
    CREATE TABLE IF NOT EXISTS etl_run_log(
      run_id TEXT PRIMARY KEY, started_at TEXT, finished_at TEXT, source_mode TEXT,
      encounter_rows INTEGER, order_rows INTEGER, loaded_encounters INTEGER,
      loaded_orders INTEGER, quarantined_orders INTEGER, status TEXT, message TEXT);
    """)
    return con

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source",choices=["csv","mock-api"],default="csv")
    ap.add_argument("--data-dir",type=Path,default=DEFAULT_DATA)
    ap.add_argument("--api-dir",type=Path,default=DEFAULT_API)
    ap.add_argument("--db",type=Path,default=DEFAULT_DB)
    ap.add_argument("--output-dir",type=Path,default=DEFAULT_OUT)
    ap.add_argument("--fail-on-errors",action="store_true")
    args=ap.parse_args()
    args.output_dir.mkdir(parents=True,exist_ok=True)
    run_id=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    log_path=args.output_dir/f"etl_{run_id}.log"
    logging.basicConfig(level=logging.INFO,format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.FileHandler(log_path),logging.StreamHandler(sys.stdout)])
    started=datetime.now(timezone.utc).isoformat()
    try:
        logging.info("ETL run %s started; source=%s",run_id,args.source)
        if args.source=="csv":
            e_raw,o_raw=read_csv_source(args.data_dir)
            source_files=[args.data_dir/"synthetic_encounters.csv",args.data_dir/"synthetic_medication_orders.csv"]
        else:
            e_raw,o_raw=read_mock_api(args.api_dir)
            source_files=sorted(args.api_dir.glob("*.json"))
        e,o=normalise(e_raw,o_raw)
        issues=validate(e,o)
        for x in issues:
            if x["count"]: logging.warning("%s.%s %s: %s (%s)",x["dataset"],x["field"],x["rule"],x["count"],x["severity"])
        error_count=sum(x["count"] for x in issues if x["severity"]=="ERROR")
        if args.fail_on_errors and error_count:
            raise ValueError(f"Validation failed with {error_count} error(s)")
        valid_enc=e[e["encounter_id"].notna() & ~e["encounter_id"].duplicated() & e["admission_date"].notna()].copy()
        valid_orders=o[o["order_id"].notna() & ~o["order_id"].duplicated() & o["order_date"].notna() & o["quantity"].notna() & (o["quantity"]>0)].copy()
        known=set(valid_enc["encounter_id"])
        valid_orders["orphan_reference"]=~valid_orders["encounter_id"].isin(known)
        quarantine=valid_orders[valid_orders["orphan_reference"]].copy()
        curated=valid_orders[~valid_orders["orphan_reference"]].copy()
        curated["line_total_inr"]=curated["quantity"]*pd.to_numeric(curated["unit_cost_inr"],errors="coerce")
        stamp=datetime.now(timezone.utc).isoformat()
        con=setup_db(args.db)
        try:
            with con:
                for _,r in e_raw.iterrows():
                    key=str(r.get("encounter_id",""))
                    payload=json.dumps({k:(None if pd.isna(v) else str(v)) for k,v in r.items()},allow_nan=False)
                    con.execute("INSERT OR REPLACE INTO raw_encounters VALUES(?,?,?)",(key,payload,stamp))
                for _,r in o_raw.iterrows():
                    key=str(r.get("order_id",""))
                    payload=json.dumps({k:(None if pd.isna(v) else str(v)) for k,v in r.items()},allow_nan=False)
                    con.execute("INSERT OR REPLACE INTO raw_medication_orders VALUES(?,?,?)",(key,payload,stamp))
                for _,r in valid_enc.iterrows():
                    con.execute("INSERT OR REPLACE INTO mart_encounters VALUES(?,?,?,?,?,?,?,?,?,?)",tuple(
                        None if pd.isna(r.get(k)) else r.get(k) for k in
                        ["encounter_id","patient_id","admission_date","discharge_date","age_years","department","payer_type","length_of_stay_days","discharge_disposition","readmission_30d_flag"]))
                for _,r in curated.iterrows():
                    con.execute("INSERT OR REPLACE INTO mart_medication_orders VALUES(?,?,?,?,?,?,?,?,?,?)",tuple(
                        None if pd.isna(r.get(k)) else r.get(k) for k in
                        ["order_id","encounter_id","order_date","drug_name","therapeutic_class","route","order_status","quantity","unit_cost_inr","line_total_inr"]))
                for _,r in quarantine.iterrows():
                    reason="orphan_encounter_reference"
                    payload=json.dumps({k:(None if pd.isna(v) else str(v)) for k,v in r.items()},allow_nan=False)
                    con.execute("INSERT OR REPLACE INTO quarantine_orders VALUES(?,?,?,?,?)",(str(r["order_id"]),str(r["encounter_id"]),reason,payload,run_id))
                con.executemany("INSERT INTO data_quality_results VALUES(?,?,?,?,?,?,?)",
                    [(run_id,x["dataset"],x["field"],x["rule"],x["severity"],x["count"],x["detail"]) for x in issues])
                con.execute("INSERT INTO etl_run_log VALUES(?,?,?,?,?,?,?,?,?,?,?)",(
                    run_id,started,datetime.now(timezone.utc).isoformat(),args.source,len(e_raw),len(o_raw),
                    len(valid_enc),len(curated),len(quarantine),"SUCCESS","Validation warnings may be present; inspect quality report."))
        finally: con.close()
        manifest={"run_id":run_id,"source":args.source,"started_at":started,"finished_at":datetime.now(timezone.utc).isoformat(),
          "source_files":[{"path":str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else p.name,"sha256":sha256(p)} for p in source_files],
          "row_counts":{"encounters_source":len(e_raw),"orders_source":len(o_raw),"encounters_loaded":len(valid_enc),
            "orders_loaded":len(curated),"orders_quarantined":len(quarantine)},
          "quality_results":issues,"database":str(args.db.relative_to(ROOT)) if args.db.is_relative_to(ROOT) else args.db.name}
        (args.output_dir/f"manifest_{run_id}.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
        (args.output_dir/f"quality_{run_id}.csv").write_text(
            "dataset,field,rule,severity,count,detail\n"+ "".join(
            ",".join('"'+str(x[k]).replace('"','""')+'"' for k in ["dataset","field","rule","severity","count","detail"])+"\n" for x in issues),encoding="utf-8")
        logging.info("Loaded encounters=%s orders=%s quarantined=%s",len(valid_enc),len(curated),len(quarantine))
        logging.info("Manifest: %s",args.output_dir/f"manifest_{run_id}.json")
        logging.info("ETL completed successfully.")
        return 0
    except Exception as ex:
        logging.exception("ETL failed: %s",ex)
        try:
            con=setup_db(args.db)
            with con: con.execute("INSERT OR REPLACE INTO etl_run_log VALUES(?,?,?,?,?,?,?,?,?,?,?)",(
                run_id,started,datetime.now(timezone.utc).isoformat(),args.source,0,0,0,0,0,"FAILED",str(ex)))
            con.close()
        except Exception: pass
        return 1

if __name__=="__main__": raise SystemExit(main())
