# v5.33.0 — Healthcare Analytics Production Validation & Portfolio Deployment

This module turns the v5.32 fictional hospital practicum into a production-style delivery exercise. All data and organizations are fictional. No patient data is included.

## Run locally
From this directory:
```bash
python scripts/validate_practicum.py
python scripts/benchmark_sqlite.py
python -m unittest discover -s tests -v
```
The validator reads the v5.32 generated CSV outputs and checks schema, key uniqueness, referential integrity, plausible ranges, reconciliation and privacy-safe output rules. It reports PASS/FAIL/WARN and exits non-zero on failed critical checks.

## Contents
- `powerbi/`: star-schema guidance, Power Query M patterns, DAX measures, report QA and performance checklist. These are implementation assets; a PBIX was not created or executed here.
- `sql/postgresql/`: PostgreSQL staging/curated DDL, migration and validation queries. They require a running PostgreSQL instance and are not claimed as executed.
- `scripts/`: portable SQLite benchmark and v5.32 deliverable validator.
- `portfolio/`: GitHub publication structure, README template, issue/PR and evidence checklist.
- `assessment/`: client presentation brief and scored practical rubric.
- `roadmap/`: interactive task tracker.

## Important limits
The current build validates Python/SQLite assets only. Power BI Desktop is not natively available in the Linux/Hyprland environment described for this workstation. PostgreSQL scripts are provided for a real server test. GitHub publication requires the user's own repository and explicit push.
