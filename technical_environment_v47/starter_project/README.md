# Healthcare Analytics Starter Project

A reproducible, synthetic-data-only project scaffold for Python, SQL and quality checks.

## Data
`data/raw/synthetic_encounters.csv` contains fictional encounter-level rows. It is not patient data and must not be used to infer real clinical outcomes.

## Run
Follow `../../guides/setup_linux.md` or `../../guides/setup_windows.md`. Then:

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
python scripts/load_sqlite.py\npython -m health_analytics.profile
```

Generated profile: `reports/generated/profile.json`.

## SQL
Import the CSV into SQLite/PostgreSQL as `encounters`, then run `sql/starter_queries.sql`. SQL dialects may require minor adjustments.

## Reproducibility
- Python dependencies are bounded in `pyproject.toml`; create a lock file when preparing a real deployment.
- Keep raw inputs immutable; write transformations to processed outputs.
- Record source, grain, units, definitions, exclusions and limitations.
- Add tests for row counts, keys, valid ranges and reconciliation.
- Never put credentials, PHI or confidential client data in Git.
