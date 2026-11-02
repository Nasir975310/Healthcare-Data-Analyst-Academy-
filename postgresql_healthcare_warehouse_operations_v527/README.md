# PostgreSQL Healthcare Warehouse Operations — v5.27.0

A PostgreSQL-native continuation of the v5.26 SQLite warehouse. Includes a PostgreSQL schema migration, psycopg 3 loader, idempotent fact/dimension upserts, patient SCD Type 2 versioning, analytical SQL, index examples and role/grant templates.

1. Run v5.25 FHIR ETL to create `healthcare_data_engineering_interoperability_v525/outputs/demo`.
2. Configure PostgreSQL and `HDA_PG_DSN`.
3. Apply `sql/migrations/001_schema.sql`.
4. Install `requirements.txt`.
5. Run `scripts/load_postgresql.py --source-dir healthcare_data_engineering_interoperability_v525/outputs/demo`.

See `docs/operations.md`. Live PostgreSQL integration was not available for this release; do not interpret syntax and unit checks as a live database test. Synthetic records only.
