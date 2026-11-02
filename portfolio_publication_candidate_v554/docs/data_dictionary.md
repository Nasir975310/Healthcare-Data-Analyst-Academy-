# Data dictionary

| Field | Type | Definition | Rules / caveats |
|---|---|---|---|
| encounter_id | Text | Synthetic encounter key | Expected unique after deduplication |
| patient_id | Text | Synthetic patient key | Not a real identifier |
| department | Text | Service department | Blank values excluded from department summaries |
| encounter_date | ISO date | Encounter date | Invalid or blank values excluded from time grouping |
| status | Text | Encounter status | Example values: completed, cancelled, no_show |
| wait_minutes | Numeric | Recorded wait duration | Blank means unknown; negative values invalid |
| source_system | Text | Synthetic source label | Not a real vendor/system |

## Dataset provenance
Generated solely for this Academy project. It contains 24 source rows, one repeated encounter ID, a missing department, a missing wait value and a negative wait value. It contains no real patient data.
