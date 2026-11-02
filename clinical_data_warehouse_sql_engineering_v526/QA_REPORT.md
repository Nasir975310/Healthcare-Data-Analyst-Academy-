# QA report — v5.26.0

- Warehouse build executed end-to-end against v5.25 synthetic FHIR ETL outputs.
- Unit tests: 5 passed.
- Dimension rows: date 6, patient 5, encounter 6, terminology 2.
- Fact rows: Observation 12, MedicationRequest 5.
- Marts: encounter summary 6, patient cohort 4.
- Source-to-mart fact counts reconciled: 12 observations and 5 medication requests.
- SQLite integrity check: `ok`; foreign-key violations: 0.
- Window-function query executed successfully in SQLite.
- Patient SCD Type 2 history is documented but not implemented because only one source snapshot exists.
