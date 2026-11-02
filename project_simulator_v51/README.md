# Interactive Healthcare Analytics Project Simulator — v5.1.0

## Project
A synthetic hospital operations engagement with evolving client requirements, an imperfect encounter dataset, an auditable Python cleaning pipeline, SQL summaries and client handoff guidance.

## Run the Python pipeline
From the Academy root:

```bash
python -m pip install pandas
python project_simulator_v51/scripts/run_engagement.py
```

On Windows PowerShell, use `py` instead of `python` if the launcher is configured.

Outputs are written to `project_simulator_v51/output/`:
- `qa_audit_all_rows.csv`
- `encounters_accepted.csv`
- `encounters_quarantine.csv`
- `department_summary_ex_emergency.csv`
- `disposition_mix.csv`
- `engagement_summary.json`
- `qa_log.md`

## SQL
Import `output/encounters_accepted.csv` into SQLite/DBeaver as `encounters_accepted`, preserving the column names, then execute `sql/engagement_queries.sql`. The browser does not execute SQL or Python.

## Expected logic
- Grain: encounter.
- Emergency remains in overall totals but is excluded from department comparison.
- LOS is calendar-day difference and is averaged for discharged encounters only.
- SBP completeness is nonmissing valid SBP among accepted reporting-period encounters; it is not BP control or clinical quality.
- Invalid keys, missing department/patient identifiers, invalid dates, invalid SBP and invalid order counts are quarantined with reason codes.

All records are synthetic. The rules are training assumptions and require data-owner agreement in real work.
