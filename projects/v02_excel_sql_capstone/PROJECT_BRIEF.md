# Integrated Excel–SQL Healthcare Analytics Portfolio Project

## Scenario
You are a junior healthcare data analyst asked to prepare a descriptive operational summary for a fictional teaching hospital. The source is the academy's synthetic SQLite database. Your task is to create a traceable extract, reconcile it, analyze it and communicate limitations.

## Scope and assumptions
- Reporting window: 1 January 2026 through 31 March 2026 inclusive.
- Primary grain: one row per encounter.
- Patient counts must use distinct patient identifiers.
- All included data is synthetic; no real patient data is present.
- This is a descriptive exercise, not a clinical audit or validated hospital performance report.

## Required workflow
1. Inspect the schema and data dictionary. Record the grain of every table.
2. Define the cohort with a half-open date interval: admission_date >= '2026-01-01' AND admission_date < '2026-04-01'.
3. Run the SQL in `capstone_analysis_queries.sql` and save the SQL script with your submission.
4. Export the query outputs from DBeaver as CSV files. Record the extraction timestamp and source database version.
5. Open `healthcare_excel_sql_capstone_workbook.xlsx`. Use its source sheets and report template to reconcile counts and create a concise dashboard/report.
6. Verify every KPI's numerator, denominator, eligibility rules and missing-data handling.
7. Write a 400–700 word interpretation with at least three findings, two limitations and one data-quality recommendation.

## Required deliverables
- Saved SQL script with comments and documented date window.
- Completed `Report_Template` sheet.
- Completed `Data_Quality_Log` sheet.
- One summary chart (encounter type or department) and one data-quality visualization.
- Short narrative with scope, findings, limitations and recommendations.
- A README describing how the work can be reproduced.

## KPI definitions
- Encounter volume: encounter rows in the selected date window.
- Unique patients: distinct patient_id values among those encounter rows.
- IPD share: IPD encounter rows divided by all encounter rows in the selected period.
- Mean SBP: mean of non-NULL SBP values; report nonmissing n and missing n.
- SBP completeness: nonmissing SBP encounter rows divided by all encounter rows.
- Mean inpatient LOS: mean LOS among IPD encounter rows only; exclude OPD zero placeholders.
- Readmission status proportion: recorded readmissions divided by IPD encounters with known readmitted_30d status. This synthetic field is not a validated readmission indicator.

## Quality-control gates
- Unique encounter count equals encounter row count for the cohort.
- Unique patient count does not exceed encounter count.
- Department totals reconcile to the cohort encounter total.
- Missing SBP count + nonmissing SBP count = cohort encounter count.
- No unexpected row multiplication after joins.
- Child-table counts are not summed after raw multi-child joins without controlling fan-out.
- Every reported percentage shows its denominator.
- The narrative distinguishes observed description from causal explanation.

## Portfolio presentation
Publish only the synthetic dataset, your SQL, your workbook and your own narrative. Include a short project summary, tools used, key methods, QA checks and limitations. Never upload real patient data, institutional extracts, screenshots containing identifiers or confidential source files to a public portfolio.
