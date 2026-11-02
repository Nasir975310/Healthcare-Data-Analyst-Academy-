# Data model and grain

## Operational (3NF-style) model
- `patients`: one row per synthetic patient token.
- `departments`: one row per department.
- `encounters`: one row per encounter; foreign keys to patient and department.
- Natural business key: `encounter_id`; surrogate primary key: `encounter_key`.

## Analytics star schema
- `fact_encounter`: one row per encounter (grain). `encounter_count=1` is additive.
- `dim_date`: one row per calendar date.
- `dim_department`: one row per department.
- Patient dimension is included in the PostgreSQL schema to support patient-level grouping; use a synthetic token only.

Do not mix encounter grain with patient grain. A patient may have multiple encounters. State the grain and denominator for each metric. Slowly changing dimensions and late-arriving facts are advanced topics not fully implemented in this lab.
