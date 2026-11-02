# Synthetic capstone data dictionary

All records are generated for education; no real patients or clinical events are represented.

| File | Grain | Key fields |
|---|---|---|
| `patients.csv` | One row per synthetic patient | patient_id, age_years, sex, diabetes, hypertension |
| `encounters.csv` | One row per synthetic encounter | encounter_id, patient_id, department, dates, LOS, discharge_status |
| `medication_orders.csv` | One row per synthetic medication order | order_id, encounter_id, drug_class, route, generic flag, quantity |
| `laboratory_results.csv` | One row per synthetic result | result_id, encounter_id, analyte, value, unit, status |

Do not interpret generated values as clinical reference data. The dataset intentionally has one-to-many relationships: patients may have multiple encounters, and encounters may have multiple medication orders and laboratory results.
