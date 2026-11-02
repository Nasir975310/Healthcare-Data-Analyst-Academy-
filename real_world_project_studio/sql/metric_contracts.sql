-- SQLite-compatible metric contract examples
-- Encounter grain: one row per encounter_id, not one row per patient.
-- Numerator/denominator for supplied flag rate must be explicitly labelled as unvalidated.
SELECT COUNT(*) AS encounter_rows,
       COUNT(DISTINCT encounter_id) AS distinct_encounters,
       COUNT(DISTINCT patient_id) AS distinct_patients,
       ROUND(AVG(length_of_stay_days),2) AS mean_los_days,
       ROUND(100.0*SUM(readmission_flag)/COUNT(*),2) AS supplied_flag_rate_pct
FROM operations_encounters;

-- Safe department metrics: aggregate encounter fact before joining any one-to-many fact.
SELECT department, COUNT(DISTINCT encounter_id) AS encounters,
       ROUND(AVG(length_of_stay_days),2) AS mean_los_days
FROM operations_encounters
GROUP BY department ORDER BY encounters DESC;
