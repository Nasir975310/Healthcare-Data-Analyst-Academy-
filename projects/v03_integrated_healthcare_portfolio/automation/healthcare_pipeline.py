"""Reproducible synthetic encounter analytics pipeline."""
from __future__ import annotations
import argparse
import logging
import json
from pathlib import Path
import sys
import pandas as pd

REQUIRED = {
    "encounter_id", "patient_id", "department_id", "admission_date",
    "encounter_type", "systolic_bp"
}

def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, dtype={
        "encounter_id": "string", "patient_id": "string",
        "department_id": "string"
    })
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    return df

def validate_encounters(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        raise ValueError("Input dataset contains no encounter rows.")
    if df["encounter_id"].isna().any() or df["encounter_id"].str.strip().eq("").any():
        raise ValueError("Encounter IDs must be nonmissing.")
    if not df["encounter_id"].is_unique:
        raise ValueError("Encounter IDs must be unique at encounter grain.")
    out = df.copy()
    out["admission_date"] = pd.to_datetime(out["admission_date"], errors="coerce")
    if out["admission_date"].isna().any():
        raise ValueError("One or more admission dates are missing or invalid.")
    out["systolic_bp"] = pd.to_numeric(out["systolic_bp"], errors="coerce")
    out["department_id"] = out["department_id"].astype("string")
    return out

def filter_period(df: pd.DataFrame, start: str, end: str) -> pd.DataFrame:
    start_ts, end_ts = pd.Timestamp(start), pd.Timestamp(end)
    if start_ts >= end_ts:
        raise ValueError("start-date must be earlier than end-date.")
    return df.loc[
        (df["admission_date"] >= start_ts) &
        (df["admission_date"] < end_ts)
    ].copy()

def summarize(df: pd.DataFrame, departments: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    if not departments["department_id"].is_unique:
        raise ValueError("Department lookup must have unique department_id values.")
    joined = df.merge(
        departments[["department_id", "department_name"]],
        on="department_id", how="left", validate="many_to_one", indicator=True
    )
    unmatched = int((joined["_merge"] != "both").sum())
    if len(joined) != len(df):
        raise AssertionError("Department join changed encounter row count.")
    summary = (joined.groupby("department_name", dropna=False)
        .agg(
            encounter_n=("encounter_id", "size"),
            unique_patients=("patient_id", "nunique"),
            sbp_nonmissing_n=("systolic_bp", "count"),
            mean_sbp=("systolic_bp", "mean"),
            median_sbp=("systolic_bp", "median")
        ).reset_index())
    summary["sbp_missing_n"] = summary["encounter_n"] - summary["sbp_nonmissing_n"]
    summary["sbp_completeness_pct"] = (
        100 * summary["sbp_nonmissing_n"] / summary["encounter_n"]
    )
    summary[["mean_sbp", "median_sbp", "sbp_completeness_pct"]] = (
        summary[["mean_sbp", "median_sbp", "sbp_completeness_pct"]].round(2)
    )
    metrics = {
        "cohort_encounters": int(len(df)),
        "unique_patients": int(df["patient_id"].nunique()),
        "sbp_nonmissing": int(df["systolic_bp"].notna().sum()),
        "sbp_missing": int(df["systolic_bp"].isna().sum()),
        "unmatched_departments": unmatched,
        "department_encounter_sum": int(summary["encounter_n"].sum())
    }
    if metrics["department_encounter_sum"] != metrics["cohort_encounters"]:
        raise AssertionError("Department counts do not reconcile to cohort total.")
    return summary, metrics

def run(input_path: Path, output_dir: Path, start: str, end: str) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    logging.info("Loading source file: %s", input_path.name)
    raw = load_data(input_path)
    logging.info("Source rows: %d", len(raw))
    clean = validate_encounters(raw)
    cohort = filter_period(clean, start, end)
    departments_path = input_path.parent / "departments.csv"
    if not departments_path.exists():
        raise FileNotFoundError(f"Department lookup not found: {departments_path}")
    departments = pd.read_csv(departments_path, dtype={"department_id": "string"})
    if "department_name" not in departments.columns or "department_id" not in departments.columns:
        raise ValueError("Department lookup requires department_id and department_name.")
    summary, metrics = summarize(cohort, departments)
    summary.to_csv(output_dir / "department_summary.csv", index=False)
    metrics.update({
        "source_file": input_path.name,
        "reporting_start_inclusive": start,
        "reporting_end_exclusive": end,
        "source_rows": int(len(raw)),
        "cohort_unique_encounters": int(cohort["encounter_id"].nunique())
    })
    import json
    (output_dir / "run_metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    logging.info("Completed: %d cohort encounters; %d unique patients", metrics["cohort_encounters"], metrics["unique_patients"])
    return metrics

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Path to encounters.csv")
    parser.add_argument("--output-dir", type=Path, required=True, help="Directory for outputs")
    parser.add_argument("--start-date", default="2026-01-01", help="Inclusive YYYY-MM-DD")
    parser.add_argument("--end-date", default="2026-04-01", help="Exclusive YYYY-MM-DD")
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    try:
        metrics = run(args.input, args.output_dir, args.start_date, args.end_date)
        print(json.dumps(metrics, indent=2))
        return 0
    except Exception as exc:
        logging.exception("Pipeline failed: %s", exc)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
