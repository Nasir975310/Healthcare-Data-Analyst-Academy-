-- SQLite teaching schema; not a validated EDC or safety database.
PRAGMA foreign_keys = ON;
CREATE TABLE trial_subject (
 subject_id TEXT PRIMARY KEY, site_id TEXT NOT NULL, arm TEXT NOT NULL CHECK(arm IN ('ACTIVE','CONTROL')),
 age INTEGER CHECK(age BETWEEN 18 AND 120), sex TEXT, disposition TEXT
);
CREATE TABLE trial_visit (
 subject_id TEXT NOT NULL REFERENCES trial_subject(subject_id),
 visit_name TEXT NOT NULL, visit_date TEXT, visit_status TEXT,
 PRIMARY KEY(subject_id, visit_name)
);
CREATE TABLE trial_measurement (
 subject_id TEXT NOT NULL, visit_name TEXT NOT NULL, parameter_code TEXT NOT NULL,
 value REAL, unit TEXT, baseline_flag INTEGER CHECK(baseline_flag IN (0,1)),
 FOREIGN KEY(subject_id,visit_name) REFERENCES trial_visit(subject_id,visit_name),
 PRIMARY KEY(subject_id,visit_name,parameter_code)
);
CREATE TABLE pv_case (
 case_id TEXT PRIMARY KEY, patient_key TEXT, receipt_date TEXT, reporter_type TEXT,
 source_version INTEGER NOT NULL DEFAULT 1
);
CREATE TABLE pv_product (
 case_id TEXT NOT NULL REFERENCES pv_case(case_id), product_role TEXT NOT NULL,
 product_name TEXT NOT NULL, PRIMARY KEY(case_id,product_role,product_name)
);
CREATE TABLE pv_event (
 case_id TEXT NOT NULL REFERENCES pv_case(case_id), event_sequence INTEGER NOT NULL,
 verbatim_term TEXT, placeholder_event_code TEXT, serious INTEGER CHECK(serious IN (0,1)),
 expected INTEGER CHECK(expected IN (0,1)), PRIMARY KEY(case_id,event_sequence)
);
