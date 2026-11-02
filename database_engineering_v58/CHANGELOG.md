# v5.8.0 — Healthcare Analytics Database Engineering & SQL Production Lab

- Added executable SQLite operational and dimensional models with primary/foreign keys, unique and check constraints.
- Added 3NF-style operational tables and an encounter-grain star schema with date and department dimensions.
- Added synthetic 60-encounter/30-patient fixture generation and reproducible local runner.
- Added transaction rollback and constraint-failure checks.
- Added index/query-plan comparison, department views, monthly aggregation and LAG window-function analysis.
- Added PostgreSQL schema, analytics and performance SQL scripts plus optional localhost-only Docker Compose.
- Added model grain documentation, SQL production patterns and learning checkpoints.
- SQLite runner and query outputs executed and tested. PostgreSQL scripts are provided but were not executed against a PostgreSQL server.
