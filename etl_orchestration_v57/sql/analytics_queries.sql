-- Curated synthetic encounter analytics
SELECT department, COUNT(*) AS encounters, ROUND(AVG(CAST(los_days AS REAL)),2) AS mean_los_days
FROM curated_encounters GROUP BY department ORDER BY encounters DESC;

SELECT disposition, COUNT(*) AS encounters
FROM curated_encounters GROUP BY disposition ORDER BY encounters DESC;

SELECT COUNT(*) AS curated_rows, COUNT(DISTINCT encounter_id) AS unique_encounters
FROM curated_encounters;
