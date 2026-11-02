-- Healthcare Analytics SQL Practice (SQLite)
-- Run in DBeaver after opening healthcare_analytics_practice.db.
-- Each query is read-only. Do not run destructive statements on source data.

-- 1. Inspect rows and columns
SELECT * FROM encounters LIMIT 10;

-- 2. Select a subset with explicit columns and aliases
SELECT encounter_id, patient_id, admission_date AS visit_date, encounter_type
FROM encounters
ORDER BY admission_date DESC, encounter_id
LIMIT 15;

-- 3. Filter a cohort; parentheses make logic explicit
SELECT encounter_id, patient_id, systolic_bp, diastolic_bp
FROM encounters
WHERE encounter_type = 'IPD'
  AND (systolic_bp >= 140 OR diastolic_bp >= 90)
ORDER BY systolic_bp DESC;

-- 4. Handle NULL explicitly
SELECT COUNT(*) AS encounter_rows,
       COUNT(systolic_bp) AS nonmissing_sbp,
       COUNT(*) - COUNT(systolic_bp) AS missing_sbp
FROM encounters;

-- 5. Conditional classification
SELECT encounter_id, systolic_bp,
       CASE WHEN systolic_bp IS NULL THEN 'Missing'
            WHEN systolic_bp >= 140 THEN 'At or above 140'
            ELSE 'Below 140' END AS sbp_band
FROM encounters;

-- 6. Aggregate at a declared grain: one row per encounter type
SELECT encounter_type, COUNT(*) AS encounters,
       ROUND(AVG(length_of_stay_days),2) AS mean_los_days
FROM encounters
GROUP BY encounter_type
ORDER BY encounters DESC;

-- 7. HAVING filters groups, WHERE filters source rows
SELECT department_id, COUNT(*) AS encounter_count
FROM encounters
WHERE admission_date >= '2026-01-01'
GROUP BY department_id
HAVING COUNT(*) >= 5;

-- 8. Join encounters to patient and department dimensions
SELECT e.encounter_id, p.synthetic_patient_code,
       d.department_name, e.admission_date, e.encounter_type
FROM encounters e
JOIN patients p ON p.patient_id=e.patient_id
JOIN departments d ON d.department_id=e.department_id
ORDER BY e.encounter_id
LIMIT 20;

-- 9. LEFT JOIN retains encounters without a matching prescription
SELECT e.encounter_id, COUNT(rx.prescription_id) AS prescription_count
FROM encounters e
LEFT JOIN prescriptions rx ON rx.encounter_id=e.encounter_id
GROUP BY e.encounter_id
ORDER BY prescription_count, e.encounter_id;

-- 10. Avoid join fan-out: aggregate child records before joining
WITH rx_counts AS (
 SELECT encounter_id, COUNT(*) AS prescription_count
 FROM prescriptions GROUP BY encounter_id
),
diag_counts AS (
 SELECT encounter_id, COUNT(*) AS diagnosis_count
 FROM diagnoses GROUP BY encounter_id
)
SELECT e.encounter_id,
       COALESCE(r.prescription_count,0) AS prescription_count,
       COALESCE(d.diagnosis_count,0) AS diagnosis_count
FROM encounters e
LEFT JOIN rx_counts r ON r.encounter_id=e.encounter_id
LEFT JOIN diag_counts d ON d.encounter_id=e.encounter_id;

-- 11. Subquery: patients with at least two encounters
SELECT patient_id, COUNT(*) AS encounter_count
FROM encounters
GROUP BY patient_id
HAVING COUNT(*) >= 2;

-- 12. CTE: department-level summary
WITH department_summary AS (
 SELECT department_id, COUNT(*) AS encounter_count,
        AVG(systolic_bp) AS mean_sbp
 FROM encounters GROUP BY department_id
)
SELECT d.department_name, s.encounter_count, ROUND(s.mean_sbp,1) AS mean_sbp
FROM department_summary s
JOIN departments d ON d.department_id=s.department_id
ORDER BY s.encounter_count DESC;

-- 13. Window function: rank encounters by SBP within department
SELECT encounter_id, department_id, systolic_bp,
       DENSE_RANK() OVER (
         PARTITION BY department_id ORDER BY systolic_bp DESC
       ) AS sbp_rank_in_department
FROM encounters
WHERE systolic_bp IS NOT NULL;

-- 14. Window function: sequence encounters per patient
SELECT patient_id, encounter_id, admission_date,
       ROW_NUMBER() OVER (
         PARTITION BY patient_id ORDER BY admission_date, encounter_id
       ) AS encounter_sequence
FROM encounters;

-- 15. Latest lab result per encounter and test
WITH ranked_labs AS (
 SELECT *, ROW_NUMBER() OVER (
   PARTITION BY encounter_id, test_code
   ORDER BY result_date DESC, result_id DESC
 ) AS rn
 FROM laboratory_results
)
SELECT encounter_id, test_code, test_name, result_value, unit
FROM ranked_labs WHERE rn=1;

-- 16. Cohort-level readmission proportion among eligible IPD rows
SELECT COUNT(*) AS eligible_ipd_encounters,
       SUM(readmitted_30d) AS recorded_readmissions,
       ROUND(1.0*SUM(readmitted_30d)/NULLIF(COUNT(readmitted_30d),0),3)
         AS proportion_among_known_status
FROM encounters
WHERE encounter_type='IPD' AND readmitted_30d IS NOT NULL;
