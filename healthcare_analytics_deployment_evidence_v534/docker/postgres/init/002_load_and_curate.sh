#!/bin/sh
set -eu
export PGPASSWORD="${POSTGRES_PASSWORD}"
psql -v ON_ERROR_STOP=1 -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" <<'SQL'
\copy raw.patients(patient_id,gender,birth_date,residence,region) FROM '/seed/patients.csv' WITH (FORMAT csv, HEADER true)
\copy raw.encounters(encounter_id,patient_id,encounter_date,encounter_type,status) FROM '/seed/encounters.csv' WITH (FORMAT csv, HEADER true)
\copy raw.observations(observation_id,encounter_id,measure,value,unit) FROM '/seed/observations.csv' WITH (FORMAT csv, HEADER true)
\copy raw.medications(medication_id,encounter_id,medication,drug_class,is_active) FROM '/seed/medications.csv' WITH (FORMAT csv, HEADER true)

INSERT INTO curated.dim_patient(patient_id,gender,birth_date,region)
SELECT patient_id,gender,birth_date,region FROM raw.patients
ON CONFLICT (patient_id) DO NOTHING;

INSERT INTO curated.fact_encounter(encounter_id,patient_id,encounter_date,encounter_type,status)
SELECT e.encounter_id,e.patient_id,e.encounter_date,e.encounter_type,e.status
FROM raw.encounters e
JOIN curated.dim_patient p ON p.patient_id=e.patient_id
WHERE e.encounter_id IS NOT NULL
ON CONFLICT (encounter_id) DO NOTHING;

INSERT INTO curated.encounter_exception(encounter_id,patient_id,reason_code)
SELECT e.encounter_id,e.patient_id,'UNKNOWN_PATIENT'
FROM raw.encounters e
LEFT JOIN curated.dim_patient p ON p.patient_id=e.patient_id
WHERE p.patient_id IS NULL;

INSERT INTO curated.fact_observation(observation_id,encounter_id,measure,value,unit)
SELECT o.observation_id,o.encounter_id,o.measure,o.value,o.unit
FROM raw.observations o
JOIN curated.fact_encounter e ON e.encounter_id=o.encounter_id
ON CONFLICT (observation_id) DO NOTHING;

INSERT INTO curated.fact_medication_order(medication_id,encounter_id,medication,drug_class,is_active)
SELECT m.medication_id,m.encounter_id,m.medication,m.drug_class,m.is_active
FROM raw.medications m
JOIN curated.fact_encounter e ON e.encounter_id=m.encounter_id
ON CONFLICT (medication_id) DO NOTHING;
SQL
