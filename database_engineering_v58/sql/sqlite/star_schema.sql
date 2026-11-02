CREATE TABLE dim_date (
 date_key INTEGER PRIMARY KEY,
 calendar_date TEXT NOT NULL UNIQUE,
 year INTEGER NOT NULL,
 month INTEGER NOT NULL
);
CREATE TABLE dim_department (
 department_key INTEGER PRIMARY KEY,
 department_name TEXT NOT NULL UNIQUE
);
CREATE TABLE fact_encounter (
 encounter_fact_key INTEGER PRIMARY KEY,
 encounter_id TEXT NOT NULL UNIQUE,
 date_key INTEGER NOT NULL REFERENCES dim_date(date_key),
 department_key INTEGER NOT NULL REFERENCES dim_department(department_key),
 encounter_count INTEGER NOT NULL DEFAULT 1 CHECK(encounter_count=1),
 los_days REAL NOT NULL CHECK(los_days>=0),
 order_count INTEGER NOT NULL CHECK(order_count>=0)
);
CREATE INDEX idx_fact_date_department ON fact_encounter(date_key,department_key);
