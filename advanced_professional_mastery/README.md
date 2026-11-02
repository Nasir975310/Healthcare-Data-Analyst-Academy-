# Advanced Professional Mastery — v3.8

All data are synthetic and generated for training.

## Dataset inventory
- `data/encounters_5000.csv`: 5,000 encounter-grain rows.
- `data/medication_orders_20000.csv`: 20,000 medication-order rows, including 540 orphan encounter references and several intentional field-quality issues.
- `data/lab_observations_15000.csv`: 15,000 clinical-observation rows.
- `data/observational_sbp_cohort.csv`: 1,200 synthetic observational cohort rows, including missing follow-up SBP and one implausible age.
- `data/dashboard_cards_flawed.csv`: deliberately flawed dashboard cards for reconciliation practice.
- `data/advanced_healthcare_analytics.db`: ready-to-query SQLite database with encounters, medication_orders and lab_observations.

## Advanced SQL
`sql/advanced_investigation.sql` contains 12 investigations using CTEs, anti-joins, window functions, date grouping, safe pre-aggregation, data-quality checks and query plans. SQLite 3.35+ is recommended.

## Statistical validation
Install dependencies from `requirements.txt`, then run:
```bash
python advanced_professional_mastery/solutions/statistical_validation.py
```
The analysis compares crude and adjusted observational associations using HC3 robust standard errors. Adjustment does not establish causality.

## Dashboard review
Use `assignments/dashboard_review.md` and `data/dashboard_cards_flawed.csv`. Recompute metrics from raw tables and document grain, denominator, join fan-out and orphan handling.

## Recommended sequence
1. SQL-ADV-01 to SQL-ADV-12.
2. STAT-ADV-01.
3. DASH-ADV-01.
4. Advanced mastery examination.
5. Rerun all analyses from a clean output folder and write an executive handoff.

Reference outputs are provided for checking after your first attempt. Never publish synthetic outputs as real hospital or clinical evidence.
