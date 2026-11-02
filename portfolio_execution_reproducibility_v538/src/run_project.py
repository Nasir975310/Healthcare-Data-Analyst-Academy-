#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, hashlib, json, sqlite3
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

REQUIRED = {"encounter_id","patient_id","department","encounter_date","status","wait_minutes","source_system"}

def load_rows(path):
    with Path(path).open(newline="",encoding="utf-8-sig") as f:
        reader=csv.DictReader(f)
        if not reader.fieldnames or not REQUIRED.issubset(reader.fieldnames):
            raise ValueError(f"Input must contain columns: {sorted(REQUIRED)}")
        return list(reader)

def analyse(rows):
    raw_count=len(rows); seen=set(); unique=[]; duplicate_ids=[]
    for row in rows:
        key=row["encounter_id"].strip()
        if key in seen:
            duplicate_ids.append(key); continue
        seen.add(key); unique.append(row)
    statuses=Counter((r["status"] or "").strip().lower() for r in unique)
    exceptions=[]; eligible_volume=[]; eligible_wait=[]
    for r in unique:
        eid=r["encounter_id"]; dept=(r["department"] or "").strip()
        dt=(r["encounter_date"] or "").strip(); status=(r["status"] or "").strip().lower()
        wait=(r["wait_minutes"] or "").strip(); problems=[]
        if not dept: problems.append("missing_department")
        if not dt: problems.append("missing_encounter_date")
        else:
            try: date.fromisoformat(dt)
            except ValueError: problems.append("invalid_encounter_date")
        if wait:
            try:
                if float(wait)<0: problems.append("negative_wait")
            except ValueError: problems.append("non_numeric_wait")
        if problems: exceptions.append({"encounter_id":eid,"issues":problems})
        if status=="completed" and dept and dt:
            try: date.fromisoformat(dt)
            except ValueError: continue
            eligible_volume.append(r)
            if wait:
                try:
                    val=float(wait)
                    if val>=0: eligible_wait.append((r,val))
                except ValueError: pass
    by_dept=defaultdict(lambda:{"completed_encounters":0,"valid_wait_n":0,"wait_sum":0.0})
    for r in eligible_volume: by_dept[r["department"]]["completed_encounters"]+=1
    for r,v in eligible_wait:
        by_dept[r["department"]]["valid_wait_n"]+=1; by_dept[r["department"]]["wait_sum"]+=v
    summaries=[]
    for dept,x in sorted(by_dept.items()):
        summaries.append({"department":dept,"completed_encounters":x["completed_encounters"],
          "valid_wait_n":x["valid_wait_n"],"mean_wait_minutes":round(x["wait_sum"]/x["valid_wait_n"],2) if x["valid_wait_n"] else None})
    report={"dataset":"synthetic_outpatient_encounters.csv",
      "grain":"One source row per encounter record; encounter_id is expected to be unique after duplicate removal.",
      "counts":{"raw_rows":raw_count,"duplicate_rows_removed":len(duplicate_ids),"deduplicated_rows":len(unique),
        "eligible_completed_encounters":len(eligible_volume),"completed_encounters_with_valid_wait":len(eligible_wait)},
      "status_counts":dict(sorted(statuses.items())),"department_summary":summaries,
      "duplicate_encounter_ids":duplicate_ids,"exceptions":exceptions,
      "metric_definitions":{
        "completed_encounters":"Deduplicated records with status=completed, valid encounter date and nonblank department.",
        "mean_wait_minutes":"Arithmetic mean among eligible completed encounters with numeric wait_minutes >= 0; denominator shown as valid_wait_n."},
      "limitations":["Synthetic teaching data; no real-world generalizability.",
        "No arrival/departure timestamps or service-level targets.",
        "First occurrence retained for duplicate IDs; production use requires source-authoritative version rules.",
        "Mean wait is sensitive to outliers and missingness; no causal or clinical conclusions are supported."]}
    return report,unique

def write_outputs(input_path,outdir):
    out=Path(outdir);out.mkdir(parents=True,exist_ok=True)
    report,unique=analyse(load_rows(input_path))
    (out/"quality_report.json").write_text(json.dumps(report,indent=2)+chr(10),encoding="utf-8")
    with (out/"department_summary.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=["department","completed_encounters","valid_wait_n","mean_wait_minutes"])
        w.writeheader();w.writerows(report["department_summary"])
    with sqlite3.connect(out/"analytics.sqlite") as con:
        con.execute("DROP TABLE IF EXISTS encounters_deduplicated")
        con.execute("CREATE TABLE encounters_deduplicated(encounter_id TEXT PRIMARY KEY, patient_id TEXT, department TEXT, encounter_date TEXT, status TEXT, wait_minutes REAL, source_system TEXT)")
        for r in unique:
            wait=(r["wait_minutes"] or "").strip()
            try: wait_value=float(wait) if wait else None
            except ValueError: wait_value=None
            con.execute("INSERT INTO encounters_deduplicated VALUES (?,?,?,?,?,?,?)",
              (r["encounter_id"],r["patient_id"],r["department"] or None,r["encounter_date"] or None,r["status"],wait_value,r["source_system"]))
    manifest={}
    for file in sorted(out.iterdir()):
        if file.is_file() and file.name!="sha256_manifest.json": manifest[file.name]=hashlib.sha256(file.read_bytes()).hexdigest()
    (out/"sha256_manifest.json").write_text(json.dumps(manifest,indent=2)+chr(10),encoding="utf-8")
    return report

def main():
    base=Path(__file__).resolve().parents[1]; p=argparse.ArgumentParser()
    p.add_argument("--input",default=str(base/"data"/"synthetic_outpatient_encounters.csv"))
    p.add_argument("--output",default=str(base/"outputs")); a=p.parse_args()
    print(json.dumps(write_outputs(a.input,a.output),indent=2))
if __name__=="__main__": main()
