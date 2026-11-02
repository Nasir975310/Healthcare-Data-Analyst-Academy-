# Clinical data warehouse design

## Star-schema model
- `dim_date`: calendar attributes and integer YYYYMMDD key.
- `dim_patient`: patient descriptors. Current demonstration uses Type 1 overwrite semantics; version/validity columns are present but no historical snapshots are supplied, so this is not a demonstrated SCD Type 2 pipeline.
- `dim_encounter`: encounter descriptors and patient relationship.
- `dim_terminology`: source and illustrative mapped codes.
- `fact_observation`: one row per source Observation, numeric value, unit, date and dimension keys.
- `fact_medication_request`: one row per MedicationRequest.
- `mart_encounter_summary`: one row per Encounter; independently aggregated observation and medication facts avoid fact-to-fact fanout.
- `mart_patient_cohort`: one row per patient meeting the configured encounter-status criterion.

## Grain and modelling rules
Declare grain before joins. Do not directly join multiple one-to-many fact tables and aggregate afterwards: that can multiply records. The encounter mart aggregates each fact independently by encounter before joining. Observation facts preserve units and terminology keys; do not combine mixed analytes or units without explicit selection and conversion.

## SCD strategy
This release documents Type 1 versus Type 2 and includes validity/version columns in `dim_patient`. The bundled source has one patient snapshot only, so Type 2 change detection and historical row closure cannot be validated from this dataset. A later release should add versioned patient snapshots and an idempotent Type 2 loader.

## SQL
`sql/analytics_examples.sql` includes date trends, patient encounter sequencing with `ROW_NUMBER`/`LAG`, cohort summaries and a staging-to-fact reconciliation example. The reconciliation query expects a staging table named `stg_observations`; create it from source CSV if running that final query. The other queries run against the built warehouse.
