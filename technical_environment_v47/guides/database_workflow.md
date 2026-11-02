# Database workflow: SQLite first, PostgreSQL second

## SQLite (no server required)
From `starter_project` with the venv active:
```bash
python scripts/load_sqlite.py
```
Open `data/health_analytics.sqlite` using DBeaver or the SQLite extension in VS Code. Run `sql/starter_queries.sql` after selecting/importing the `encounters` table. The loader recreates table contents on each run from the bundled synthetic CSV.

## PostgreSQL (optional)
Start the local service using Docker Compose. Connect from DBeaver:
- Host: `127.0.0.1`
- Port: `5432`
- Database: `healthcare_training`
- Username: `analyst`
- Password: `local_training_only_change_me` (training only)

The database starts empty. Import the CSV using DBeaver's import wizard, or write an explicit ETL loader. Verify row counts and key uniqueness after import. Stop it with `docker compose down`; preserve data with the named volume, or remove the volume only when intentionally resetting training data.

## Data engineering discipline
Keep source files immutable. Record dataset grain, primary key, timestamp semantics, units, allowed values and missing-value meaning. Test joins for row multiplication and orphan keys. Separate exploratory output from validated reporting.
