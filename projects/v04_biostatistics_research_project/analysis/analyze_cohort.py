#!/usr/bin/env python3
"""Reproducible descriptive analysis for the synthetic Volume 4 cohort."""
from pathlib import Path
import argparse
import pandas as pd

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="../data/synthetic_biostatistics_cohort.csv")
    parser.add_argument("--output", default="../outputs")
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    source = (here / args.input).resolve()
    out = (here / args.output).resolve()
    out.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(source)
    required = {"patient_id","age_years","diabetes","regimen_group","discharge_sbp","readmission_30d","site"}
    missing = required - set(df.columns)
    if missing: raise ValueError(f"Missing required columns: {sorted(missing)}")
    if df["patient_id"].duplicated().any(): raise ValueError("patient_id must be unique in this exercise")
    if not set(df["diabetes"].dropna().unique()).issubset({0,1}): raise ValueError("Unexpected diabetes coding")
    if not set(df["readmission_30d"].dropna().unique()).issubset({0,1}): raise ValueError("Unexpected outcome coding")
    summary = df.groupby("regimen_group", dropna=False).agg(
        encounters=("patient_id","size"),
        sbp_n=("discharge_sbp","count"),
        sbp_mean=("discharge_sbp","mean"),
        sbp_sd=("discharge_sbp","std"),
        sbp_median=("discharge_sbp","median"),
        readmissions=("readmission_30d","sum"),
        outcome_n=("readmission_30d","count")
    ).reset_index()
    summary["sbp_missing_pct"] = 100*(summary["encounters"]-summary["sbp_n"])/summary["encounters"]
    summary["readmission_pct"] = 100*summary["readmissions"]/summary["outcome_n"]
    summary.to_csv(out/"group_summary.csv", index=False)
    missingness = pd.DataFrame({"variable":df.columns,"missing_n":[int(df[c].isna().sum()) for c in df.columns]})
    missingness["missing_pct"] = 100*missingness["missing_n"]/len(df)
    missingness.to_csv(out/"missingness.csv",index=False)
    (out/"validation.txt").write_text(
        f"rows={len(df)}\nunique_patients={df.patient_id.nunique()}\n"
        f"duplicate_patient_ids={int(df.patient_id.duplicated().sum())}\n"
        f"missing_discharge_sbp={int(df.discharge_sbp.isna().sum())}\n"
        "All checks are structural; no clinical validity is implied.\n"
    )
    print(summary.to_string(index=False))
    print(f"\nOutputs written to {out}")
if __name__ == "__main__": main()
