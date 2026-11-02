-- Synthetic training data only. Import the CSV to a table named encounters.
-- 1. Row count and unique encounters
SELECT COUNT(*) AS rows, COUNT(DISTINCT encounter_id) AS unique_encounters
FROM encounters;

-- 2. Encounter count by department
SELECT department, COUNT(*) AS encounters
FROM encounters
GROUP BY department
ORDER BY encounters DESC;

-- 3. Mean length of stay by department
SELECT department, ROUND(AVG(length_of_stay_days), 2) AS mean_los_days
FROM encounters
GROUP BY department
ORDER BY mean_los_days DESC;

-- 4. Missingness in discharge disposition
SELECT COUNT(*) AS missing_disposition
FROM encounters
WHERE discharge_disposition IS NULL OR TRIM(discharge_disposition) = '';
