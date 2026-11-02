# Portfolio capstones and job readiness — v2.9.0

## Synthetic datasets
- `data/hospital_operations.csv`: 500 encounter-grain rows.
- `data/pharmacy_orders.csv`: 1,200 medication-order-line rows. Contains 36 intentionally orphan encounter references for data-quality review.
- `data/analytics_service_requests.csv`: 180 service-ticket rows.

All records are generated synthetic training data. They are not patient records, operational benchmarks or clinical evidence.

## Run the reference analysis
From the Academy root:
```bash
python -m pip install -r portfolio_career/scripts/requirements.txt
python portfolio_career/scripts/run_portfolio_capstone.py
```
Outputs are created in `portfolio_career/outputs/`: department metrics, pharmacy utilisation, service delivery, orphan review and quality summary.

## Included professional assets
- Three capstone briefs with deliverables and domain-specific critical cautions.
- Twelve professional execution challenges.
- Twelve interview questions with strong-answer guidance and common pitfalls.
- Project README and client handoff templates.
- Portfolio quality gate checklist.
- SQLite-compatible SQL reference queries.

## Important interpretation limits
- The supplied 30-day readmission flag is not independently validated; do not call its raw proportion a validated readmission rate.
- Medication order rows do not establish administration, dispensing or adherence.
- The 36 orphan order rows must be investigated; the reference script retains and reports them.
- Ticket turnaround is a synthetic service metric, not a clinical outcome.
- Use only synthetic or explicitly authorised data. Never publish PHI, confidential trial data, production identifiers, secrets or client information.
