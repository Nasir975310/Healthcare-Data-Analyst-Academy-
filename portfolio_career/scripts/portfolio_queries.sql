-- SQLite-compatible portfolio queries. Run against tables loaded from CSV.
-- 1. Encounter-level LOS and readmission flag summary
SELECT department, COUNT(DISTINCT encounter_id) AS encounters,
       ROUND(AVG(julianday(discharge_date)-julianday(admit_date)),2) AS mean_los_days,
       SUM(readmit_30d_flag) AS supplied_readmit_flags
FROM hospital_operations GROUP BY department ORDER BY encounters DESC;

-- 2. Pharmacy utilisation, preserving order-line grain
SELECT therapeutic_class, COUNT(DISTINCT order_id) AS order_lines,
       SUM(quantity) AS quantity,
       ROUND(SUM(quantity*unit_cost_inr),2) AS extended_cost_inr
FROM pharmacy_orders GROUP BY therapeutic_class ORDER BY extended_cost_inr DESC;

-- 3. Explicit orphan-order audit (do not inner-join these away)
SELECT o.* FROM pharmacy_orders o
LEFT JOIN hospital_operations e ON e.encounter_id=o.encounter_id
WHERE e.encounter_id IS NULL;

-- 4. Avoid join fan-out: aggregate orders before joining to encounter grain
WITH order_by_encounter AS (
 SELECT encounter_id, COUNT(DISTINCT order_id) AS order_lines,
        SUM(quantity*unit_cost_inr) AS order_value_inr
 FROM pharmacy_orders GROUP BY encounter_id
)
SELECT e.department, COUNT(DISTINCT e.encounter_id) AS encounters,
       SUM(COALESCE(o.order_lines,0)) AS order_lines,
       ROUND(SUM(COALESCE(o.order_value_inr,0)),2) AS order_value_inr
FROM hospital_operations e LEFT JOIN order_by_encounter o USING(encounter_id)
GROUP BY e.department;
