# Release 2.1.0 — Healthcare SQL Mastery

## Added
- Searchable Healthcare SQL Mastery section with 11 progressive challenges.
- Topics: table grain, SELECT, filtering, aggregation, HAVING, INNER/LEFT JOIN, join cardinality, CTEs, window functions, healthcare metric denominators, data-quality checks and EXPLAIN QUERY PLAN.
- Starter query, optional hint, revealable worked solution, expected result and validation explanation per challenge.
- Browser-local challenge completion tracker.
- Ready-to-query SQLite database with 80 synthetic encounter records and 150 synthetic medication-order records.
- Printable challenge and solution SQL files plus setup README.

## Validation
All reference queries were executed against the packaged SQLite database. The supplied keys are unique; 70 encounters have at least one order and 10 have none. The synthetic readmission flag proportion is 7/80 (8.75%).

## Limitations
- The data and readmission flag are synthetic teaching materials.
- SQLite is the training dialect; PostgreSQL, SQL Server and BigQuery have dialect-specific differences.
- Browser UI does not execute SQL; use DBeaver or SQLite CLI.
- Completion tracking uses local browser storage and does not cloud-sync.
