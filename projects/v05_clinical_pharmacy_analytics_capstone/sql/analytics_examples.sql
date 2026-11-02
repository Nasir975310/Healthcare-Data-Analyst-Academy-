-- V05 synthetic capstone SQL examples
-- Adapt date syntax to your SQL engine. Keep each table at its native grain.

-- 1. Encounter summary: one row per department
SELECT department,
       COUNT(DISTINCT encounter_id) AS encounters,
       COUNT(DISTINCT patient_id) AS distinct_patients,
       AVG(length_of_stay_days) AS mean_los_days
FROM encounters
GROUP BY department
ORDER BY encounters DESC;

-- 2. Medication order lines by class
SELECT drug_class,
       COUNT(DISTINCT order_id) AS order_lines,
       SUM(CASE WHEN generic_name_documented = 1 THEN 1 ELSE 0 END) AS generic_documented
FROM medication_orders
GROUP BY drug_class
ORDER BY order_lines DESC;

-- 3. Laboratory result profiling: keep analyte and unit separate
SELECT analyte, unit, status,
       COUNT(*) AS result_rows,
       AVG(value) AS mean_value
FROM laboratory_results
GROUP BY analyte, unit, status;

-- Never join all four raw tables before aggregation: one-to-many joins multiply rows.
