-- SQLite query templates. Replace table/column names to match your data.
-- Encounter volume by department
SELECT department, COUNT(*) AS encounters
FROM encounters
GROUP BY department
ORDER BY encounters DESC;

-- Unique patients by department (patient-level count)
SELECT department, COUNT(DISTINCT patient_id) AS unique_patients
FROM encounters
WHERE patient_id IS NOT NULL AND TRIM(patient_id) <> ''
GROUP BY department;

-- Average calendar-day LOS among discharged encounters
SELECT AVG(julianday(discharge_date) - julianday(admit_date)) AS mean_los_days
FROM encounters
WHERE disposition = 'Discharged';

-- Missing SBP count and completeness
SELECT COUNT(*) AS total_encounters,
       SUM(CASE WHEN sbp IS NOT NULL AND TRIM(CAST(sbp AS TEXT)) <> '' THEN 1 ELSE 0 END) AS sbp_recorded
FROM encounters;
