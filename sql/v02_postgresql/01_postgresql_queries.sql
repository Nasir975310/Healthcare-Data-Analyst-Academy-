-- PostgreSQL examples for the academy synthetic database.
-- Schema is academy. Connect to the practice database and run:
SET search_path TO academy;

-- Explicit date range; DATE columns are compared with DATE literals.
SELECT encounter_id, patient_id, admission_date, encounter_type
FROM encounters
WHERE admission_date >= DATE '2026-01-01'
  AND admission_date < DATE '2026-04-01'
ORDER BY admission_date, encounter_id;

-- Distinct patients versus encounter rows.
SELECT COUNT(*) AS encounter_rows,
       COUNT(DISTINCT patient_id) AS unique_patients
FROM encounters;

-- One row per department.
SELECT d.department_name,
       COUNT(e.encounter_id) AS encounter_count,
       COUNT(e.systolic_bp) AS nonmissing_sbp_n,
       ROUND(AVG(e.systolic_bp),1) AS mean_sbp
FROM departments d
LEFT JOIN encounters e ON e.department_id=d.department_id
GROUP BY d.department_id,d.department_name
ORDER BY encounter_count DESC;

-- Pre-aggregate child tables before joining to avoid fan-out.
WITH rx AS (
 SELECT encounter_id,COUNT(*) AS prescription_count
 FROM prescriptions GROUP BY encounter_id
),
dx AS (
 SELECT encounter_id,COUNT(*) AS diagnosis_count
 FROM diagnoses GROUP BY encounter_id
)
SELECT e.encounter_id,
       COALESCE(rx.prescription_count,0) AS prescription_count,
       COALESCE(dx.diagnosis_count,0) AS diagnosis_count
FROM encounters e
LEFT JOIN rx ON rx.encounter_id=e.encounter_id
LEFT JOIN dx ON dx.encounter_id=e.encounter_id;

-- Latest result per encounter and test.
WITH ranked AS (
 SELECT lr.*,
        ROW_NUMBER() OVER (
          PARTITION BY encounter_id,test_code
          ORDER BY result_date DESC,result_id DESC
        ) AS rn
 FROM laboratory_results lr
)
SELECT encounter_id,test_code,test_name,result_value,unit,result_date
FROM ranked WHERE rn=1;

-- Explain a read-only query plan.
EXPLAIN (ANALYZE, BUFFERS)
SELECT encounter_id,patient_id,admission_date
FROM encounters
WHERE patient_id=10
ORDER BY admission_date;

-- Read-only safety: start with SELECT; do not paste destructive statements
-- into a production connection. Use a transaction and rollback for approved
-- test modifications in a disposable database.
