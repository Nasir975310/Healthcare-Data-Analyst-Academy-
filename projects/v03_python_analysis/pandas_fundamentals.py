"""pandas fundamentals: Q1 2026 encounter and department summary."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "datasets" / "v03_python"
OUT = ROOT / "projects" / "v03_python_analysis" / "reports"
OUT.mkdir(parents=True, exist_ok=True)

enc = pd.read_csv(DATA / "encounters.csv", dtype={"encounter_id":"string","patient_id":"string"})
dept = pd.read_csv(DATA / "departments.csv")
enc["admission_date"] = pd.to_datetime(enc["admission_date"], errors="coerce")
enc["systolic_bp"] = pd.to_numeric(enc["systolic_bp"], errors="coerce")

cohort = enc.loc[
    (enc["admission_date"] >= "2026-01-01") &
    (enc["admission_date"] < "2026-04-01")
].copy()
assert cohort["encounter_id"].is_unique, "Encounter grain is not unique."

joined = cohort.merge(
    dept[["department_id","department_name"]],
    on="department_id", how="left", validate="many_to_one", indicator=True
)
unmatched = int((joined["_merge"] != "both").sum())
assert len(joined) == len(cohort), "Department merge changed row count."
summary = (joined.groupby("department_name", dropna=False)
    .agg(encounter_n=("encounter_id","size"),
         unique_patients=("patient_id","nunique"),
         sbp_nonmissing_n=("systolic_bp","count"),
         mean_sbp=("systolic_bp","mean"))
    .reset_index())
summary["sbp_missing_n"] = summary["encounter_n"] - summary["sbp_nonmissing_n"]
summary["mean_sbp"] = summary["mean_sbp"].round(1)
summary.to_csv(OUT / "pandas_department_summary.csv", index=False)

print("Cohort encounters:", len(cohort))
print("Unique patients:", cohort["patient_id"].nunique())
print("Unmatched departments:", unmatched)
print(summary.to_string(index=False))
