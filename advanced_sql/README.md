# Advanced Healthcare SQL Interview Bank

20 progressive interview-style challenges using SQLite-compatible SQL and the bundled `healthcare_advanced_sql.db`.

## Run
```bash
sqlite3 healthcare_advanced_sql.db
.read reference_solutions.sql
```
Or open the database in DBeaver and execute individual statements. Search challenge IDs in `challenges.json` for scenario, task, solution and expected interpretation.

## Dataset
- 300 synthetic encounters; 150 distinct patient IDs (multiple encounters per patient).
- 800 synthetic medication order lines.
- 41 intentionally orphan order references.
- `readmission_30d_flag` is a supplied synthetic field, not a validated clinical outcome.
- Medication order rows are not administration, dispensing, adherence or ingestion evidence.

## Dialect notes
SQLite is the executable reference. PostgreSQL equivalents may use `FILTER`, `DATE_TRUNC`, `PERCENTILE_CONT`, `INTERVAL`, `EXPLAIN (ANALYZE, BUFFERS)` and different date arithmetic. Do not paste SQLite `julianday()` into PostgreSQL. `ROWS BETWEEN 6 PRECEDING` means seven ordered rows, not guaranteed seven calendar days when dates are missing.

## Interview standard
Explain table grain, denominator, NULL handling, join cardinality, time boundaries, data quality, assumptions and clinical interpretation. A query that runs but answers the wrong question is not a correct answer.
