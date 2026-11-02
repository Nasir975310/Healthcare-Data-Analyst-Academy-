"""Reproducible synthetic hospital encounter analytics pipeline."""
from pathlib import Path
import csv, json, sqlite3
from collections import Counter, defaultdict
from datetime import date
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data/raw/synthetic_hospital_encounters.csv"
PROCESSED = ROOT / "data/processed"
QUARANTINE = ROOT / "data/quarantine"
REPORTS = ROOT / "reports"
DEPARTMENTS = {"General Medicine", "Cardiology", "Orthopaedics", "Neurology", "Pulmonology"}
DISPOSITIONS = {"Home", "Transfer", "Referred", "Expired"}
AGE_BANDS = {"18-29", "30-44", "45-59", "60-74", "75+"}

def run_pipeline():
    for folder in (PROCESSED, QUARANTINE, REPORTS):
        folder.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(RAW, dtype=str, keep_default_na=False)
    raw_rows = len(df)
    df["source_row"] = range(2, raw_rows + 2)
    df["length_of_stay_days"] = pd.to_numeric(df["length_of_stay_days"], errors="coerce")
    df["parsed_date"] = pd.to_datetime(df["admission_date"], errors="coerce")
    checks = {
        "missing_encounter_id": df["encounter_id"].str.strip().eq(""),
        "duplicate_encounter_id": df["encounter_id"].duplicated(keep="first"),
        "missing_patient_token": df["patient_token"].str.strip().eq(""),
        "invalid_date": df["parsed_date"].isna(),
        "invalid_department": ~df["department"].isin(DEPARTMENTS),
        "invalid_length_of_stay": ~df["length_of_stay_days"].between(1, 60),
        "invalid_disposition": ~df["discharge_disposition"].isin(DISPOSITIONS),
        "invalid_age_band": ~df["age_band"].isin(AGE_BANDS),
    }
    issue_counts = {name: int(mask.sum()) for name, mask in checks.items()}
    any_issue = pd.Series(False, index=df.index)
    for mask in checks.values():
        any_issue |= mask
    quarantine = df.loc[any_issue].copy()
    quarantine["quality_issues"] = [
        ";".join(name for name, mask in checks.items() if bool(mask.loc[idx]))
        for idx in quarantine.index
    ]
    clean = df.loc[~any_issue].copy()
    clean["admission_date"] = clean["parsed_date"].dt.strftime("%Y-%m-%d")
    clean["length_of_stay_days"] = clean["length_of_stay_days"].astype(int)
    keep = ["encounter_id","patient_token","admission_date","department","length_of_stay_days","discharge_disposition","age_band"]
    clean[keep].to_csv(PROCESSED / "clean_encounters.csv", index=False)
    quarantine.to_csv(QUARANTINE / "quarantined_encounters.csv", index=False)
    quality = {
        "dataset": RAW.name, "synthetic_data": True, "raw_rows": raw_rows,
        "accepted_rows": int(len(clean)), "quarantined_rows": int(len(quarantine)),
        "acceptance_rate_pct": round(len(clean) / raw_rows * 100, 2),
        "issue_counts_nonexclusive": issue_counts,
        "unique_encounter_ids_after_cleaning": int(clean["encounter_id"].nunique()),
        "rules": {"los_days":"1–60 inclusive","date":"valid ISO calendar date","department":"approved training list","disposition":"approved training list","age_band":"approved training list"},
    }
    (PROCESSED / "quality_report.json").write_text(json.dumps(quality, indent=2))
    db_path = PROCESSED / "hospital_analytics.sqlite"
    with sqlite3.connect(db_path) as conn:
        conn.execute("DROP TABLE IF EXISTS encounters")
        conn.execute("""CREATE TABLE encounters (
            encounter_id TEXT PRIMARY KEY, patient_token TEXT NOT NULL,
            admission_date TEXT NOT NULL, department TEXT NOT NULL,
            length_of_stay_days INTEGER NOT NULL CHECK(length_of_stay_days BETWEEN 1 AND 60),
            discharge_disposition TEXT NOT NULL, age_band TEXT NOT NULL)""")
        clean[keep].to_sql("encounters", conn, if_exists="append", index=False)
        dept = pd.read_sql_query("""SELECT department, COUNT(*) AS encounters,
            ROUND(AVG(length_of_stay_days),2) AS mean_los_days
            FROM encounters GROUP BY department ORDER BY encounters DESC""", conn)
        disp = pd.read_sql_query("""SELECT discharge_disposition, COUNT(*) AS encounters
            FROM encounters GROUP BY discharge_disposition ORDER BY encounters DESC""", conn)
        dept.to_csv(PROCESSED / "department_summary.csv", index=False)
        disp.to_csv(PROCESSED / "disposition_summary.csv", index=False)
        db_rows = conn.execute("SELECT COUNT(*) FROM encounters").fetchone()[0]
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(dept["department"], dept["encounters"])
    ax.set_title("Synthetic encounters by department")
    ax.set_ylabel("Encounter count")
    ax.tick_params(axis="x", rotation=20)
    fig.tight_layout()
    fig.savefig(REPORTS / "department_encounters.png", dpi=140)
    plt.close(fig)
    lines = [
        "# Hospital Encounter Analytics — Training Report", "",
        "> Synthetic training dataset. Not real hospital performance or clinical evidence.", "",
        "## Data pipeline summary",
        f"- Raw records: {raw_rows}", f"- Accepted records: {len(clean)}",
        f"- Quarantined records: {len(quarantine)}",
        f"- Acceptance rate: {quality['acceptance_rate_pct']}%",
        f"- SQLite row count: {db_rows}", "",
        "## Non-exclusive quality issue counts",
        "| Rule | Rows flagged |", "|---|---:|",
    ]
    lines += [f"| {k} | {val} |" for k,val in issue_counts.items()]
    lines += ["", "Issue counts are non-exclusive: one row may violate multiple rules.", "",
              "## Department summary", dept.to_markdown(index=False), "",
              "## Discharge disposition summary", disp.to_markdown(index=False), "",
              "## Limitations", "- All records are fictional and generated for learning.",
              "- Quarantined records are excluded, not automatically repaired.",
              "- The descriptive summaries are not risk-adjusted and do not establish causality.",
              "- Validate definitions and business rules with an authorised data owner before real use."]
    (REPORTS / "project_report.md").write_text("\n".join(lines))
    return quality

if __name__ == "__main__":
    print(json.dumps(run_pipeline(), indent=2))
