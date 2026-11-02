-- PostgreSQL 15+ recommended. Apply with psql -v ON_ERROR_STOP=1 -f 001_schema.sql
BEGIN;
CREATE SCHEMA IF NOT EXISTS hda;
SET search_path TO hda, public;

CREATE TABLE IF NOT EXISTS dim_date (
  date_key integer PRIMARY KEY,
  full_date date NOT NULL UNIQUE,
  year smallint NOT NULL,
  month smallint NOT NULL CHECK(month BETWEEN 1 AND 12),
  day smallint NOT NULL CHECK(day BETWEEN 1 AND 31),
  quarter smallint NOT NULL CHECK(quarter BETWEEN 1 AND 4)
);

-- SCD Type 2: exactly one current row per natural patient_id.
CREATE TABLE IF NOT EXISTS dim_patient (
  patient_key bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  patient_id text NOT NULL,
  gender text,
  birth_date date,
  valid_from timestamptz NOT NULL,
  valid_to timestamptz,
  is_current boolean NOT NULL DEFAULT true,
  version integer NOT NULL,
  row_hash text NOT NULL,
  CONSTRAINT uq_patient_version UNIQUE(patient_id,version),
  CONSTRAINT ck_patient_validity CHECK(valid_to IS NULL OR valid_to > valid_from),
  CONSTRAINT ck_patient_current CHECK((is_current AND valid_to IS NULL) OR (NOT is_current AND valid_to IS NOT NULL))
);
CREATE UNIQUE INDEX IF NOT EXISTS uq_dim_patient_current ON dim_patient(patient_id) WHERE is_current;

CREATE TABLE IF NOT EXISTS dim_encounter (
  encounter_key bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  encounter_id text NOT NULL UNIQUE,
  patient_id text NOT NULL,
  status text,
  class_code text,
  start_datetime timestamptz,
  end_datetime timestamptz
);
CREATE TABLE IF NOT EXISTS dim_terminology (
  terminology_key bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  source_system text NOT NULL,
  source_code text NOT NULL,
  display text,
  mapped_system text,
  mapped_concept text,
  mapping_status text NOT NULL,
  UNIQUE(source_system,source_code)
);
CREATE TABLE IF NOT EXISTS fact_observation (
  observation_key bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  observation_id text NOT NULL UNIQUE,
  patient_key bigint REFERENCES dim_patient(patient_key),
  encounter_key bigint REFERENCES dim_encounter(encounter_key),
  date_key integer REFERENCES dim_date(date_key),
  terminology_key bigint REFERENCES dim_terminology(terminology_key),
  value_numeric double precision,
  unit text
);
CREATE TABLE IF NOT EXISTS fact_medication_request (
  medication_key bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  medication_request_id text NOT NULL UNIQUE,
  patient_key bigint REFERENCES dim_patient(patient_key),
  encounter_key bigint REFERENCES dim_encounter(encounter_key),
  authored_date_key integer REFERENCES dim_date(date_key),
  status text,
  medication_display text,
  source_system text,
  source_code text
);
CREATE TABLE IF NOT EXISTS mart_encounter_summary (
  encounter_id text PRIMARY KEY,
  patient_id text NOT NULL,
  encounter_date date,
  encounter_status text,
  observation_count bigint NOT NULL,
  medication_request_count bigint NOT NULL,
  distinct_observation_concepts bigint NOT NULL,
  systolic_mean double precision,
  diastolic_mean double precision,
  refreshed_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS mart_patient_cohort (
  patient_id text PRIMARY KEY,
  qualifying_encounters bigint NOT NULL,
  first_qualifying_encounter date,
  last_qualifying_encounter date,
  refreshed_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ix_fact_obs_patient_date ON fact_observation(patient_key,date_key);
CREATE INDEX IF NOT EXISTS ix_fact_obs_term_date ON fact_observation(terminology_key,date_key);
CREATE INDEX IF NOT EXISTS ix_fact_med_patient_date ON fact_medication_request(patient_key,authored_date_key);
CREATE INDEX IF NOT EXISTS ix_enc_patient_start ON dim_encounter(patient_id,start_datetime);
COMMIT;
