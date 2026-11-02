-- SIM-02 solution — SQLite
SELECT department, COUNT(*) AS encounter_count,
       ROUND(AVG(length_of_stay_days),2) AS mean_los_days
FROM encounters
GROUP BY department
ORDER BY encounter_count DESC, department;

SELECT therapeutic_class, order_status, COUNT(*) AS order_count
FROM medication_orders
GROUP BY therapeutic_class, order_status
ORDER BY therapeutic_class, order_status;

SELECT COUNT(DISTINCT encounter_id) AS encounters_with_orders
FROM medication_orders;

WITH order_counts AS (
  SELECT encounter_id, COUNT(*) AS medication_order_count
  FROM medication_orders
  GROUP BY encounter_id
)
SELECT e.department,
       COUNT(*) AS encounter_count,
       SUM(COALESCE(o.medication_order_count,0)) AS medication_order_count,
       SUM(CASE WHEN COALESCE(o.medication_order_count,0)>0 THEN 1 ELSE 0 END) AS encounters_with_orders
FROM encounters e
LEFT JOIN order_counts o ON e.encounter_id=o.encounter_id
GROUP BY e.department
ORDER BY e.department;
