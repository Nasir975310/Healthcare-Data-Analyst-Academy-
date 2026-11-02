# Clinical Medication Utilization Case Study (v5.46)

## Purpose
A reproducible portfolio exercise analysing antihypertensive regimen patterns and paired blood-pressure measurements using synthetic data. This is not your Pharm.D thesis dataset.

## Run
Requires Python 3.10+; standard library only. From this directory:

```bash
python src/run_analysis.py
python -m unittest discover -s tests -v
```

Outputs are written to `outputs/`: summary JSON, drug-class CSV and SQLite database. Generated outputs are intentionally excluded from source publication bundles.

## Dataset
`data/synthetic_hypertension_records.csv` contains 301 rows representing 300 unique synthetic record IDs. It includes deliberate quality issues: one duplicate ID, missing follow-up SBP/DBP values, one implausible follow-up SBP, and one missing primary drug class. The pipeline logs these issues and excludes or nulls values according to documented rules.

## Analysis boundaries
- This is a synthetic educational dataset, not patient-level evidence.
- Drug classes are descriptive; there is no treatment-effect comparison or causal inference.
- Adherence categories are simulated and not validated measures.
- The `<140/90 mmHg` flag is an illustrative operational convention only, not an individualized clinical target or treatment recommendation.
- Do not use this output for diagnosis, prescribing, quality accreditation or clinical decisions.

## Portfolio tasks
1. Explain the grain and primary key.
2. Reconcile raw rows, unique IDs, excluded rows and paired SBP rows.
3. Run all four SQL queries in `sql/analysis_queries.sql`.
4. Compare mean paired SBP change by drug class without claiming comparative efficacy.
5. Discuss missingness, outlier handling, selection bias and limitations.
6. Produce a one-page stakeholder summary with methods, results, limitations and next steps.

## Structure
- `data/`: source synthetic CSV
- `sql/`: SQLite schema and analysis queries
- `src/`: reproducible analysis pipeline
- `tests/`: automated checks
- `outputs/`: generated artifacts; not for source release
- `docs/`: data dictionary, metric contract, assignment and interpretation guide
