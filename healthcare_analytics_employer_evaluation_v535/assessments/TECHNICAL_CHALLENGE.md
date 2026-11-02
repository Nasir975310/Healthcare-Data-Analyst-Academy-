# Healthcare Data Analyst — Timed Technical Challenge

**Time:** 120 minutes. **Data:** fictional/synthetic v5.32 practicum only.

## Scenario
A fictional teaching hospital requests an operational review of encounter activity and medication-order mix. The source has 91 encounter rows; one encounter refers to an unknown patient. Produce reliable descriptive analysis, not clinical conclusions.

## Part A — Data and SQL (30 points)
1. Report source, accepted and rejected encounter counts. Explain the rejection rule.
2. Write SQL for monthly encounter counts and unique patients.
3. Write SQL for encounter counts by type and status.
4. Identify duplicate encounter IDs and orphan patient references.
5. Explain why joining encounter and medication facts can inflate encounter counts.

## Part B — Python and validation (25 points)
1. Load a CSV with explicit dtypes where appropriate.
2. Validate required columns, key uniqueness and referential integrity.
3. Reconcile raw = accepted + rejected.
4. Produce a compact quality report with issue counts and examples.
5. Explain how your pipeline behaves on rerun.

## Part C — BI and KPI logic (20 points)
1. Define encounter count, unique patients and average encounters per patient.
2. Explain model grain and relationship direction.
3. Describe a dashboard page for operational monitoring.
4. Explain how you would reconcile DAX to SQL.
5. State what medication-order metrics do and do not mean.

## Part D — Communication and governance (25 points)
1. Write a one-page findings memo with period, denominator and limitations.
2. Explain the orphan encounter and remediation options.
3. Identify three privacy/security controls before publication.
4. Give three operational recommendations supported by the data.
5. Present the project in five minutes.

## Submission
`answers.sql`, `analysis.py` or notebook, `quality_report.json`, `findings_memo.md`, dashboard screenshot or clearly labelled specification, `limitations.md`, reproduction commands and environment details.
