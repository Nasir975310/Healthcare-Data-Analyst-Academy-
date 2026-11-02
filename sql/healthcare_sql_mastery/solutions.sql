-- Healthcare SQL Mastery: reference solutions (SQLite)

-- SQL-01 | Inspect the tables and establish the grain
SELECT 'encounters' AS table_name,
       COUNT(*) AS row_count,
       COUNT(DISTINCT encounter_id) AS distinct_key_count
FROM encounters
UNION ALL
SELECT 'medication_orders', COUNT(*), COUNT(DISTINCT order_id)
FROM medication_orders;


-- SQL-02 | Filter a defined reporting period
SELECT encounter_id, admission_date, department, length_of_stay_days
FROM encounters
WHERE admission_date >= '2026-01-01'
  AND admission_date < '2026-04-01'
ORDER BY admission_date DESC, encounter_id;


-- SQL-03 | Build department-level operational metrics
SELECT department,
       COUNT(*) AS encounter_count,
       ROUND(AVG(length_of_stay_days), 2) AS mean_los_days
FROM encounters
GROUP BY department
ORDER BY encounter_count DESC, department;


-- SQL-04 | Find therapeutic classes with high order volume
SELECT therapeutic_class, COUNT(*) AS order_count
FROM medication_orders
GROUP BY therapeutic_class
HAVING COUNT(*) >= 20
ORDER BY order_count DESC, therapeutic_class;


-- SQL-05 | Join encounters to medication orders safely
SELECT e.department,
       COUNT(m.order_id) AS medication_order_count
FROM encounters e
INNER JOIN medication_orders m
  ON e.encounter_id = m.encounter_id
GROUP BY e.department
ORDER BY medication_order_count DESC, e.department;


-- SQL-06 | Measure encounter coverage with LEFT JOIN
WITH order_counts AS (
  SELECT encounter_id, COUNT(*) AS order_count
  FROM medication_orders
  GROUP BY encounter_id
)
SELECT e.department,
       COUNT(*) AS total_encounters,
       SUM(CASE WHEN COALESCE(o.order_count, 0) > 0 THEN 1 ELSE 0 END) AS encounters_with_orders,
       SUM(CASE WHEN COALESCE(o.order_count, 0) = 0 THEN 1 ELSE 0 END) AS encounters_without_orders
FROM encounters e
LEFT JOIN order_counts o ON e.encounter_id = o.encounter_id
GROUP BY e.department
ORDER BY e.department;


-- SQL-07 | Create an encounter-level medication summary
WITH orders_per_encounter AS (
  SELECT encounter_id, COUNT(*) AS order_count
  FROM medication_orders
  GROUP BY encounter_id
)
SELECT e.encounter_id, e.department, e.length_of_stay_days,
       COALESCE(o.order_count, 0) AS order_count
FROM encounters e
LEFT JOIN orders_per_encounter o
  ON e.encounter_id = o.encounter_id
ORDER BY e.encounter_id;


-- SQL-08 | Rank departments by mean length of stay
WITH dept_metrics AS (
  SELECT department,
         COUNT(*) AS encounter_count,
         AVG(length_of_stay_days) AS mean_los
  FROM encounters
  GROUP BY department
)
SELECT department, encounter_count,
       ROUND(mean_los, 2) AS mean_los_days,
       DENSE_RANK() OVER (ORDER BY mean_los DESC) AS los_rank
FROM dept_metrics
ORDER BY los_rank, department;


-- SQL-09 | Calculate the supplied 30-day flag proportion
SELECT COUNT(*) AS total_encounters,
       SUM(CASE WHEN readmission_30d_flag = 1 THEN 1 ELSE 0 END) AS flagged_encounters,
       ROUND(100.0 * SUM(CASE WHEN readmission_30d_flag = 1 THEN 1 ELSE 0 END)
             / NULLIF(COUNT(*), 0), 2) AS supplied_flag_percent
FROM encounters;


-- SQL-10 | Run key, chronology and referential-integrity checks
SELECT COUNT(*) AS duplicate_encounter_keys FROM (
  SELECT encounter_id FROM encounters GROUP BY encounter_id HAVING COUNT(*) > 1
);
SELECT COUNT(*) AS duplicate_order_keys FROM (
  SELECT order_id FROM medication_orders GROUP BY order_id HAVING COUNT(*) > 1
);
SELECT COUNT(*) AS invalid_encounter_chronology
FROM encounters WHERE discharge_date < admission_date;
SELECT COUNT(*) AS orphan_orders
FROM medication_orders m
WHERE NOT EXISTS (SELECT 1 FROM encounters e WHERE e.encounter_id = m.encounter_id);


-- SQL-11 | Inspect a query plan and justify an index
CREATE INDEX IF NOT EXISTS idx_orders_class_status
ON medication_orders(therapeutic_class, order_status);

EXPLAIN QUERY PLAN
SELECT order_id, order_date, drug_name
FROM medication_orders
WHERE therapeutic_class = 'Statin'
  AND order_status = 'Active';
