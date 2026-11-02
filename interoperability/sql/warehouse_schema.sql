-- SQLite training warehouse schema. Execute in a disposable local database.
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS dim_patient(
 patient_id TEXT PRIMARY KEY, birth_date TEXT, administrative_sex TEXT, active INTEGER
);
CREATE TABLE IF NOT EXISTS dim_department(
 department_id INTEGER PRIMARY KEY, department_name TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS fact_encounter(
 encounter_id TEXT PRIMARY KEY, patient_id TEXT NOT NULL REFERENCES dim_patient(patient_id),
 department_id INTEGER REFERENCES dim_department(department_id),
 encounter_class TEXT, status TEXT, start_date TEXT, end_date TEXT, source_system TEXT
);
CREATE TABLE IF NOT EXISTS fact_medication_order(
 medication_order_id TEXT PRIMARY KEY, encounter_id TEXT NOT NULL REFERENCES fact_encounter(encounter_id),
 patient_id TEXT NOT NULL REFERENCES dim_patient(patient_id), drug_display TEXT,
 atc_code TEXT, route TEXT, status TEXT, authored_on TEXT, quantity REAL, source_system TEXT
);
CREATE TABLE IF NOT EXISTS fact_observation(
 observation_id TEXT PRIMARY KEY, encounter_id TEXT NOT NULL REFERENCES fact_encounter(encounter_id),
 patient_id TEXT NOT NULL REFERENCES dim_patient(patient_id), test_display TEXT,
 loinc_code TEXT, value REAL, unit TEXT, effective_date TEXT, status TEXT, source_system TEXT
);
CREATE INDEX IF NOT EXISTS ix_fact_encounter_patient ON fact_encounter(patient_id);
CREATE INDEX IF NOT EXISTS ix_fact_med_order_encounter ON fact_medication_order(encounter_id);
CREATE INDEX IF NOT EXISTS ix_fact_observation_encounter ON fact_observation(encounter_id);
