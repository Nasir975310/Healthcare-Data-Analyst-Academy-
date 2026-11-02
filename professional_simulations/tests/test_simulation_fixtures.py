#!/usr/bin/env python3
"""Regression checks for v3.7 synthetic professional simulation fixtures."""
import csv,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SIM=ROOT/"professional_simulations"
def rows(name):
 with (SIM/"data"/name).open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))
def main():
 assert len(rows("encounters_raw.csv"))==501
 assert len(rows("medication_orders_raw.csv"))==1000
 assert len(rows("antihypertensive_due_cohort.csv"))==300
 out=SIM/"outputs"/"regression"
 a=subprocess.run([sys.executable,str(SIM/"solutions/run_sim04_hospital_review.py"),"--data",str(SIM/"data"),"--out",str(out/"sim04")],capture_output=True,text=True)
 assert a.returncode==0,a.stderr
 s=json.loads((out/"sim04/summary.json").read_text())
 assert (s["encounters_raw"],s["encounters_valid"],s["encounter_rows_quarantined"])==(501,495,6)
 assert (s["orders_raw"],s["orphan_order_rows"],s["order_rows_with_one_or_more_issues"])==(1000,6,11)
 b=subprocess.run([sys.executable,str(SIM/"solutions/run_sim05_due_review.py"),"--input",str(SIM/"data/antihypertensive_due_cohort.csv"),"--output",str(out/"sim05/due_summary.json")],capture_output=True,text=True)
 assert b.returncode==0,b.stderr
 d=json.loads((out/"sim05/due_summary.json").read_text())
 assert (d["records_raw"],d["records_valid_for_baseline_description"],d["paired_sbp_denominator"],d["records_with_quality_flags"])==(300,298,297,3)
 assert round(d["mean_change_followup_minus_baseline_mmhg"],2)==-13.96
 print("PASS: dataset counts, SIM-04 quality counts, SIM-05 denominators and summary statistic")
if __name__=="__main__":main()
