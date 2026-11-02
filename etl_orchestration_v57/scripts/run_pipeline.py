#!/usr/bin/env python3
"""Reproducible CSV -> validation/quarantine -> SQLite staging/curated ETL."""
from __future__ import annotations
import argparse, csv, hashlib, json, logging, sqlite3
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd

def sha(p):
    h=hashlib.sha256()
    with Path(p).open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",required=True);ap.add_argument("--config",required=True)
    ap.add_argument("--output-dir",default="output");ap.add_argument("--run-id",default="")
    a=ap.parse_args();src=Path(a.input).resolve();cfgp=Path(a.config).resolve();out=Path(a.output_dir).resolve()
    out.mkdir(parents=True,exist_ok=True);(out/"quarantine").mkdir(exist_ok=True)
    runid=a.run_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    logging.basicConfig(filename=out/"pipeline.log",level=logging.INFO,format="%(asctime)s %(levelname)s %(message)s")
    log=logging.getLogger("healthcare_etl");started=datetime.now(timezone.utc).isoformat()
    cfg=json.loads(cfgp.read_text());df=pd.read_csv(src,dtype=str,keep_default_na=False)
    source_hash=sha(src);expected=cfg["required"];actual=list(df.columns)
    missing_cols=[c for c in expected if c not in actual];added_cols=[c for c in actual if c not in expected]
    if missing_cols and cfg.get("schema_policy","warn")=="fail":raise ValueError(f"Missing schema columns: {missing_cols}")
    df["_source_row"]=range(2,len(df)+2);df["_run_id"]=runid
    reasons=[[] for _ in range(len(df))]
    def flag(mask,msg):
        for i,b in enumerate(mask):
            if bool(b):reasons[i].append(msg)
    for c in expected:
        if c not in df.columns:
            for x in reasons:x.append(f"missing_column:{c}")
    key=cfg["primary_key"]
    if key in df:
        s=df[key].astype(str).str.strip()
        flag(s.eq(""),f"blank_primary_key:{key}")
        flag(s.duplicated(keep="first"),f"duplicate_primary_key:{key}")
    for c in cfg.get("date_fields",[]):
        if c in df:flag(pd.to_datetime(df[c],errors="coerce").isna(),f"invalid_date:{c}")
    for c,rule in cfg.get("numeric_rules",{}).items():
        if c in df:
            n=pd.to_numeric(df[c],errors="coerce")
            flag(n.isna(),f"invalid_numeric:{c}")
            if "min" in rule:flag(n.notna()&(n<float(rule["min"])),f"below_minimum:{c}")
            if "max" in rule:flag(n.notna()&(n>float(rule["max"])),f"above_maximum:{c}")
    for c,allowed in cfg.get("allowed_values",{}).items():
        if c in df:flag(~df[c].isin(allowed),f"invalid_category:{c}")
    rejected=[i for i,x in enumerate(reasons) if x];accepted=[i for i,x in enumerate(reasons) if not x]
    q=df.iloc[rejected].copy()
    q["rejection_reasons"]=[";".join(reasons[i]) for i in rejected]
    accepted_df=df.iloc[accepted].copy()
    q.to_csv(out/"quarantine"/f"quarantine_{runid}.csv",index=False)
    # CSV output removes internal source metadata only from curated output? preserve run and row lineage.
    db=out/"healthcare_analytics.sqlite"
    with sqlite3.connect(db) as con:
        con.execute("""CREATE TABLE IF NOT EXISTS staging_encounters (
          encounter_id TEXT, patient_id TEXT, admit_date TEXT, department TEXT,
          los_days TEXT, order_count TEXT, sbp TEXT, disposition TEXT,
          _source_row INTEGER, _run_id TEXT)""")
        con.execute("""CREATE TABLE IF NOT EXISTS curated_encounters (
          encounter_id TEXT PRIMARY KEY, patient_id TEXT, admit_date TEXT, department TEXT,
          los_days REAL, order_count INTEGER, sbp REAL, disposition TEXT,
          _source_row INTEGER, _run_id TEXT)""")
        con.execute("""CREATE TABLE IF NOT EXISTS pipeline_runs (
          run_id TEXT PRIMARY KEY, started_utc TEXT, completed_utc TEXT, source_file TEXT,
          source_sha256 TEXT, raw_rows INTEGER, accepted_rows INTEGER, rejected_rows INTEGER,
          schema_missing TEXT, schema_added TEXT)""")
        con.execute("DELETE FROM staging_encounters WHERE _run_id=?",(runid,))
        for _,r in df.iterrows():
            con.execute("INSERT INTO staging_encounters VALUES (?,?,?,?,?,?,?,?,?,?)",
                tuple(str(r.get(c,"")) for c in expected)+ (int(r["_source_row"]),runid))
        # Incremental upsert: reprocessing same key refreshes curated values and provenance.
        for _,r in accepted_df.iterrows():
            vals=[str(r.get("encounter_id","")),str(r.get("patient_id","")),str(r.get("admit_date","")),
                  str(r.get("department","")),float(r["los_days"]),int(float(r["order_count"])),
                  float(r["sbp"]),str(r.get("disposition","")),int(r["_source_row"]),runid]
            con.execute("""INSERT INTO curated_encounters VALUES (?,?,?,?,?,?,?,?,?,?)
              ON CONFLICT(encounter_id) DO UPDATE SET patient_id=excluded.patient_id,
              admit_date=excluded.admit_date,department=excluded.department,los_days=excluded.los_days,
              order_count=excluded.order_count,sbp=excluded.sbp,disposition=excluded.disposition,
              _source_row=excluded._source_row,_run_id=excluded._run_id""",vals)
        completed=datetime.now(timezone.utc).isoformat()
        con.execute("INSERT OR REPLACE INTO pipeline_runs VALUES (?,?,?,?,?,?,?,?,?,?)",
            (runid,started,completed,src.name,source_hash,len(df),len(accepted),len(rejected),
             json.dumps(missing_cols),json.dumps(added_cols)))
        stage_count=con.execute("SELECT COUNT(*) FROM staging_encounters WHERE _run_id=?",(runid,)).fetchone()[0]
        curated_keys=con.execute("SELECT COUNT(DISTINCT encounter_id) FROM curated_encounters").fetchone()[0]
    summary={"run_id":runid,"source_file":src.name,"source_sha256":source_hash,"rows_raw":len(df),
      "rows_accepted":len(accepted),"rows_rejected":len(rejected),"staging_rows_for_run":stage_count,
      "curated_unique_encounters_total":curated_keys,"schema_missing_columns":missing_cols,"schema_added_columns":added_cols,
      "reconciliation":{"raw_equals_accepted_plus_rejected":len(df)==len(accepted)+len(rejected),
                        "staging_equals_raw":stage_count==len(df)},
      "database":str(db),"quarantine_file":str(out/"quarantine"/f"quarantine_{runid}.csv")}
    (out/f"run_summary_{runid}.json").write_text(json.dumps(summary,indent=2))
    log.info("run=%s raw=%d accepted=%d rejected=%d",runid,len(df),len(accepted),len(rejected))
    # Current-run manifest with hashes for inspectable outputs.
    manifest={"run_id":runid,"source_sha256":source_hash,"config_sha256":sha(cfgp),"outputs":{}}
    for p in [out/f"run_summary_{runid}.json",out/"quarantine"/f"quarantine_{runid}.csv",db]:
        manifest["outputs"][str(p.relative_to(out))]={"sha256":sha(p),"bytes":p.stat().st_size}
    (out/f"audit_manifest_{runid}.json").write_text(json.dumps(manifest,indent=2))
    print(json.dumps(summary,indent=2))
if __name__=="__main__":main()
