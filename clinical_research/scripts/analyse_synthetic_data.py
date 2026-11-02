#!/usr/bin/env python3
"""Descriptive analysis of synthetic trial and pharmacovigilance training data."""
from pathlib import Path
import pandas as pd
BASE=Path(__file__).resolve().parents[1]
trial=pd.read_csv(BASE/"data/synthetic_trial_subjects.csv")
pv=pd.read_csv(BASE/"data/synthetic_pv_cases.csv")
assert trial.subject_id.is_unique and pv.case_id.is_unique
trial["change_sbp"]=trial.week12_sbp-trial.baseline_sbp
print("TRIAL: subject counts by arm")
print(trial.groupby("arm").agg(n=("subject_id","nunique"),mean_baseline=("baseline_sbp","mean"),mean_week12=("week12_sbp","mean"),mean_change=("change_sbp","mean"),ae_count=("ae_flag","sum")).round(2))
print("\\nPV: case counts by product/event")
print(pv.groupby(["product","event_code"]).agg(cases=("case_id","nunique"),serious=("serious","sum")).reset_index().to_string(index=False))
print("\\nPV data quality")
print({"duplicate_case_ids":int(pv.case_id.duplicated().sum()),"receipt_before_onset":int((pd.to_datetime(pv.receipt_date)<pd.to_datetime(pv.onset_date)).sum()),"serious_cases":int(pv.serious.sum())})
