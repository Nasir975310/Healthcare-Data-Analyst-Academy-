#!/usr/bin/env python3
"""Small, auditable synthetic healthcare data pipeline; stdlib only."""
from pathlib import Path
import argparse, csv, hashlib, json, sqlite3, datetime as dt, html, platform, sys
ROOT=Path(__file__).resolve().parents[1]
def sha256(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(65536),b""): h.update(chunk)
    return h.hexdigest()
def run(input_path, output_dir):
    cfg=json.loads((ROOT/"config/pipeline.json").read_text())
    output_dir.mkdir(parents=True,exist_ok=True)
    quarantine=output_dir/"quarantine.csv"
    accepted=[]; rejected=[]; seen=set()
    with input_path.open(newline="",encoding="utf-8-sig") as f:
        reader=csv.DictReader(f)
        missing=[c for c in cfg["required_columns"] if c not in (reader.fieldnames or [])]
        if missing: raise ValueError("Missing required columns: "+", ".join(missing))
        for line,row in enumerate(reader,2):
            errors=[]
            eid=(row.get("encounter_id") or "").strip()
            if not eid: errors.append("missing_encounter_id")
            elif eid in seen: errors.append("duplicate_encounter_id")
            seen.add(eid)
            try: dt.date.fromisoformat(row["encounter_date"])
            except Exception: errors.append("invalid_encounter_date")
            try:
                los=int(row["los_days"])
                if los<0: errors.append("negative_los")
            except Exception: errors.append("invalid_los")
            try:
                charge=float(row["charge_inr"])
                if charge<0: errors.append("negative_charge")
            except Exception: errors.append("invalid_charge")
            if row["encounter_type"] not in cfg["allowed_encounter_types"]: errors.append("unknown_encounter_type")
            for c in ("patient_id","department_id","discharge_status"):
                if not (row.get(c) or "").strip(): errors.append("missing_"+c)
            if errors: rejected.append({"source_line":line,"encounter_id":eid,"errors":";".join(errors),"raw":row})
            else:
                row["los_days"]=los; row["charge_inr"]=charge
                row["department_name"]=row["department_id"]
                accepted.append(row)
    qpath=quarantine
    with qpath.open("w",newline="",encoding="utf-8") as f:
        fields=["source_line","encounter_id","errors","raw"]
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
        for r in rejected: w.writerow(r)
    dbpath=output_dir/"curated_warehouse.sqlite"
    con=sqlite3.connect(dbpath)
    try:
        con.executescript((ROOT/"sql/warehouse_schema.sql").read_text())
        now=dt.datetime.now(dt.timezone.utc).isoformat()
        digest=sha256(input_path)
        for r in accepted:
            con.execute("INSERT OR REPLACE INTO dim_department VALUES(?,?)",(r["department_id"],r["department_name"]))
            con.execute("""INSERT OR REPLACE INTO fact_encounter VALUES(?,?,?,?,?,?,?,?,?,?)""",
             (r["encounter_id"],r["patient_id"],r["department_id"],r["encounter_date"],r["encounter_type"],
              r["discharge_status"],r["los_days"],r["charge_inr"],digest,now))
        con.commit()
        loaded=con.execute("SELECT COUNT(*) FROM fact_encounter").fetchone()[0]
        distinct=con.execute("SELECT COUNT(DISTINCT patient_id) FROM fact_encounter").fetchone()[0]
        charges=con.execute("SELECT COALESCE(SUM(charge_inr),0) FROM fact_encounter").fetchone()[0]
        by_type=con.execute("SELECT encounter_type,COUNT(*) FROM fact_encounter GROUP BY encounter_type").fetchall()
    finally: con.close()
    manifest={"pipeline":cfg["pipeline_name"],"schema_version":cfg["schema_version"],
      "run_timestamp_utc":now,"input_file":input_path.name,"input_sha256":digest,
      "rows_read":len(accepted)+len(rejected),"accepted_this_run":len(accepted),
      "quarantined_this_run":len(rejected),"warehouse_rows_after_run":loaded,
      "unique_patients_after_run":distinct,"charges_inr_after_run":round(charges,2),
      "counts_by_encounter_type":dict(by_type),"python":platform.python_version(),
      "platform":platform.platform(),"status":"PASS" if not rejected else "PASS_WITH_QUARANTINE"}
    mpath=output_dir/"run_manifest.json"; mpath.write_text(json.dumps(manifest,indent=2),encoding="utf-8")
    rows=[f"<tr><td>{html.escape(k)}</td><td>{html.escape(str(v))}</td></tr>" for k,v in manifest.items()]
    report="<html><head><meta charset='utf-8'><title>Pipeline quality report</title></head><body><h1>Pipeline run report</h1><p>Reference synthetic dataset only.</p><table>"+ "".join(rows)+"</table></body></html>"
    (output_dir/"quality_report.html").write_text(report,encoding="utf-8")
    return manifest
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",type=Path,default=ROOT/"data/inbound/encounters.csv")
    ap.add_argument("--output-dir",type=Path,default=ROOT/"output")
    a=ap.parse_args()
    result=run(a.input,a.output_dir)
    print(json.dumps(result,indent=2))
    return 0
if __name__=="__main__": sys.exit(main())
