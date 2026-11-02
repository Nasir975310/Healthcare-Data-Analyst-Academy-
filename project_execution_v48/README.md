# v4.8.0 — Practical Project Execution Engine

A complete, runnable end-to-end healthcare analytics assignment using a fictional hospital encounter dataset with planted data-quality issues.

## Run from this directory
Create/activate a Python virtual environment and install `pandas`, `matplotlib`, `pytest` (or reuse the v4.7 starter environment). Then:

```bash
python -m pip install pandas matplotlib pytest
python run_project.py
python -m pytest -q
```

The pipeline profiles raw data, validates rules, quarantines invalid rows, cleans valid rows, loads SQLite, executes SQL summaries, generates a Markdown report and a PNG chart.

## Outputs
- `data/processed/clean_encounters.csv`
- `data/quarantine/quarantined_encounters.csv`
- `data/processed/quality_report.json`
- `data/processed/department_summary.csv`
- `data/processed/disposition_summary.csv`
- `data/processed/hospital_analytics.sqlite`
- `reports/project_report.md`
- `reports/department_encounters.png`

## Important
The dataset is synthetic and contains deliberately planted errors for training. The results are not real hospital performance, clinical evidence or operational benchmarks. The pipeline is educational, not a production ETL system.
