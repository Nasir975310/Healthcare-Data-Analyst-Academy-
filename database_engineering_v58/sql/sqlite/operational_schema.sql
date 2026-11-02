PRAGMA foreign_keys=ON;
CREATE TABLE departments (
 department_id INTEGER PRIMARY KEY,
 department_name TEXT NOT NULL UNIQUE
);
CREATE TABLE patients (
 patient_key INTEGER PRIMARY KEY,
 patient_token TEXT NOT NULL UNIQUE
);
CREATE TABLE encounters (
 encounter_key INTEGER PRIMARY KEY,
 encounter_id TEXT NOT NULL UNIQUE,
 patient_key INTEGER NOT NULL REFERENCES patients(patient_key),
 department_id INTEGER NOT NULL REFERENCES departments(department_id),
 admit_date TEXT NOT NULL CHECK(date(admit_date) IS NOT NULL),
 los_days REAL NOT NULL CHECK(los_days>=0),
 disposition TEXT NOT NULL CHECK(disposition IN ('Discharged','Admitted','Transferred'))
);
CREATE INDEX idx_encounters_admit_date ON encounters(admit_date);
CREATE INDEX idx_encounters_department_date ON encounters(department_id,admit_date);
CREATE VIEW v_department_summary AS
 SELECT d.department_name,COUNT(*) AS encounter_count,ROUND(AVG(e.los_days),2) AS mean_los_days
 FROM encounters e JOIN departments d USING(department_id)
 GROUP BY d.department_name;
