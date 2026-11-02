"""Starter: profile synthetic practicum data. Run with pandas installed.
Usage: python profile_and_validate.py ../data/hospital_encounters_raw.csv
"""
import argparse, json
from pathlib import Path
import pandas as pd

def profile(path):
    df = pd.read_csv(path)
    result = {
        "file": Path(path).name,
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "missing_by_column": {k:int(v) for k,v in df.isna().sum().items()},
        "duplicate_rows": int(df.duplicated().sum()),
        "duplicate_encounter_ids": int(df["encounter_id"].duplicated().sum()) if "encounter_id" in df else None,
    }
    if {"admission_date","discharge_date"}.issubset(df.columns):
        a=pd.to_datetime(df.admission_date,errors="coerce")
        d=pd.to_datetime(df.discharge_date,errors="coerce")
        result["invalid_date_order"]=int((d<a).sum())
        result["unparseable_admission_dates"]=int(a.isna().sum())
        result["unparseable_discharge_dates"]=int(d.isna().sum())
    return result

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("csv")
    args=p.parse_args()
    print(json.dumps(profile(args.csv),indent=2))
