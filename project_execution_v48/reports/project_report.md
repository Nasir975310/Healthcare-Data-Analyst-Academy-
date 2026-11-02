# Hospital Encounter Analytics — Training Report

> Synthetic training dataset. Not real hospital performance or clinical evidence.

## Data pipeline summary
- Raw records: 241
- Accepted records: 231
- Quarantined records: 10
- Acceptance rate: 95.85%
- SQLite row count: 231

## Non-exclusive quality issue counts
| Rule | Rows flagged |
|---|---:|
| missing_encounter_id | 0 |
| duplicate_encounter_id | 1 |
| missing_patient_token | 1 |
| invalid_date | 2 |
| invalid_department | 2 |
| invalid_length_of_stay | 2 |
| invalid_disposition | 1 |
| invalid_age_band | 1 |

Issue counts are non-exclusive: one row may violate multiple rules.

## Department summary
| department       |   encounters |   mean_los_days |
|:-----------------|-------------:|----------------:|
| Orthopaedics     |           49 |            4.88 |
| Neurology        |           48 |            3.77 |
| Pulmonology      |           46 |            4.33 |
| Cardiology       |           46 |            4.74 |
| General Medicine |           42 |            3.86 |

## Discharge disposition summary
| discharge_disposition   |   encounters |
|:------------------------|-------------:|
| Referred                |           64 |
| Home                    |           60 |
| Expired                 |           54 |
| Transfer                |           53 |

## Limitations
- All records are fictional and generated for learning.
- Quarantined records are excluded, not automatically repaired.
- The descriptive summaries are not risk-adjusted and do not establish causality.
- Validate definitions and business rules with an authorised data owner before real use.