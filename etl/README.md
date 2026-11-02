# Healthcare ETL laboratory

Start with `DATA_CONTRACTS.md` and `PIPELINE_ARCHITECTURE.md`.

## Quick run
From the Academy root:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-etl.txt
python scripts/healthcare_etl_pipeline.py --source csv
```
Fish:
```fish
source .venv/bin/activate.fish
```
Mock paginated API:
```bash
python scripts/healthcare_etl_pipeline.py --source mock-api
```
Output:
- `assignments/outputs/healthcare_etl_training.db`
- `assignments/outputs/etl_runs/` — logs, manifests and quality CSVs

Open the database in DBeaver or SQLite. Run `sql/healthcare_etl/etl_audit_queries.sql`.

The mock API is local JSON fixtures; it makes no network requests. The generic REST extractor is a template requiring a real API contract and approved access.
