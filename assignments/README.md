# Job simulation assignments

All records in `data/` are synthetic and created for this Academy. They do not describe real patients or a real hospital.

## Assignments
- SIM-01: Excel hospital operations review.
- SIM-02: SQL prescribing and encounter analysis.
- SIM-03: ambiguous client request through final analytical handoff.

## Suggested order
Complete SIM-01, then SIM-02, then SIM-03. SIM-03 reuses the same data and expects you to apply both Excel and SQL reasoning.

## Important interpretation boundaries
- Encounter table grain: one row per synthetic encounter.
- Medication table grain: one row per synthetic medication order.
- A medication order is not proof of dispensing, administration or adherence.
- The synthetic 30-day readmission flag is not a validated quality measure.
- These exercises do not support clinical decisions or causal conclusions.

## SQL
Import the CSV files into a local SQLite database with DBeaver. Use `starter/analysis_starter.sql`; compare your work with `solutions/sim02_solution.sql` only after attempting the tasks.


## Reference solutions
- `solutions/sim01_reference_checks.md` contains numeric reconciliation checks for SIM-01. Attempt the work before opening it.
- `solutions/sim02_solution.sql` contains one valid SQLite solution for SIM-02. Alternative correct queries are acceptable if grain and results are preserved.
