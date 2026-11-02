"""Generate a portfolio documentation pack from the v4.8 synthetic project outputs."""
from pathlib import Path
import argparse, csv, json, hashlib, subprocess, sys
from datetime import datetime, timezone

FIELDS = [
("encounter_id","Unique encounter-level identifier","string","none","Unique, non-empty","No missing values","Raw CSV","Primary key uniqueness"),
("patient_token","Synthetic patient linkage token","string","none","SYN-* token","No missing values","Raw CSV","Non-empty"),
("admission_date","Encounter admission calendar date","date","YYYY-MM-DD","Valid ISO calendar date","No missing values","Raw CSV","Date parser"),
("department","Training department category","string","category","Approved department list","No missing values","Raw CSV","Allow-list membership"),
("length_of_stay_days","Encounter length of stay","integer","days","1–60 inclusive","No missing values","Raw CSV","Numeric range"),
("discharge_disposition","Training discharge category","string","category","Home, Transfer, Referred, Expired","No missing values","Raw CSV","Allow-list membership"),
("age_band","Age category band","string","category","18-29, 30-44, 45-59, 60-74, 75+","No missing values","Raw CSV","Allow-list membership"),
]
METRICS = [
("Encounter count","How many accepted encounter records are in the cleaned dataset?","Count of encounter_id","Not applicable","One row per encounter","No additional filter","Quarantined records excluded","encounters","Analyst","SQLite count equals accepted row count"),
("Mean length of stay","What is the arithmetic mean LOS among accepted encounters?","Sum of length_of_stay_days","Count of accepted encounters with valid LOS","Encounter","No additional filter","Quarantined records excluded","days","Analyst","SQL AVG reconciles to cleaned data"),
("Department encounter volume","How many accepted encounters are assigned to each department?","Count of encounter_id within department","Not applicable","Encounter","Group by department","Quarantined records excluded","encounters","Analyst","Department totals sum to accepted row count"),
]
def write_csv(path, header, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(header); w.writerows(rows)
def sha256(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()
def build(project:Path, output:Path):
    quality_path=project/"data/processed/quality_report.json"
    if not quality_path.exists():
        raise FileNotFoundError("Run the v4.8 project first: python run_project.py")
    q=json.loads(quality_path.read_text(encoding="utf-8"))
    if q.get("synthetic_data") is not True:
        raise ValueError("This portfolio generator expects the declared synthetic training fixture.")
    output.mkdir(parents=True,exist_ok=True)
    write_csv(output/"data_dictionary.csv",
      ["field_name","definition","data_type","unit","allowed_values","missing_value_meaning","source","validation_rule"],FIELDS)
    write_csv(output/"metric_contract.csv",
      ["metric_name","business_question","numerator","denominator","grain","filters","exclusions","unit","owner","validation_test"],METRICS)
    quality_lines=["# QA and Reproducibility Summary","",
      "> Generated from the v4.8 synthetic training project. Review before publication.","",
      f"- Dataset: `{q['dataset']}`",f"- Raw rows: {q['raw_rows']}",
      f"- Accepted rows: {q['accepted_rows']}",f"- Quarantined rows: {q['quarantined_rows']}",
      f"- Acceptance rate: {q['acceptance_rate_pct']}%",
      f"- Unique cleaned encounter IDs: {q['unique_encounter_ids_after_cleaning']}","",
      "## Non-exclusive issue counts","",
      "| Check | Rows flagged |","|---|---:|"]
    quality_lines += [f"| {k} | {v} |" for k,v in q["issue_counts_nonexclusive"].items()]
    quality_lines += ["","Issue counts are non-exclusive. A row may fail more than one rule.",
      "## Reproduction","",
      "```bash","python run_project.py","python -m pytest -q","```","",
      "## Interpretation boundary",
      "This is synthetic data. Descriptive summaries do not establish causality, clinical validity or real hospital performance."]
    (output/"qa_reproducibility.md").write_text("\n".join(quality_lines),encoding="utf-8")
    readme=f"""# Synthetic Hospital Encounter Analytics

## Project summary
A reproducible training project demonstrating healthcare encounter data profiling, rule-based validation, quarantine, SQLite loading, SQL summaries and report generation.

## Dataset
- File: `{q['dataset']}`
- Raw rows: {q['raw_rows']}
- Accepted rows: {q['accepted_rows']}
- Quarantined rows: {q['quarantined_rows']}
- Grain: one row per encounter
- Primary key: `encounter_id`

## Tools
Python, pandas, SQLite, SQL, pytest and Matplotlib.

## Run
```bash
python -m pip install -r requirements.txt
python run_project.py
python -m pytest -q
```

## Quality controls
See `qa_reproducibility.md` for non-exclusive issue counts, reconciliation and reproduction steps. Data dictionary and metric contract are included in this portfolio pack.

## Outputs
Clean CSV, quarantine CSV, quality report, SQLite database, SQL summaries, Markdown report and chart.

## Limitations
All data is synthetic. Results are not actual hospital performance, clinical evidence or causal estimates. Quarantined records are excluded rather than automatically repaired. Real patient data would require formal authority, approved security controls and governance.
"""
    (output/"README_draft.md").write_text(readme,encoding="utf-8")
    inventory=[
      ("Raw synthetic CSV","data/raw/synthetic_hospital_encounters.csv","Input fixture; synthetic only"),
      ("Pipeline source","src/hda_project/pipeline.py","Profiling, validation, quarantine, SQLite and reporting"),
      ("SQL queries","sql/analysis_queries.sql","Grouped summaries and reconciliation"),
      ("Automated tests","tests/test_pipeline.py","Pipeline and quality-rule tests"),
      ("Generated quality report","data/processed/quality_report.json","Counts and issue flags"),
      ("Generated analytical report","reports/project_report.md","Descriptive findings and limitations"),
      ("Generated chart","reports/department_encounters.png","Department encounter counts"),
    ]
    write_csv(output/"portfolio_evidence_inventory.csv",["evidence_item","repository_path","what_it_demonstrates"],inventory)
    (output/"cv_evidence_worksheet.md").write_text((Path(__file__).resolve().parents[1]/"templates/cv_evidence_worksheet.md").read_text(),encoding="utf-8")
    (output/"interview_questions.md").write_text((Path(__file__).resolve().parents[1]/"templates/interview_bank.md").read_text(),encoding="utf-8")
    manifest={"generated_utc":datetime.now(timezone.utc).isoformat(),"dataset":q["dataset"],
      "synthetic_data":True,"raw_rows":q["raw_rows"],"accepted_rows":q["accepted_rows"],
      "quarantined_rows":q["quarantined_rows"],"files":[]}
    for p in sorted(project.rglob("*")):
        if p.is_file() and not any(part in {".venv","__pycache__",".pytest_cache"} for part in p.parts) and p.suffix not in {".sqlite",".db",".pyc"}:
            manifest["files"].append({"path":str(p.relative_to(project)),"sha256":sha256(p)})
    (output/"evidence_manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
    checklist="""# Publication quality gate

- [ ] Dataset is synthetic or explicitly authorised for public release.
- [ ] No PHI, credentials, `.env`, confidential notes or private client paths.
- [ ] README accurately describes the work and limitations.
- [ ] Data dictionary and metric contract reviewed.
- [ ] Raw, accepted and quarantined counts reconcile.
- [ ] Primary key uniqueness tested.
- [ ] SQL totals reconcile to cleaned data.
- [ ] Project runs from a clean environment.
- [ ] Automated tests pass and actual output is recorded.
- [ ] Charts have readable labels, units and denominators.
- [ ] No unsupported causal, clinical, financial or compliance claims.
- [ ] CV statements are backed by inspectable repository evidence.
- [ ] Git staged diff reviewed before pushing.
- [ ] Public repository visibility deliberately approved.
"""
    (output/"publication_quality_gate.md").write_text(checklist,encoding="utf-8")
    return manifest
if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--project",type=Path,default=Path("../project_execution_v48"))
    ap.add_argument("--output",type=Path,default=Path("output"))
    a=ap.parse_args()
    m=build(a.project.resolve(),a.output.resolve())
    print(f"Generated portfolio pack with {len(m['files'])} source-file hashes.")
