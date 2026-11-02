-- SQLite schema for the synthetic antihypertensive utilization case study
CREATE TABLE IF NOT EXISTS hypertension_records (
 record_id TEXT PRIMARY KEY, age_years INTEGER NOT NULL, sex TEXT NOT NULL,
 diabetes INTEGER NOT NULL CHECK(diabetes IN (0,1)), ckd INTEGER NOT NULL CHECK(ckd IN (0,1)),
 ischemic_heart_disease INTEGER NOT NULL CHECK(ischemic_heart_disease IN (0,1)),
 primary_drug_class TEXT, regimen_classes TEXT, antihypertensive_count INTEGER, adherence_category TEXT,
 baseline_sbp_mmhg REAL, baseline_dbp_mmhg REAL, followup_sbp_mmhg REAL, followup_dbp_mmhg REAL, followup_days INTEGER);
