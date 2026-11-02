# Synthetic Hospital Encounter Analytics

**Reporting period:** 1 January 2026 inclusive to 1 April 2026 exclusive  
**Analysis grain:** one row per encounter  
**Source:** `datasets/v03_python/encounters.csv` and `departments.csv`  
**Status:** Generated from the executed Python pipeline

## Executive summary

The reporting cohort contains **104 encounters** and **60 distinct synthetic patients**. Of the encounter records, **96** have recorded systolic blood pressure (SBP) and **8** have missing SBP. All department keys matched, and department encounter totals reconcile to the cohort total.

These are descriptive results from a small fictional dataset. They do not describe a real hospital or support clinical conclusions.

## Data-quality checks

| Check | Result |
|---|---:|
| Source encounter rows | 104 |
| Unique encounter IDs | 104 |
| Cohort encounters | 104 |
| Distinct patients | 60 |
| Nonmissing SBP | 96 |
| Missing SBP | 8 |
| Unmatched department keys | 0 |
| Department total | 104 |

## Department summary

| department_name   |   encounter_n |   unique_patients |   sbp_nonmissing_n |   mean_sbp |   median_sbp |   sbp_missing_n |   sbp_completeness_pct |
|:------------------|--------------:|------------------:|-------------------:|-----------:|-------------:|----------------:|-----------------------:|
| Cardiology        |            14 |                14 |                 14 |     140.04 |       139.25 |               0 |                 100    |
| Emergency         |            19 |                18 |                 17 |     137.75 |       138.7  |               2 |                  89.47 |
| Endocrinology     |            16 |                15 |                 14 |     141.7  |       139.2  |               2 |                  87.5  |
| General Medicine  |            41 |                31 |                 38 |     145.97 |       146.6  |               3 |                  92.68 |
| Nephrology        |            14 |                13 |                 13 |     142.2  |       134.6  |               1 |                  92.86 |

Mean and median SBP use nonmissing SBP values only. Completeness uses all encounter rows in the department as the denominator. Unique patients are not additive across departments if a patient attends more than one department.

## Interpretation

- General Medicine has the largest encounter count in this synthetic cohort (41).
- Cardiology has complete SBP recording in this generated sample (14 of 14); other departments have some missing SBP values.
- Department mean SBP values are descriptive summaries only. They are not a basis for ranking departments or judging quality.
- Encounter rows are not independent patient observations because patients may have repeated encounters.

## Limitations

- The data are synthetic, small and generated for software training.
- SBP missingness may not be random; this report does not model the missingness mechanism.
- No causal inference or treatment-effect analysis is justified.
- The data are not suitable for clinical decision-making, model training or real-world hospital benchmarking.

## Reproducibility

The pipeline source is `automation/healthcare_pipeline.py`. It uses a half-open date interval and validates encounter uniqueness and many-to-one department joins. Run instructions and automated tests are in `README.md`. Software and package versions should be recorded at the time the learner reruns the project.
