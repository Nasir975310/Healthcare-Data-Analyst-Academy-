# Dashboard Review Assignment — DASH-ADV-01

**Time:** 75 minutes · **Role:** Healthcare BI Analyst

## Scenario
A dashboard owner reports that the monthly dashboard differs from source extracts. Review `data/dashboard_cards_flawed.csv` and recompute all four metrics from the three raw tables.

## Tasks
1. Confirm encounter volume and distinct-patient count.
2. Reconcile raw medication orders with orders linked to known encounters; explicitly report orphan rows.
3. Compare mean length of stay from the encounter table with the value produced after joining encounter rows to medication orders.
4. Recompute the supplied synthetic 30-day flag rate at encounter grain.
5. Identify which cards are correct, misleading or incomplete and why.
6. Propose a corrected semantic model and a QA test for each metric.

## Deliverables
- Metric reconciliation table (dashboard value, recomputed value, difference, cause)
- Grain and relationship diagram
- Corrected metric definitions
- QA test plan
- Short executive explanation

## Acceptance
Do not remove orphan orders silently. Do not calculate encounter-level metrics from an unaggregated one-to-many join. Label the readmission-like flag as supplied and unvalidated.
