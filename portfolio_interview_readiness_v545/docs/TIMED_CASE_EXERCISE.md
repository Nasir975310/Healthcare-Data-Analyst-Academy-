# Timed case exercise — outpatient waiting-time review

**Time limit:** 45 minutes. **Dataset:** `github_portfolio_publication_v542/sample_export/data/synthetic_outpatient_encounters.csv`. All records are fictional.

## Scenario
An operations manager reports that one department has “unacceptably long waits” and asks for a ranking and a staffing recommendation by the end of the day.

## Tasks
1. **0–8 min:** Inspect schema, row grain, duplicate keys, nulls, status values and invalid wait times. Record row counts before and after each filter.
2. **8–18 min:** Write SQL to report eligible encounter count, valid wait count, mean and median wait by department. If median is unavailable in the SQL engine, state how you would calculate it safely.
3. **18–28 min:** Validate the SQL output against an independent Python calculation. Explain any discrepancy.
4. **28–38 min:** Draft a 150-word manager update: findings, denominator, caveats and next validation step.
5. **38–45 min:** Give a recommendation that avoids causal overreach and specify what additional data are needed.

## Scoring (20 points)
- Grain, data quality and denominator (0–5)
- Correct SQL and aggregation (0–5)
- Independent validation and reproducibility (0–4)
- Clear stakeholder communication (0–3)
- Limitations, privacy and decision safety (0–3)

**Pass for practice:** 15/20, with no zero in denominator, validation or decision safety. This is an internal practice threshold, not an employer standard.

## Expected deliverable
A short analysis note, SQL file, validation evidence and manager update. Do not use the sample's reference results as a substitute for running your own analysis.
