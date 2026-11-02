# Take-home challenge: outpatient service operations

**Timebox:** 120 minutes. **Dataset:** synthetic teaching records only. **Deliverables:** SQL query, Python script/notebook, one-page findings memo, QA notes.

## Scenario
A clinic operations manager wants a weekly view of outpatient encounters. The extract contains encounter ID, patient ID, department, encounter date, status, wait minutes and a source-system flag. Some rows may be duplicated, cancelled or incomplete.

## Tasks
1. Define the analysis grain and inclusion/exclusion rules.
2. Profile missingness, duplicates, invalid wait times and status distribution.
3. Produce weekly encounter volume by department and median wait among eligible completed encounters.
4. Explain how you would avoid counting duplicate encounters and how you would handle missing department/date.
5. Write three QA checks with expected behavior.
6. Create a short memo with two evidence-backed observations, one limitation and one operational question for the manager.
7. Explain why wait-time association does not establish causation or service quality by itself.

## Submission contract
- `analysis.sql` — readable SQL, explicit filters and denominator.
- `analysis.py` or notebook — reproducible cleaning and summary.
- `findings.md` — no unsupported causal or clinical claims.
- `qa.md` — row counts before/after, rejected records and test results.
- `README.md` — environment, run commands, data provenance and limitations.

## Scoring (100 points)
| Domain | Points |
|---|---:|
| Grain, cohort and metric definitions | 15 |
| SQL correctness and readability | 20 |
| Python reproducibility and validation | 20 |
| QA, exceptions and reconciliation | 15 |
| Interpretation and limitations | 15 |
| Communication and handover | 10 |
| Privacy and data provenance | 5 |

Automatic review failure: real patient data exposed, fabricated results, concealed exclusions or unsupported claims of deployment.
