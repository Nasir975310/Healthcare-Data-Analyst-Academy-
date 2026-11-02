# Practicum synthetic data dictionary

| File | Grain | Rows | Key fields | Cautions |
|---|---|---:|---|---|
| hospital_encounters_raw.csv | Encounter | 1,200 | encounter_id | Synthetic supplied flag is not a validated readmission measure |
| antihypertensive_due_raw.csv | Patient | 500 | patient_id | Prescription is not adherence; cohort is not causal |
| pv_cases_raw.csv | Safety case | 240 | case_id | Duplicate-candidate flag requires manual review; no signal/causality conclusion |
| medication_orders_raw.csv | Medication order | 1,800 | order_id | Contains deliberately planted quality exceptions and orphan references |
| dashboard_cards_to_review.csv | Dashboard card | 4 | card | Contains deliberately questionable definitions/values for critique |

All names, IDs, dates and values are fabricated for education. These records are not patient data and must not be used for clinical care, regulatory submissions or operational decisions.
