# Excel and Power Query Laboratory — Data Dictionary

All records are synthetic training data. They do not represent real patients, prescribing decisions, prices, or hospital performance.

## excel_encounters.csv
| Field | Meaning | Type |
|---|---|---|
| encounter_id | Unique synthetic encounter key | Text |
| patient_id | Synthetic patient key; may repeat across encounters | Text |
| admission_date / discharge_date | Encounter dates | ISO date |
| age_years | Age in years | Integer |
| department | Reporting department | Category |
| payer_type | Synthetic payer category | Category |
| length_of_stay_days | Supplied stay duration | Integer |
| discharge_disposition | Discharge outcome category | Category |
| readmission_30d_flag | Supplied synthetic binary flag; not independently validated | 0/1 |

## excel_raw_medication_orders.csv
| Field | Meaning | Type |
|---|---|---|
| order_id | Source order identifier; inspect duplicates | Text |
| encounter_id | Encounter foreign key; inspect orphan values | Text |
| order_date | Order date | ISO date |
| drug_name | Source drug label; includes whitespace/case defect | Text |
| therapeutic_class | Source class; includes a blank | Text |
| route | Source route | Category |
| order_status | Source status; includes whitespace/case defect | Category |
| quantity | Synthetic ordered quantity; not dispensing or administration | Integer |
| unit_cost_inr | Synthetic unit cost; includes missing value | Decimal INR |
| prescriber_id | Synthetic prescriber identifier | Text |
| pharmacy_location | Synthetic pharmacy location | Category |
| line_total_inr | quantity × unit_cost_inr; blank if unit cost is missing | Decimal INR |

The raw orders file intentionally contains one duplicate-like source row, one orphan encounter key, inconsistent text formatting, a missing therapeutic class and a missing unit cost. The `order_id` values remain unique because the repeated source content is assigned a distinct source ID; students must detect duplicate business content as a separate quality question.

## synthetic_formulary_reference.csv
Reference mapping for drug name, standard therapeutic class, standard route, formulary active flag and synthetic reference unit cost. It is a training lookup table, not a clinical formulary.
