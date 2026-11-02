# Synthetic healthcare data contracts

## Encounter extract
- **Grain:** one row per encounter.
- **Primary key:** `encounter_id` (non-null, unique, text).
- **Required fields:** encounter_id, patient_id, admission_date, department, length_of_stay_days.
- **Types:** identifiers/categories as text; dates ISO `YYYY-MM-DD`; age and LOS numeric; supplied flag numeric 0/1.
- **Quality rules:** admission date must parse; key unique; LOS nonnegative; patient_id may repeat because one patient can have multiple encounters.
- **Caveat:** supplied `readmission_30d_flag` is synthetic and not independently validated.

## Medication-order extract
- **Grain:** one row per medication order.
- **Primary key:** `order_id` (non-null, unique, text).
- **Foreign reference:** `encounter_id` should match Encounter[encounter_id].
- **Required fields:** order_id, encounter_id, order_date, drug_name, quantity.
- **Types:** identifiers and labels as text; order_date ISO date; quantity positive numeric.
- **Optional fields:** unit_cost_inr, prescriber_id, pharmacy_location. If absent, record as not supplied; do not fabricate.
- **Quality rules:** duplicate order key is fatal; invalid date or nonpositive quantity is fatal; orphan encounter reference is quarantined; missing therapeutic class is a warning.
- **Caveat:** order data is not dispensing, administration, adherence or appropriateness evidence.

## General pipeline contract
- Preserve source payloads and checksums.
- Keep source, raw, curated and quarantine layers distinguishable.
- Record run ID, timestamps, source row counts, loaded rows, rejected rows and status.
- No real PHI is included in this Academy. Do not use production data without authorisation, approved security controls and an appropriate data-processing agreement.
