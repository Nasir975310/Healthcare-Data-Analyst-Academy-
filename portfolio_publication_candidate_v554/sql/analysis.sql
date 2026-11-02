-- SQLite 3.x. Run after src/run_project.py has created outputs/analytics.sqlite.
-- Grain: one deduplicated encounter per encounter_id.
SELECT status, COUNT(*) AS encounter_rows
FROM encounters_deduplicated
GROUP BY status
ORDER BY status;

SELECT department,
       COUNT(*) AS completed_encounters,
       COUNT(wait_minutes) AS valid_wait_n,
       ROUND(AVG(wait_minutes), 2) AS mean_wait_minutes
FROM encounters_deduplicated
WHERE status = 'completed'
  AND department IS NOT NULL AND TRIM(department) <> ''
  AND encounter_date IS NOT NULL
  AND wait_minutes IS NOT NULL AND wait_minutes >= 0
GROUP BY department
ORDER BY department;

SELECT encounter_id, COUNT(*) AS source_rows
FROM encounters_deduplicated
GROUP BY encounter_id
HAVING COUNT(*) > 1;
