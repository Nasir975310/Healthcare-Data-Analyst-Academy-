# Portfolio and client delivery workflow

## Purpose
Convert an analysis project into a reproducible handover scaffold with provenance, a structural data dictionary, executive and technical report templates, a portfolio narrative, and a QA gate.

## Run

```bash
python scripts/delivery_builder.py \\
  --input data/synthetic_encounter_profile.csv \\
  --output outputs/demo_delivery \\
  --title "30-day readmission profile" \\
  --audience "Hospital quality team" \\
  --objective "Describe aggregate readmission patterns for service planning." \\
  --owner "Analytics team"
```

The command copies the CSV, fingerprints the input with SHA-256, profiles missingness and unique values, creates documentation, and writes a ZIP handover archive.

## Reproducible environment
The included environment manifest records Python/platform information and gives explicit instructions for generating a resolved environment lock. It intentionally does not fabricate package versions. For pip environments run `python -m pip freeze > requirements-lock.txt`; for Conda run `conda env export --no-builds > environment-lock.yml`. Review platform compatibility and remove local editable paths before delivery.

## GitHub-ready structure
Keep analysis code under `src/` or `scripts/`, tests under `tests/`, immutable input snapshots under governed `data/raw/`, derived data under `data/processed/`, reports under `reports/`, and docs under `docs/`. Add `.gitignore` rules for secrets, credentials, raw patient data, database files, and local environments. Never push PHI or client-confidential data to a public repository.

## Reporting variants
- Executive: decision context, key validated findings, implications, limitations, next steps.
- Technical: cohort, definitions, provenance, transformations, methods, QA, uncertainty, limitations, reproducibility.

## QA and acceptance
Complete every item in `qa_acceptance_checklist.json`. A false value means the gate is not complete. The automated generator checks structure and provenance; it does not certify clinical, statistical, privacy, legal, or regulatory correctness.
