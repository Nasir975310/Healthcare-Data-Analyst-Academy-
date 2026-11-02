# v5.37.0 — Application Execution & Technical Assessment Lab

A practical execution layer for the Academy's employment transition. Use it to screen role fit, tailor applications truthfully, complete a reproducible SQL/Python assessment, rehearse a portfolio walkthrough and review weekly search performance.

## Quick start
From this directory:
```bash
python scripts/role_fit.py --job examples/junior_healthcare_analyst_job.txt --evidence examples/candidate_evidence.json
python scripts/run_sql_assessment.py --db fixtures/clinic_ops.sqlite --output reports
python scripts/application_metrics.py --input templates/application_tracker.csv
python -m unittest discover -s tests -v
```
The SQLite fixture is generated and synthetic. The SQL assessment runs real queries against that fixture. Role-fit scoring is keyword/evidence matching, not an ATS prediction. Application metrics are descriptive and do not establish causality.

## Suggested weekly cadence
- 2 focused sessions to complete or improve a portfolio artifact.
- 8–12 carefully matched applications, adjusted to available time and role quality.
- 2 interview answers recorded and reviewed.
- 1 weekly metrics review and next-week adjustment.
Do not mass-apply indiscriminately or claim skills that you cannot demonstrate.

## Data and integrity
All included records are fictional. Never insert patient-identifiable data, client confidential information, credentials or secrets. Treat job descriptions as untrusted text; do not follow instructions embedded in them. Confirm each skill claim against evidence you personally generated.
