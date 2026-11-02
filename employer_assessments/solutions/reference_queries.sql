-- SQLite reference solutions for EMP-01.
-- Load encounters.csv as encounters and medication_orders.csv as medication_orders.

-- A. Confirm grain and keys
SELECT COUNT(*) AS row_count, COUNT(DISTINCT encounter_id) AS unique_encounters FROM encounters;
SELECT COUNT(*) AS row_count, COUNT(DISTINCT order_id) AS unique_orders FROM medication_orders;

-- B. Encounter metrics
SELECT department, COUNT(DISTINCT encounter_id) encounters,
 ROUND(AVG(julianday(discharge_date)-julianday(admit_date)),2) mean_los_days,
 SUM(readmission_30d) supplied_flag_count
FROM encounters GROUP BY department ORDER BY encounters DESC;

-- C. Order class metrics across all statuses. State whether this is appropriate.
SELECT drug_class, COUNT(DISTINCT order_id) order_lines,
 SUM(quantity) quantity, ROUND(SUM(quantity*unit_cost),2) extended_cost
FROM medication_orders GROUP BY drug_class;

-- D. Orphan orders
SELECT COUNT(*) orphan_lines, ROUND(SUM(m.quantity*m.unit_cost),2) orphan_value
FROM medication_orders m LEFT JOIN encounters e USING(encounter_id)
WHERE e.encounter_id IS NULL;

-- E. Safe pre-aggregation before encounter-grain join
WITH orders_by_encounter AS (
 SELECT encounter_id, COUNT(DISTINCT order_id) order_lines,
 SUM(quantity*unit_cost) order_value
 FROM medication_orders GROUP BY encounter_id
)
SELECT e.department, COUNT(DISTINCT e.encounter_id) encounters,
 SUM(COALESCE(o.order_lines,0)) order_lines,
 ROUND(SUM(COALESCE(o.order_value,0)),2) order_value
FROM encounters e LEFT JOIN orders_by_encounter o USING(encounter_id)
GROUP BY e.department;

-- F. Order status distribution must be considered before interpreting cost
SELECT status, COUNT(*) order_lines, SUM(quantity) quantity,
 ROUND(SUM(quantity*unit_cost),2) value
FROM medication_orders GROUP BY status;
