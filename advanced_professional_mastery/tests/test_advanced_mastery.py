#!/usr/bin/env python3
"""Regression checks for v3.8 advanced professional mastery fixtures."""
import csv,json,sqlite3,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];A=ROOT/"advanced_professional_mastery"
def main():
 db=sqlite3.connect(A/"data/advanced_healthcare_analytics.db")
 assert db.execute("select count(*) from encounters").fetchone()[0]==5000
 assert db.execute("select count(*) from medication_orders").fetchone()[0]==20000
 assert db.execute("select count(*) from lab_observations").fetchone()[0]==15000
 orphan=db.execute("select count(*) from medication_orders o left join encounters e using(encounter_id) where e.encounter_id is null").fetchone()[0]
 assert orphan==540
 q=subprocess.run([sys.executable,str(A/"solutions/statistical_validation.py"),"--input",str(A/"data/observational_sbp_cohort.csv"),"--output",str(A/"outputs/test_stat.json")],capture_output=True,text=True)
 assert q.returncode==0,q.stderr
 stat=json.loads((A/"outputs/test_stat.json").read_text())
 assert (stat["raw_n"],stat["complete_case_n"],stat["treated_n"])==(1200,1181,171)
 assert round(stat["crude_difference_treated_minus_untreated"],2)==6.66
 assert round(stat["adjusted_treatment_coefficient"],2)==-3.62
 assert stat["adjusted_robust_95ci"][0]<0<stat["crude_robust_95ci"][0] or stat["crude_robust_95ci"][0]>0
 print("PASS: database row counts, 540 orphan orders, statistical cohort denominators and regression outputs")
def test_advanced_mastery(): main()
if __name__=="__main__":main()
