# Healthcare Analytics Capstone v5.30

All records are synthetic and intentionally include one orphan encounter (PT999) to test data-quality handling. It is retained in staging and rejected from the curated fact table to preserve referential integrity. No real patient information is present.

## Run
From this module directory:
```bash
python src/run_capstone.py
python -m unittest discover -s tests -v
```
The runner creates `reports/capstone_warehouse.sqlite`, `capstone_results.json`, and `kpi_summary.csv`. It uses Python's standard library only.

## Grain and model
- `dim_patient`: one row per patient.
- `fact_encounter`: one row per encounter.
- `fact_observation`: one row per observation.
- `fact_medication`: one row per medication order.

Do not join the two child fact tables directly; aggregate each independently before combining by encounter to avoid fanout.

## Clinical interpretation boundary
Blood-pressure summaries are descriptive statistics on a small synthetic dataset. A threshold count is an analytical flag only; it is not a hypertension diagnosis, quality measure, or treatment recommendation.

## Capstone deliverables
1. Data profiling and quality report.
2. Normalized SQLite warehouse.
3. SQL analysis outputs.
4. KPI dictionary and dashboard wireframe.
5. Reproducible run instructions and limitations.
6. Client handover and assessment rubric.
