# v4.3 Practicum — synthetic client engagements

Five realistic healthcare analytics engagements with briefs, synthetic data, deliverable requirements, acceptance criteria and a 100-point reviewer rubric.

Start at `briefs/`. Work on copies of files; retain immutable raw data. Put your own scripts, SQL, workbooks, dashboard exports and reports in a separate project folder. The supplied CSVs are synthetic and are not clinical source data. Do not upload PHI.

The browser tracker records status and self-ratings locally. It cannot inspect your local project files, execute SQL/Python, or verify evidence. A self-score is not reviewer approval. Use the rubric and handoff template for an independent review.


## Load the practicum data into SQLite
Install pandas if needed, then run:
```bash
python starter/load_practicum_sqlite.py
```
This creates `practicum_training.sqlite` in this folder and loads four tables. The database is generated locally; it is not included as a prebuilt binary. A SQL starter is in `starter/join_fanout_investigation.sql`.
