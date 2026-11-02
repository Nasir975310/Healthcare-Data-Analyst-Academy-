-- Integrated Excel-SQL capstone: reproducible SQLite outputs
-- Reporting window: 2026-01-01 inclusive to 2026-04-01 exclusive.
-- Dataset is synthetic. Run each SELECT separately and export result grids.

-- A. Cohort inventory and grain reconciliation
SELECT COUNT(*) AS encounter_rows,
       COUNT(DISTINCT encounter_id) AS unique_encounters,
       COUNT(DISTINCT patient_id) AS unique_patients,
       MIN(admission_date) AS first_admission,
       MAX(admission_date) AS last_admission
FROM encounters
WHERE admission_date >= '2026-01-01'
  AND admission_date < '2026-04-01';

-- B. Encounter type summary
SELECT encounter_type,
       COUNT(*) AS encounter_count,
       COUNT(DISTINCT patient_id) AS unique_patients,
       ROUND(100.0*COUNT(*)/(SELECT COUNT(*) FROM encounters
         WHERE admission_date >= '2026-01-01' AND admission_date < '2026-04-01'),1) AS pct_of_encounters
FROM encounters
WHERE admission_date >= '2026-01-01'
  AND admission_date < '2026-04-01'
GROUP BY encounter_type
ORDER BY encounter_count DESC;

-- C. Department summary, including missing SBP denominator
SELECT d.department_name,
       COUNT(e.encounter_id) AS encounter_count,
       COUNT(e.systolic_bp) AS nonmissing_sbp_n,
       COUNT(e.encounter_id)-COUNT(e.systolic_bp) AS missing_sbp_n,
       ROUND(AVG(e.systolic_bp),1) AS mean_sbp
FROM departments d
LEFT JOIN encounters e
  ON e.department_id=d.department_id
 AND e.admission_date >= '2026-01-01'
 AND e.admission_date < '2026-04-01'
GROUP BY d.department_id,d.department_name
ORDER BY encounter_count DESC;

-- D. Inpatient LOS summary; OPD zero placeholders are excluded.
SELECT COUNT(*) AS inpatient_encounters,
       COUNT(length_of_stay_days) AS nonmissing_los_n,
       ROUND(AVG(length_of_stay_days),2) AS mean_los_days,
       MIN(length_of_stay_days) AS min_los_days,
       MAX(length_of_stay_days) AS max_los_days
FROM encounters
WHERE encounter_type='IPD'
  AND admission_date >= '2026-01-01'
  AND admission_date < '2026-04-01';

-- E. Readmission status among known IPD statuses only.
SELECT COUNT(*) AS ipd_with_known_status,
       SUM(readmitted_30d) AS recorded_readmissions,
       ROUND(100.0*SUM(readmitted_30d)/NULLIF(COUNT(readmitted_30d),0),1) AS pct_among_known_status
FROM encounters
WHERE encounter_type='IPD'
  AND admission_date >= '2026-01-01'
  AND admission_date < '2026-04-01'
  AND readmitted_30d IS NOT NULL;

-- F. Encounter-level medication counts, pre-aggregated to prevent fan-out.
WITH rx AS (
 SELECT encounter_id,COUNT(*) AS rx_count
 FROM prescriptions GROUP BY encounter_id
)
SELECT e.encounter_id,e.patient_id,e.admission_date,e.encounter_type,
       COALESCE(rx.rx_count,0) AS prescription_count
FROM encounters e
LEFT JOIN rx ON rx.encounter_id=e.encounter_id
WHERE e.admission_date >= '2026-01-01'
  AND e.admission_date < '2026-04-01'
ORDER BY e.admission_date,e.encounter_id;

-- G. Data-quality checks: duplicate encounter IDs and orphan child records.
SELECT encounter_id,COUNT(*) AS n
FROM encounters GROUP BY encounter_id HAVING COUNT(*)>1;

SELECT 'diagnoses' AS child_table,COUNT(*) AS orphan_rows
FROM diagnoses d LEFT JOIN encounters e ON e.encounter_id=d.encounter_id
WHERE e.encounter_id IS NULL
UNION ALL
SELECT 'prescriptions',COUNT(*)
FROM prescriptions p LEFT JOIN encounters e ON e.encounter_id=p.encounter_id
WHERE e.encounter_id IS NULL
UNION ALL
SELECT 'laboratory_results',COUNT(*)
FROM laboratory_results l LEFT JOIN encounters e ON e.encounter_id=l.encounter_id
WHERE e.encounter_id IS NULL;
