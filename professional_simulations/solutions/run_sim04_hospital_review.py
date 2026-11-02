#!/usr/bin/env python3
"""Reference quality profile and KPI calculations for SIM-04; synthetic data only."""
import csv, json, argparse
from pathlib import Path
from collections import Counter, defaultdict
from datetime import date
def read(p):
 with open(p,newline="",encoding="utf-8") as f:return list(csv.DictReader(f))
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--data",default="professional_simulations/data");ap.add_argument("--out",default="professional_simulations/outputs");a=ap.parse_args()
 d=Path(a.data);o=Path(a.out);o.mkdir(parents=True,exist_ok=True)
 raw=read(d/"encounters_raw.csv");orders=read(d/"medication_orders_raw.csv")
 seen=set();valid=[];issues=[]
 for n,r in enumerate(raw,2):
  eid=r["encounter_id"];problems=[]
  if eid in seen:problems.append("duplicate_encounter_id")
  seen.add(eid)
  try: los=int(r["length_of_stay_days"])
  except: los=None;problems.append("invalid_los")
  if los is not None and los<0:problems.append("negative_los")
  try:
   ad=date.fromisoformat(r["admit_date"]);dd=date.fromisoformat(r["discharge_date"])
   if dd<ad:problems.append("discharge_before_admission")
  except:problems.append("invalid_date")
  if not r["department"]:problems.append("missing_department")
  if r["payer"] not in {"Self-pay","Insurance A","Insurance B","Government"}:problems.append("invalid_payer")
  if not r["patient_key"]:problems.append("missing_patient_key")
  if problems:issues.append({"source_row":n,"encounter_id":eid,"issues":problems})
  if not problems:valid.append(r)
 # explicit duplicate strategy: first row retained, subsequent duplicate quarantined.
 bydept=defaultdict(list)
 for r in valid:bydept[r["department"]].append(r)
 kpis=[]
 for dep,rows in sorted(bydept.items()):
  los=[int(x["length_of_stay_days"]) for x in rows]
  flags=[int(x["readmission_30d_flag"]) for x in rows]
  kpis.append({"department":dep,"encounters":len(rows),"mean_los_days":round(sum(los)/len(los),2),"supplied_flag_count":sum(flags),"supplied_flag_rate_pct":round(100*sum(flags)/len(flags),2)})
 ids={r["encounter_id"] for r in valid}
 orphan=[r for r in orders if r["encounter_id"] not in ids]
 order_issues=[]
 for n,r in enumerate(orders,2):
  probs=[]
  try:
   if int(r["quantity"])<=0:probs.append("nonpositive_quantity")
  except:probs.append("invalid_quantity")
  if r["unit_cost_inr"]=="":probs.append("missing_unit_cost")
  if not r["therapeutic_class"]:probs.append("missing_therapeutic_class")
  if r["encounter_id"] not in ids:probs.append("orphan_encounter_reference")
  if not r["drug_name"]:probs.append("missing_drug_name")
  if probs:order_issues.append({"source_row":n,"order_id":r["order_id"],"issues":probs})
 summary={"encounters_raw":len(raw),"encounters_valid":len(valid),"encounter_rows_quarantined":len(issues),"orders_raw":len(orders),"orphan_order_rows":len(orphan),"order_rows_with_one_or_more_issues":len(order_issues),"valid_encounter_denominator":len(valid),"readmission_flag_caveat":"Supplied synthetic flag; not validated clinical readmission."}
 for name,rows in [("department_kpis.csv",kpis),("encounter_issue_log.json",issues),("order_issue_log.json",order_issues),("summary.json",[summary])]:
  p=o/name
  if name.endswith(".csv"):
   with p.open("w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys() if rows else []);w.writeheader();w.writerows(rows)
  else:p.write_text(json.dumps(rows[0] if name=="summary.json" else rows,indent=2))
 print(json.dumps(summary,indent=2))
if __name__=="__main__":main()
