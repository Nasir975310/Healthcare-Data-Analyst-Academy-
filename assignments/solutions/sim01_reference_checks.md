# SIM-01 reference checks (open after completing the assignment)

These are checks against the supplied synthetic dataset, not clinical benchmarks.

## Overall encounter metrics
- Encounter rows: 80
- Unique encounter IDs: 80
- Mean length of stay: 3.875 days (round to 3.88 days)
- Encounters with `readmission_30d_flag = 1`: 7
- Flagged proportion: 8.75% (7 / 80 = 8.75%)

## Encounter summary by department

| Department | Encounters | Mean LOS (days) |
|---|---:|---:|
| Cardiology | 14 | 4.21 |
| Emergency | 24 | 3.75 |
| General Medicine | 15 | 3.60 |
| Neurology | 13 | 3.69 |
| Orthopaedics | 14 | 4.21 |

## Medication orders by therapeutic class and status

| Therapeutic class | Active | Completed | Discontinued |
|---|---:|---:|---:|
| ACE inhibitor | 9 | 8 | 6 |
| ARB | 9 | 6 | 6 |
| Antidiabetic | 7 | 8 | 6 |
| Beta blocker | 5 | 9 | 4 |
| Calcium-channel blocker | 9 | 6 | 12 |
| Diuretic | 6 | 8 | 1 |
| Statin | 5 | 7 | 13 |

## Interpretation cautions
- The readmission flag is a synthetic field with no validated derivation or follow-up protocol. Report it only as a supplied flag.
- The data do not establish all-cause unplanned readmission, eligibility, complete 30-day follow-up or causal effects.
- Medication rows are orders. They are not dispensing, administration or adherence events.
- Mean LOS is descriptive; assess the distribution and context before making operational recommendations.
