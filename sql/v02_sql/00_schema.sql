
PRAGMA foreign_keys=ON;
CREATE TABLE departments (
 department_id INTEGER PRIMARY KEY,
 department_code TEXT NOT NULL UNIQUE,
 department_name TEXT NOT NULL
);
CREATE TABLE patients (
 patient_id INTEGER PRIMARY KEY,
 synthetic_patient_code TEXT NOT NULL UNIQUE,
 sex TEXT CHECK(sex IN ('F','M','Other','Unknown')),
 date_of_birth TEXT,
 district TEXT,
 created_at TEXT NOT NULL
);
CREATE TABLE encounters (
 encounter_id INTEGER PRIMARY KEY,
 patient_id INTEGER NOT NULL REFERENCES patients(patient_id),
 department_id INTEGER NOT NULL REFERENCES departments(department_id),
 admission_date TEXT NOT NULL,
 discharge_date TEXT,
 encounter_type TEXT NOT NULL CHECK(encounter_type IN ('OPD','IPD','Emergency')),
 systolic_bp REAL,
 diastolic_bp REAL,
 length_of_stay_days INTEGER,
 outcome TEXT CHECK(outcome IN ('Discharged','Transferred','Died','Ongoing')),
 readmitted_30d INTEGER CHECK(readmitted_30d IN (0,1) OR readmitted_30d IS NULL)
);
CREATE TABLE diagnoses (
 diagnosis_id INTEGER PRIMARY KEY,
 encounter_id INTEGER NOT NULL REFERENCES encounters(encounter_id),
 diagnosis_code TEXT NOT NULL,
 diagnosis_label TEXT NOT NULL,
 diagnosis_role TEXT NOT NULL CHECK(diagnosis_role IN ('Primary','Secondary'))
);
CREATE TABLE prescriptions (
 prescription_id INTEGER PRIMARY KEY,
 encounter_id INTEGER NOT NULL REFERENCES encounters(encounter_id),
 generic_name TEXT NOT NULL,
 drug_class TEXT NOT NULL,
 dose TEXT,
 route TEXT,
 start_date TEXT NOT NULL,
 stop_date TEXT
);
CREATE TABLE laboratory_results (
 result_id INTEGER PRIMARY KEY,
 encounter_id INTEGER NOT NULL REFERENCES encounters(encounter_id),
 test_code TEXT NOT NULL,
 test_name TEXT NOT NULL,
 result_value REAL,
 unit TEXT NOT NULL,
 result_date TEXT NOT NULL,
 abnormal_flag INTEGER CHECK(abnormal_flag IN (0,1) OR abnormal_flag IS NULL)
);
