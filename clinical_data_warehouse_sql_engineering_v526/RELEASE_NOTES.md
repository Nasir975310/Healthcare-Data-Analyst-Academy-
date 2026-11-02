# Release 5.26.0

- Added clinical star-schema warehouse built from v5.25 FHIR ETL outputs.
- Added date, patient, encounter and terminology dimensions.
- Added Observation and MedicationRequest fact tables with declared grain.
- Added encounter summary and patient cohort marts.
- Added analytic SQL examples using window functions and aggregation.
- Added foreign-key/integrity checks and SHA-256 warehouse manifest.
- Documented fanout prevention and SCD Type 1/Type 2 boundaries.
