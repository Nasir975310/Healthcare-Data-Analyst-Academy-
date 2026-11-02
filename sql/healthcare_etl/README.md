# ETL audit SQL

Run these queries against the SQLite database created by `scripts/healthcare_etl_pipeline.py`.

```bash
sqlite3 assignments/outputs/healthcare_etl_training.db
```
Then execute `etl_audit_queries.sql` in SQLite or open the database in DBeaver.

The SQL file is read-only and audits run history, mart grain, quarantined records, quality findings and order summaries.
