# v5.34.0 — Deployment Evidence & Reproducibility Workbench

This module adds a containerized PostgreSQL practice environment, repeatable database validation, local evidence capture, a CI workflow, and a release-readiness gate for the v5.32/v5.33 synthetic hospital practicum.

## Quick start
From this directory:
```bash
python scripts/capture_local_evidence.py
python -m unittest discover -s tests -v
```

For PostgreSQL, run from the Academy root:
```bash
cd healthcare_analytics_deployment_evidence_v534
bash scripts/run_postgres_validation.sh
```
Requires Docker Engine and the Docker Compose plugin. The Compose stack mounts only the synthetic v5.32 CSV files read-only. The database is local practice infrastructure, not a production deployment.

## Outputs
- `evidence/local_evidence.json`: locally generated test and provenance evidence.
- `evidence/postgres_validation.json`: generated only after the PostgreSQL container workflow succeeds.
- `evidence/templates/`: external Power BI and GitHub evidence templates.
- `docker/`: PostgreSQL 16 container and initialization scripts.
- `.github/workflows/quality.yml`: repository CI workflow.

## What is and is not verified
Python validation, SQLite benchmark, file hashes, and unit tests can run locally. PostgreSQL container execution requires Docker and is run by the user on their machine. Power BI Desktop validation and GitHub publication remain external acceptance tasks. Never mark these as complete without evidence.

All patient and encounter data in this project are synthetic. Do not load identifiable patient data into this practice stack.
