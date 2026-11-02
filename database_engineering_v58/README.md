# v5.8.0 — Healthcare Analytics Database Engineering & SQL Production Lab

Hands-on database engineering: relational modelling, constraints, dimensional modelling, indexes, query plans, window functions, transactions, views, and migration exercises.

## Run the SQLite lab (no database server required)

### Linux (Ryoku / Arch)
```bash
python scripts/run_sqlite_lab.py --output-dir output
```

### Windows PowerShell
```powershell
py scripts\run_sqlite_lab.py --output-dir output
```

The runner builds a synthetic operational schema and a star-schema mart in SQLite, loads synthetic fixtures, executes analytical SQL, captures query plans, checks constraints/transactions, and writes a QA report. It is safe to rerun with a fresh output directory.

## PostgreSQL practice
Review and run scripts in `sql/postgresql/` against a PostgreSQL database you control. Optional Docker Compose is provided. PostgreSQL scripts are provided for real execution but were not executed in the release QA environment unless explicitly reported.

### Optional PostgreSQL with Docker
```bash
docker compose -f docker-compose.yml up -d
```
Connection defaults in compose are local educational credentials only. Change them before any non-local use. Never expose the database port publicly.

## Learning path
1. Relational schema and constraints
2. Transactional loading
3. Star schema and grain
4. Index design and EXPLAIN
5. Window functions and cohort-style summaries
6. Views, data quality constraints and migration planning

All data are synthetic. No clinical decision support, patient-level recommendations, or real hospital outcomes are represented.
