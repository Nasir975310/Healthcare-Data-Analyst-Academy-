CREATE SCHEMA raw;
CREATE SCHEMA curated;
CREATE TABLE raw.patients (
  patient_id TEXT, gender TEXT, birth_date DATE, residence TEXT, region TEXT
);
CREATE TABLE raw.encounters (
  encounter_id TEXT, patient_id TEXT, encounter_date DATE,
  encounter_type TEXT, status TEXT
);
CREATE TABLE raw.observations (
  observation_id TEXT, encounter_id TEXT, measure TEXT, value NUMERIC, unit TEXT
);
CREATE TABLE raw.medications (
  medication_id TEXT, encounter_id TEXT, medication TEXT, drug_class TEXT, is_active BOOLEAN
);
CREATE TABLE curated.dim_patient (
  patient_id TEXT PRIMARY KEY, gender TEXT, birth_date DATE, region TEXT
);
CREATE TABLE curated.fact_encounter (
  encounter_id TEXT PRIMARY KEY,
  patient_id TEXT NOT NULL REFERENCES curated.dim_patient(patient_id),
  encounter_date DATE NOT NULL, encounter_type TEXT NOT NULL, status TEXT NOT NULL
);
CREATE TABLE curated.encounter_exception (
  encounter_id TEXT, patient_id TEXT, reason_code TEXT NOT NULL
);
CREATE TABLE curated.fact_observation (
  observation_id TEXT PRIMARY KEY,
  encounter_id TEXT NOT NULL REFERENCES curated.fact_encounter(encounter_id),
  measure TEXT NOT NULL, value NUMERIC NOT NULL, unit TEXT NOT NULL
);
CREATE TABLE curated.fact_medication_order (
  medication_id TEXT PRIMARY KEY,
  encounter_id TEXT NOT NULL REFERENCES curated.fact_encounter(encounter_id),
  medication TEXT NOT NULL, drug_class TEXT NOT NULL, is_active BOOLEAN NOT NULL
);
CREATE INDEX ix_fact_encounter_date ON curated.fact_encounter(encounter_date);
CREATE INDEX ix_fact_encounter_patient ON curated.fact_encounter(patient_id);
CREATE INDEX ix_fact_med_order_class ON curated.fact_medication_order(drug_class);
