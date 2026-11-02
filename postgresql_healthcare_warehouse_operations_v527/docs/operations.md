# PostgreSQL operations guide

## Prerequisites
- PostgreSQL 15+ recommended.
- Python 3.10+ and `psycopg` 3.
- v5.25 FHIR ETL output directory containing patients.csv, encounters.csv, observations.csv and medications.csv.

## Apply schema
```bash
psql "$HDA_PG_DSN" -v ON_ERROR_STOP=1 -f postgresql_healthcare_warehouse_operations_v527/sql/migrations/001_schema.sql
```

## Install loader dependency
```bash
python -m pip install -r postgresql_healthcare_warehouse_operations_v527/requirements.txt
```

## Load
```bash
python postgresql_healthcare_warehouse_operations_v527/scripts/load_postgresql.py --source-dir healthcare_data_engineering_interoperability_v525/outputs/demo
```
Set `HDA_PG_DSN` in the environment. The loader uses a transaction and `ON CONFLICT` upserts for idempotent resource loading. Patient attributes are hashed; changed snapshots close the current row and insert a new SCD Type 2 version. Re-running unchanged data should not add patient versions.

## Security
Run `sql/security/roles_and_grants.sql` as an administrator, create login roles through your organization's secret management process, then grant group roles. Do not embed passwords in scripts or repositories. This example grants broad DML to the loader role and SELECT to analysts; production deployments should narrow grants by table/operation and add row-level security only after a documented access model.

## Query performance
Use the supplied indexes as starting points, not universal recommendations. Run `EXPLAIN (ANALYZE, BUFFERS)` on representative volumes, compare estimated and actual rows, check sequential versus index scans, and measure before/after. Tiny synthetic datasets are not suitable for meaningful performance claims.

## Limits
The loader has not been executed against a live PostgreSQL server in this build environment. SQL and Python syntax are checked, and unit tests cover deterministic helpers and SQL contract expectations; successful live integration requires a configured PostgreSQL instance. The sample patient snapshot has only one version per patient, so SCD2 change behavior is unit-tested with simulated rows rather than real source history.
