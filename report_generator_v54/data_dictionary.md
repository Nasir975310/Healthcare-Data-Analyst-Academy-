# Sample data dictionary

| Field | Meaning | Type | Notes |
|---|---|---|---|
| encounter_id | Synthetic encounter identifier | String | Not a real patient identifier |
| patient_id | Synthetic patient token | String | Repeated tokens may represent multiple encounters |
| department | Synthetic service/department | Category | Not an actual facility |
| admit_date | Synthetic admission date | Date | Source date field; validate parseability before period analysis |
| disposition | Synthetic encounter disposition | Category | Synthetic |
| los_days | Length of stay | Numeric | Descriptive only |
| order_count | Number of synthetic orders per encounter | Integer | Not a measure of prescribing appropriateness |
| sbp | Systolic blood pressure | Numeric | Synthetic; not clinically validated |
