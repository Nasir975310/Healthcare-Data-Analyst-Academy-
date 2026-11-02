-- PostgreSQL 14+ reference DDL. Execute in a dedicated practice database.
CREATE SCHEMA IF NOT EXISTS hda_raw;
CREATE SCHEMA IF NOT EXISTS hda_curated;

CREATE TABLE IF NOT EXISTS hda_raw.encounters (
  source_row_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  encounter_id TEXT,
  patient_id TEXT,
  encounter_date DATE,
  encounter_type TEXT,
  source_file TEXT NOT NULL,
  ingested_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS hda_curated.dim_patient (
  patient_id TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS hda_curated.fact_encounter (
  encounter_id TEXT PRIMARY KEY,
  patient_id TEXT NOT NULL REFERENCES hda_curated.dim_patient(patient_id),
  encounter_date DATE NOT NULL,
  encounter_type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS hda_curated.encounter_exceptions (
  source_row_id BIGINT PRIMARY KEY,
  encounter_id TEXT,
  patient_id TEXT,
  reason_code TEXT NOT NULL,
  reason_detail TEXT,
  recorded_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_fact_encounter_date
ON hda_curated.fact_encounter(encounter_date);
CREATE INDEX IF NOT EXISTS ix_fact_encounter_patient
ON hda_curated.fact_encounter(patient_id);
