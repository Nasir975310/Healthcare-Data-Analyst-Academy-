#!/usr/bin/env python3
"""Descriptive reference analysis for synthetic antihypertensive DUE cohort."""
import csv,json,argparse,statistics
from pathlib import Path
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--input",default="professional_simulations/data/antihypertensive_due_cohort.csv");ap.add_argument("--output",default="professional_simulations/outputs/due_summary.json");a=ap.parse_args()
 with open(a.input,newline="",encoding="utf-8") as f:rows=list(csv.DictReader(f))
 issues=[];valid=[];paired=[]
 for i,r in enumerate(rows,2):
  probs=[]
  try:age=int(r["age_years"])
  except:age=None;probs.append("invalid_age")
  if age is not None and not 18<=age<=110:probs.append("implausible_age")
  try:days=int(r["followup_days"])
  except:days=None;probs.append("invalid_followup_days")
  if days is not None and not 0<days<=365:probs.append("implausible_followup_interval")
  try:b=int(r["baseline_sbp_mmhg"])
  except:b=None;probs.append("invalid_baseline_sbp")
  try:f=int(r["followup_sbp_mmhg"])
  except:f=None;probs.append("missing_or_invalid_followup_sbp")
  if probs:issues.append({"source_row":i,"study_id":r["study_id"],"issues":probs})
  if age is not None and 18<=age<=110 and days is not None and 0<days<=365 and b is not None:valid.append(r)
  if age is not None and 18<=age<=110 and days is not None and 0<days<=365 and b is not None and f is not None:paired.append((r,b,f))
 changes=[f-b for r,b,f in paired]
 byclass={}
 for cl in sorted({r["antihypertensive_class"] for r,b,f in paired}):
  vals=[f-b for r,b,f in paired if r["antihypertensive_class"]==cl]
  byclass[cl]={"paired_n":len(vals),"mean_sbp_change_mmhg":round(statistics.mean(vals),2) if vals else None}
 out={"records_raw":len(rows),"records_valid_for_baseline_description":len(valid),"paired_sbp_denominator":len(paired),"records_with_quality_flags":len(issues),"mean_baseline_sbp_paired":round(statistics.mean([b for r,b,f in paired]),2),"mean_followup_sbp_paired":round(statistics.mean([f for r,b,f in paired]),2),"mean_change_followup_minus_baseline_mmhg":round(statistics.mean(changes),2),"class_summaries":byclass,"issue_log":issues,"interpretation":"Synthetic descriptive analysis only. Unadjusted class comparisons are not causal or comparative-effectiveness evidence."}
 Path(a.output).parent.mkdir(parents=True,exist_ok=True);Path(a.output).write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items() if k!="issue_log"},indent=2))
if __name__=="__main__":main()
