-- Run against data/processed/hospital_analytics.sqlite
SELECT department, COUNT(*) AS encounters,
       ROUND(AVG(length_of_stay_days), 2) AS mean_los_days
FROM encounters
GROUP BY department
ORDER BY encounters DESC;

SELECT discharge_disposition, COUNT(*) AS encounters
FROM encounters
GROUP BY discharge_disposition
ORDER BY encounters DESC;

SELECT age_band, COUNT(*) AS encounters,
       ROUND(AVG(length_of_stay_days), 2) AS mean_los_days
FROM encounters
GROUP BY age_band
ORDER BY age_band;

-- Reconciliation: must equal accepted_rows in quality_report.json
SELECT COUNT(*) AS sqlite_rows,
       COUNT(DISTINCT encounter_id) AS unique_encounters
FROM encounters;
