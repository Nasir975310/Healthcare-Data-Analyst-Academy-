# Integrated Healthcare Analytics Portfolio — Project Brief

## Scenario
You are a junior healthcare data analyst preparing a descriptive operational report for a fictional teaching hospital. The source records are synthetic and were created for this Academy.

## Business question
What does the first-quarter 2026 encounter dataset show about encounter volume, distinct patients, department distribution and completeness of recorded systolic blood pressure (SBP)?

## Scope and definitions
- Reporting period: 1 January 2026 inclusive to 1 April 2026 exclusive.
- Analysis grain: one row per encounter.
- Encounter count: number of eligible encounter records after confirming unique encounter IDs.
- Distinct patients: count of unique patient IDs; one patient may have multiple encounters.
- SBP completeness: nonmissing SBP records divided by all eligible encounter records, multiplied by 100.
- Mean and median SBP: calculated from nonmissing values only; show the nonmissing denominator.
- Department join: encounter.department_id to department.department_id; expected many-to-one relationship.

## Required workflow
1. Profile source data and verify table grain.
2. Validate required columns, keys, date parsing and missingness.
3. Filter the reporting period using a half-open date interval.
4. Join the department lookup and verify row-count preservation.
5. Produce grouped metrics in Python and independently in R.
6. Reconcile totals against the SQL reference.
7. Create a report with charts, interpretation, limitations and provenance.
8. Run automated tests and preserve QA evidence.

## Required deliverables
- Python CLI pipeline and automated tests.
- R summary and visualization scripts.
- SQL reference query file.
- Quarto report source and rendered report (HTML render is learner task).
- Summary CSV/JSON, charts and QA log.
- README with environment setup and exact run commands.
- Handoff note and short portfolio presentation.

## Acceptance criteria
- All 104 source encounter IDs are unique.
- Reporting cohort and date boundaries are consistent in each tool.
- Department lookup key is unique and join preserves cohort row count.
- SBP missingness is reported, never silently replaced with zero.
- Department totals sum to cohort encounter count.
- Python tests pass.
- Python/R/SQL differences are investigated and documented.
- Report clearly distinguishes descriptive observations from causal or clinical claims.
- No real patient information, credentials or confidential source data are included.

## Portfolio safety
Only the Academy's fictional data may be used in a public portfolio. Never publish real patient records or institutional extracts without explicit authorization and approved governance.
