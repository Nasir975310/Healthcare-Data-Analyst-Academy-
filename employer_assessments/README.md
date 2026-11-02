# Employer-Style Technical Assessments — v3.1.0

## Included
- Five hiring simulations: SQL, Python/data quality, Excel, dashboard review and remote client communication.
- Three synthetic datasets: 300 encounter records, 800 medication-order rows and 100 data-quality issue examples.
- Seven SQLite-compatible SQL reference queries and a pandas QA reference script.
- Portfolio review scorecard and mock interview rubric.
- Eight additional employer-assessment challenges, with local completion tracking integrated into full Academy backup export/import.

## Run the Python reference
From the Academy root:
```bash
python -m pip install -r employer_assessments/solutions/requirements.txt
python employer_assessments/solutions/qa_assessment.py
```
Add `--fail-on-orphans` to return exit code 2 when orphan order references are present. The default run exports a QA issue log and summary while preserving source extracts.

## Dataset facts
- 300 unique encounter IDs.
- 800 unique medication-order IDs.
- 41 intentionally orphan medication-order references.
- The orphan references are synthetic QA defects, not real operational data.

## Assessment integrity
The browser module presents scenarios, time limits, deliverables and rubrics; it does not execute Excel, SQL or Python in-browser. Use local tools. Reference solutions are supplied for learning after attempting the task. For a realistic timed assessment, attempt the brief first, save your work, then compare against reference methods.

## Privacy and interpretation
All records are synthetic. Medication orders do not establish administration, dispensing or adherence. A supplied readmission flag is not automatically a validated readmission rate. Do not publish patient-identifiable or confidential employer data.
