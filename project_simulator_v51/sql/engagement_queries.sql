-- Import encounters_accepted.csv into a table named encounters_accepted.
-- If using SQLite CLI, import the CSV after creating the table with matching column names.
SELECT department,
       COUNT(*) AS encounters,
       COUNT(DISTINCT patient_id) AS unique_patients
FROM encounters_accepted
WHERE department <> 'Emergency'
GROUP BY department
ORDER BY department;

SELECT disposition, COUNT(*) AS encounters,
       ROUND(100.0*COUNT(*)/(SELECT COUNT(*) FROM encounters_accepted),2) AS share_pct
FROM encounters_accepted
GROUP BY disposition
ORDER BY encounters DESC;

SELECT COUNT(*) AS discharged_encounters,
       ROUND(AVG(julianday(discharge_date)-julianday(admit_date)),2) AS average_los_calendar_days
FROM encounters_accepted
WHERE disposition='Discharged';

SELECT COUNT(*) AS accepted_encounters,
       SUM(CASE WHEN NULLIF(TRIM(sbp),'') IS NOT NULL THEN 1 ELSE 0 END) AS with_sbp,
       ROUND(100.0*SUM(CASE WHEN NULLIF(TRIM(sbp),'') IS NOT NULL THEN 1 ELSE 0 END)/COUNT(*),2) AS sbp_completeness_pct
FROM encounters_accepted;
