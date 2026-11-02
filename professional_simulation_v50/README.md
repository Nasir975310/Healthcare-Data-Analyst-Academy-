# Healthcare Analytics Professional Simulation — v5.0.0

A unified capstone assessment with four employer-style scenarios, transparent scoring rubrics, model answers, a synthetic SQLite fixture, and a Python QA script.

## Run
From the Academy root:

```bash
python -m pip install pandas
python professional_simulation_v50/python/analyse_fixture.py
```

Fish/Linux and Bash:
```bash
sqlite3 professional_simulation_v50/fixtures/training.db < professional_simulation_v50/sql/reference_queries.sql
```
Create the database first:
```bash
sqlite3 professional_simulation_v50/fixtures/training.db
.mode csv
.import professional_simulation_v50/fixtures/encounters.csv encounters
.quit
```
Windows PowerShell uses the same Python command if Python is on PATH. For SQLite, install SQLite CLI or use DB Browser for SQLite/DBeaver: create a database, import the CSV, then execute `sql/reference_queries.sql`.

Expected SQL result for first query: 3 unique patients (P001, P002, P004, P005 = 4; note P001 appears in two encounters but only one active order; correct result is 4). The department summary should be interpreted at patient level.

All fixture records are synthetic. The browser app stores progress locally; it does not execute SQL/Python or transmit data.
