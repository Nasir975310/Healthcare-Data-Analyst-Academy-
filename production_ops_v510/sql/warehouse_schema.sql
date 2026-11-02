PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS dim_department(
 department_id TEXT PRIMARY KEY,
 department_name TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS fact_encounter(
 encounter_id TEXT PRIMARY KEY,
 patient_id TEXT NOT NULL,
 department_id TEXT NOT NULL REFERENCES dim_department(department_id),
 encounter_date TEXT NOT NULL,
 encounter_type TEXT NOT NULL,
 discharge_status TEXT NOT NULL,
 los_days INTEGER NOT NULL CHECK(los_days>=0),
 charge_inr REAL NOT NULL CHECK(charge_inr>=0),
 source_file_sha256 TEXT NOT NULL,
 loaded_at_utc TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_fact_date_department ON fact_encounter(encounter_date,department_id);
CREATE INDEX IF NOT EXISTS ix_fact_patient ON fact_encounter(patient_id);
