-- Worked reference queries; run after schema.sql and seed.sql.
-- Run after schema.sql and seed.sql
SET search_path TO hda, public;
-- PG-04A: preserve encounter grain while counting orders
SELECT d.department_name, COUNT(DISTINCT e.encounter_id) AS encounters,
       COUNT(o.order_id) AS medication_orders
FROM departments d LEFT JOIN encounters e USING(department_id)
LEFT JOIN medication_orders o USING(encounter_id)
GROUP BY d.department_name ORDER BY encounters DESC;
-- PG-04B: anti-join
SELECT e.encounter_id, e.admission_date, d.department_name
FROM encounters e JOIN departments d USING(department_id)
WHERE NOT EXISTS (SELECT 1 FROM medication_orders o WHERE o.encounter_id=e.encounter_id)
ORDER BY e.encounter_id;
-- PG-04C: window ranking
WITH class_counts AS (
 SELECT dr.therapeutic_class, COUNT(*) AS order_count
 FROM medication_orders o JOIN drugs dr USING(drug_id)
 GROUP BY dr.therapeutic_class
)
SELECT therapeutic_class, order_count,
       DENSE_RANK() OVER(ORDER BY order_count DESC) AS volume_rank
FROM class_counts ORDER BY volume_rank, therapeutic_class;
-- PG-04D: compare departments with the mean of department means
WITH dept AS (
 SELECT d.department_name, AVG(e.length_of_stay_days) AS mean_los
 FROM encounters e JOIN departments d USING(department_id)
 GROUP BY d.department_name
)
SELECT department_name, ROUND(mean_los,2) AS mean_los,
       ROUND(AVG(mean_los) OVER(),2) AS mean_of_department_means
FROM dept ORDER BY mean_los DESC;
-- PG-04E: set operation
SELECT encounter_id FROM encounters WHERE readmission_30d_flag IS TRUE
UNION
SELECT encounter_id FROM encounters WHERE length_of_stay_days >= 7;
-- PG-05: utilisation metrics with explicit denominator
SELECT COUNT(*) AS orders, COUNT(DISTINCT encounter_id) AS encounters_with_orders,
       ROUND(COUNT(*)::numeric/NULLIF(COUNT(DISTINCT encounter_id),0),2) AS orders_per_ordered_encounter,
       COUNT(DISTINCT drug_id) AS distinct_drugs, SUM(quantity) AS ordered_quantity,
       ROUND(SUM(quantity*unit_cost_inr),2) AS synthetic_order_value_inr
FROM medication_orders;
SELECT COUNT(*) FILTER (WHERE readmission_30d_flag IS TRUE) AS supplied_flag_yes,
       COUNT(*) AS encounter_denominator,
       ROUND(100.0*COUNT(*) FILTER (WHERE readmission_30d_flag IS TRUE)/NULLIF(COUNT(*),0),2) AS supplied_flag_percent
FROM encounters;
SELECT d.department_name, dr.therapeutic_class, COUNT(*) AS order_count
FROM medication_orders o JOIN encounters e USING(encounter_id)
JOIN departments d USING(department_id) JOIN drugs dr USING(drug_id)
GROUP BY d.department_name, dr.therapeutic_class
ORDER BY d.department_name, order_count DESC;
