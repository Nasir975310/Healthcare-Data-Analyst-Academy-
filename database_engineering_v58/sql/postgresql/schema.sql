CREATE SCHEMA IF NOT EXISTS analytics;
CREATE TABLE IF NOT EXISTS analytics.dim_department (
 department_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 department_name TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS analytics.dim_date (
 date_key INTEGER PRIMARY KEY,
 calendar_date DATE NOT NULL UNIQUE,
 calendar_year SMALLINT NOT NULL,
 calendar_month SMALLINT NOT NULL CHECK(calendar_month BETWEEN 1 AND 12)
);
CREATE TABLE IF NOT EXISTS analytics.dim_patient (
 patient_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 patient_token TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS analytics.fact_encounter (
 encounter_fact_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 encounter_id TEXT NOT NULL UNIQUE,
 patient_key BIGINT NOT NULL REFERENCES analytics.dim_patient(patient_key),
 department_key BIGINT NOT NULL REFERENCES analytics.dim_department(department_key),
 date_key INTEGER NOT NULL REFERENCES analytics.dim_date(date_key),
 encounter_count SMALLINT NOT NULL DEFAULT 1 CHECK(encounter_count=1),
 los_days NUMERIC(8,2) NOT NULL CHECK(los_days>=0),
 order_count INTEGER NOT NULL CHECK(order_count>=0),
 disposition TEXT NOT NULL CHECK(disposition IN ('Discharged','Admitted','Transferred'))
);
CREATE INDEX IF NOT EXISTS ix_fact_date_dept ON analytics.fact_encounter(date_key,department_key);
CREATE INDEX IF NOT EXISTS ix_fact_patient_date ON analytics.fact_encounter(patient_key,date_key);
