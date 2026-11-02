# Source data dictionary

All values are synthetic. The data period and units are illustrative.

| File | Column | Meaning |
|---|---|---|
| patients.csv | patient_id | Synthetic patient key |
| patients.csv | gender | Synthetic demographic category |
| patients.csv | birth_date | Date of birth; use only when age is analytically required |
| patients.csv | residence | Urban/rural category |
| patients.csv | region | Synthetic administrative region |
| encounters.csv | encounter_id | Encounter key |
| encounters.csv | patient_id | Patient foreign key; one deliberate orphan exists |
| encounters.csv | encounter_date | ISO date |
| encounters.csv | encounter_type | Outpatient, inpatient or emergency |
| encounters.csv | status | Completed, cancelled or scheduled |
| observations.csv | observation_id | Observation key |
| observations.csv | encounter_id | Encounter foreign key |
| observations.csv | measure | Systolic BP or diastolic BP |
| observations.csv | value | Numeric synthetic observation |
| observations.csv | unit | mmHg |
| medications.csv | medication_id | Medication-order key |
| medications.csv | encounter_id | Encounter foreign key |
| medications.csv | medication | Synthetic medication name |
| medications.csv | drug_class | Illustrative class label |
| medications.csv | is_active | 1/0 training flag; not a validated order status |

## Grain
- Patient: one row per patient.
- Encounter: one row per encounter.
- Observation: one row per recorded measurement.
- Medication: one row per medication order.

The two child facts (observation and medication) must remain separate or be independently aggregated before combining. Otherwise, multiple measurements multiplied by multiple medication orders can inflate counts.
