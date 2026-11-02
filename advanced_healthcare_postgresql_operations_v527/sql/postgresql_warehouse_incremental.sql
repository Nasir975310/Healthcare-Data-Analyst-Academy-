-- PostgreSQL 15+ reference implementation. Execute with psql.
-- This script creates schema objects; load CSVs into staging tables using \copy.
BEGIN;
CREATE SCHEMA IF NOT EXISTS hda;
CREATE TABLE IF NOT EXISTS hda.dim_patient (
 patient_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 patient_id TEXT NOT NULL, gender TEXT, birth_date DATE, record_hash TEXT NOT NULL,
 valid_from DATE NOT NULL, valid_to DATE, is_current BOOLEAN NOT NULL DEFAULT TRUE,
 CONSTRAINT ck_patient_validity CHECK(valid_to IS NULL OR valid_to>=valid_from),
 CONSTRAINT uq_patient_version UNIQUE(patient_id,valid_from)
);
CREATE UNIQUE INDEX IF NOT EXISTS uq_patient_current ON hda.dim_patient(patient_id) WHERE is_current;
CREATE TABLE IF NOT EXISTS hda.dim_encounter(
 encounter_id TEXT PRIMARY KEY, patient_id TEXT NOT NULL, status TEXT, class_code TEXT,
 start_datetime TIMESTAMPTZ, end_datetime TIMESTAMPTZ
);
CREATE TABLE IF NOT EXISTS hda.fact_observation(
 observation_id TEXT PRIMARY KEY, patient_id TEXT NOT NULL, encounter_id TEXT NOT NULL,
 effective_datetime TIMESTAMPTZ, source_system TEXT, source_code TEXT,
 value_numeric NUMERIC, unit TEXT
);
CREATE TABLE IF NOT EXISTS hda.fact_medication_request(
 medication_request_id TEXT PRIMARY KEY, patient_id TEXT NOT NULL, encounter_id TEXT NOT NULL,
 authored_on DATE, status TEXT, medication_display TEXT
);
CREATE TABLE IF NOT EXISTS hda.etl_batch(
 batch_id TEXT PRIMARY KEY, started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
 completed_at TIMESTAMPTZ, source_hash TEXT NOT NULL, status TEXT NOT NULL,
 inserted_patients INTEGER DEFAULT 0, changed_patients INTEGER DEFAULT 0,
 upserted_encounters INTEGER DEFAULT 0, inserted_observations INTEGER DEFAULT 0,
 inserted_medications INTEGER DEFAULT 0, error_message TEXT
);
CREATE INDEX IF NOT EXISTS ix_obs_patient_time ON hda.fact_observation(patient_id,effective_datetime);
CREATE INDEX IF NOT EXISTS ix_obs_code_time ON hda.fact_observation(source_code,effective_datetime);
CREATE INDEX IF NOT EXISTS ix_med_patient_date ON hda.fact_medication_request(patient_id,authored_on);
COMMIT;

-- Staging table definitions. Load files with psql \copy (run from repo root):
CREATE TEMP TABLE stg_patient(patient_id TEXT,gender TEXT,birth_date DATE);
CREATE TEMP TABLE stg_encounter(encounter_id TEXT,patient_id TEXT,status TEXT,class_code TEXT,start_datetime TIMESTAMPTZ,end_datetime TIMESTAMPTZ);
CREATE TEMP TABLE stg_observation(observation_id TEXT,patient_id TEXT,encounter_id TEXT,effective_datetime TIMESTAMPTZ,source_system TEXT,source_code TEXT,value_numeric NUMERIC,unit TEXT);
CREATE TEMP TABLE stg_medication(medication_request_id TEXT,patient_id TEXT,encounter_id TEXT,authored_on DATE,status TEXT,medication_display TEXT);

-- Example load commands (adjust file paths):
-- \copy stg_patient FROM 'patients.csv' CSV HEADER
-- \copy stg_encounter FROM 'encounters.csv' CSV HEADER
-- \copy stg_observation FROM 'observations_postgres.csv' CSV HEADER
-- \copy stg_medication FROM 'medications.csv' CSV HEADER

-- Idempotent Type 2 patient dimension load. Set :effective_date in psql.
-- Hash only attributes selected for history; expand according to governance policy.
CREATE TEMP TABLE stg_patient_hashed ON COMMIT DROP AS
SELECT patient_id,gender,birth_date,
       encode(digest(concat_ws('|',coalesce(gender,''),coalesce(birth_date::text,'')),'sha256'),'hex') AS record_hash
FROM stg_patient;

-- New patients.
INSERT INTO hda.dim_patient(patient_id,gender,birth_date,record_hash,valid_from,valid_to,is_current)
SELECT s.patient_id,s.gender,s.birth_date,s.record_hash,DATE '2026-01-01',NULL,TRUE
FROM stg_patient_hashed s
WHERE NOT EXISTS(SELECT 1 FROM hda.dim_patient d WHERE d.patient_id=s.patient_id AND d.is_current);

-- Changed patients: close prior version, then insert new current version.
WITH changed AS (
 SELECT s.* FROM stg_patient_hashed s JOIN hda.dim_patient d
 ON d.patient_id=s.patient_id AND d.is_current
 WHERE d.record_hash<>s.record_hash
), closed AS (
 UPDATE hda.dim_patient d SET valid_to=DATE '2026-01-02',is_current=FALSE
 FROM changed c WHERE d.patient_id=c.patient_id AND d.is_current
 RETURNING d.patient_id
)
INSERT INTO hda.dim_patient(patient_id,gender,birth_date,record_hash,valid_from,valid_to,is_current)
SELECT c.patient_id,c.gender,c.birth_date,c.record_hash,DATE '2026-01-03',NULL,TRUE
FROM changed c JOIN closed x USING(patient_id);

INSERT INTO hda.dim_encounter(encounter_id,patient_id,status,class_code,start_datetime,end_datetime)
SELECT encounter_id,patient_id,status,class_code,start_datetime,end_datetime FROM stg_encounter
ON CONFLICT(encounter_id) DO UPDATE SET patient_id=EXCLUDED.patient_id,status=EXCLUDED.status,
 class_code=EXCLUDED.class_code,start_datetime=EXCLUDED.start_datetime,end_datetime=EXCLUDED.end_datetime;

INSERT INTO hda.fact_observation(observation_id,patient_id,encounter_id,effective_datetime,source_system,source_code,value_numeric,unit)
SELECT observation_id,patient_id,encounter_id,effective_datetime,source_system,source_code,value_numeric,unit
FROM stg_observation ON CONFLICT(observation_id) DO NOTHING;

INSERT INTO hda.fact_medication_request(medication_request_id,patient_id,encounter_id,authored_on,status,medication_display)
SELECT medication_request_id,patient_id,encounter_id,authored_on,status,medication_display
FROM stg_medication ON CONFLICT(medication_request_id) DO NOTHING;

-- Operational checks
SELECT 'observation_count' AS check_name, count(*) AS result FROM hda.fact_observation
UNION ALL SELECT 'medication_count',count(*) FROM hda.fact_medication_request;
