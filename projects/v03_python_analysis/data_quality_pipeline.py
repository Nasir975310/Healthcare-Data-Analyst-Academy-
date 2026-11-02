"""Auditable data-quality profile; raw input is never overwritten."""
from pathlib import Path
import pandas as pd
import json

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "datasets" / "v03_python" / "encounters.csv"
OUT = ROOT / "projects" / "v03_python_analysis" / "reports"
OUT.mkdir(parents=True, exist_ok=True)

raw = pd.read_csv(SOURCE, dtype={"encounter_id":"string","patient_id":"string","department_id":"string"})
required = ["encounter_id","patient_id","department_id","admission_date","encounter_type","systolic_bp"]
missing_columns = [c for c in required if c not in raw.columns]
if missing_columns:
    raise ValueError(f"Missing required columns: {missing_columns}")

df = raw.copy()
df["admission_date_parsed"] = pd.to_datetime(df["admission_date"], errors="coerce")
df["sbp_parsed"] = pd.to_numeric(df["systolic_bp"], errors="coerce")
df["missing_encounter_id"] = df["encounter_id"].isna() | df["encounter_id"].str.strip().eq("")
df["duplicate_encounter_id"] = df["encounter_id"].duplicated(keep=False)
df["invalid_admission_date"] = df["admission_date"].notna() & df["admission_date_parsed"].isna()
df["invalid_sbp_parse"] = df["systolic_bp"].notna() & df["systolic_bp"].astype(str).str.strip().ne("") & df["sbp_parsed"].isna()
df["missing_sbp"] = df["sbp_parsed"].isna()
df["discharge_date_parsed"] = pd.to_datetime(df["discharge_date"], errors="coerce")
df["discharge_before_admission"] = (
    df["discharge_date_parsed"].notna() & df["admission_date_parsed"].notna() &
    (df["discharge_date_parsed"] < df["admission_date_parsed"])
)
flag_cols = [c for c in df.columns if c.startswith(("missing_","duplicate_","invalid_","discharge_before_"))]
df["any_quality_flag"] = df[flag_cols].any(axis=1)
df.to_csv(OUT / "encounters_quality_flags.csv", index=False)

report = {
    "source_file": SOURCE.name,
    "row_count": int(len(df)),
    "unique_encounter_ids": int(df["encounter_id"].nunique(dropna=True)),
    "duplicate_encounter_id_rows": int(df["duplicate_encounter_id"].sum()),
    "missing_sbp": int(df["missing_sbp"].sum()),
    "invalid_admission_date": int(df["invalid_admission_date"].sum()),
    "invalid_sbp_parse": int(df["invalid_sbp_parse"].sum()),
    "discharge_before_admission": int(df["discharge_before_admission"].sum()),
    "rows_with_any_flag": int(df["any_quality_flag"].sum()),
    "column_missingness": {k:int(v) for k,v in df.isna().sum().items()}
}
(OUT / "data_quality_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
