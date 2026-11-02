# v5.20.0 — Healthcare Analytics Integrated Execution Engine

Adds local execution for trusted Python scripts, CSV-to-SQLite loading, read-only SQL queries, and declarative CSV transformations.

## Commands

```bash
# Execute a trusted project Python script with timeout and captured logs
python scripts/execution_engine.py run-python --project ./my_project --script src/python/analysis.py --timeout 120

# Load a CSV as TEXT columns into the project's SQLite database
python scripts/execution_engine.py load-csv --project ./my_project --input data/raw/encounters.csv --table encounters

# Run one read-only SELECT/WITH query and save results as CSV
python scripts/execution_engine.py query-sql --project ./my_project --sql "SELECT service_line, COUNT(*) AS n FROM encounters GROUP BY service_line" --output service_line_counts.csv

# Run supported declarative pipeline steps from JSON
python scripts/execution_engine.py run-pipeline --project ./my_project --config pipeline.json

# Inspect recorded Python runs
python scripts/execution_engine.py runs --project ./my_project
```

## Pipeline operations
`drop_duplicates` (requires `key`), `filter_equals` (`column`, `value`), `rename` (`from`, `to`), and `select_columns` (`columns`). Unknown operations fail closed.

## Safety and technical boundaries
- Python execution runs local code with the current interpreter and user permissions. Execute only trusted scripts; timeout is not a security sandbox.
- SQLite import stores values as TEXT; define explicit casts and validation in analysis SQL when required.
- SQL interface allows one SELECT/WITH statement, uses SQLite read-only mode and a mutation-denying authorizer, and caps returned rows at 100,000.
- CSV pipeline supports only the documented transformations; it is not a general-purpose ETL engine.
- Python run logs and metadata are local records, not tamper-proof audit trails.
- PostgreSQL and DAX/Power Query are not executed by this release.
