-- Advanced SQL investigation pack (SQLite 3.35+)
-- Tables: encounters, medication_orders, lab_observations.
-- 1. Grain and key profile
SELECT 'encounters' AS table_name, COUNT(*) AS rows, COUNT(DISTINCT encounter_id) AS distinct_keys FROM encounters
UNION ALL SELECT 'orders', COUNT(*), COUNT(DISTINCT order_id) FROM medication_orders
UNION ALL SELECT 'labs', COUNT(*), COUNT(DISTINCT observation_id) FROM lab_observations;

-- 2. Orphan medication orders (anti-join)
SELECT COUNT(*) AS orphan_order_rows
FROM medication_orders o LEFT JOIN encounters e ON e.encounter_id=o.encounter_id
WHERE e.encounter_id IS NULL;

-- 3. Department utilisation, with encounter denominator
WITH enc AS (
 SELECT department, COUNT(*) AS encounter_n, AVG(los_days) AS mean_los
 FROM encounters GROUP BY department
), ord AS (
 SELECT e.department, COUNT(*) AS order_n, SUM(o.quantity) AS quantity_total
 FROM encounters e JOIN medication_orders o ON o.encounter_id=e.encounter_id
 GROUP BY e.department
)
SELECT enc.department, enc.encounter_n, ROUND(enc.mean_los,2) AS mean_los_days,
       COALESCE(ord.order_n,0) AS order_n, COALESCE(ord.quantity_total,0) AS quantity_total
FROM enc LEFT JOIN ord ON ord.department=enc.department
ORDER BY enc.encounter_n DESC;

-- 4. Window function: rank departments by encounter volume
WITH d AS (SELECT department,COUNT(*) AS encounter_n FROM encounters GROUP BY department)
SELECT department,encounter_n,DENSE_RANK() OVER(ORDER BY encounter_n DESC) AS volume_rank
FROM d ORDER BY volume_rank,department;

-- 5. Patient-level first encounter cohort and 30-day supplied flag
WITH ranked AS (
 SELECT patient_id,encounter_id,admit_date,readmit_30d_flag,
        ROW_NUMBER() OVER(PARTITION BY patient_id ORDER BY admit_date,encounter_id) AS rn
 FROM encounters
)
SELECT COUNT(*) AS first_encounter_patients,
       SUM(readmit_30d_flag) AS supplied_flag_count,
       ROUND(100.0*SUM(readmit_30d_flag)/COUNT(*),2) AS supplied_flag_pct
FROM ranked WHERE rn=1;

-- 6. Monthly order trend, safe date grain
SELECT substr(order_date,1,7) AS month, COUNT(*) AS order_rows,
       COUNT(DISTINCT encounter_id) AS encounters_with_orders,
       SUM(quantity) AS total_quantity
FROM medication_orders
GROUP BY substr(order_date,1,7) ORDER BY month;

-- 7. Latest SBP observation per encounter using window ranking
WITH x AS (
 SELECT encounter_id,value,unit,observed_date,
        ROW_NUMBER() OVER(PARTITION BY encounter_id ORDER BY observed_date DESC,observation_id DESC) AS rn
 FROM lab_observations WHERE code='SBP'
)
SELECT COUNT(*) AS encounters_with_sbp, ROUND(AVG(value),2) AS mean_latest_sbp
FROM x WHERE rn=1;

-- 8. Data quality issue summary
SELECT
 SUM(CASE WHEN quantity<=0 THEN 1 ELSE 0 END) AS nonpositive_quantity,
 SUM(CASE WHEN unit_cost IS NULL THEN 1 ELSE 0 END) AS missing_unit_cost,
 SUM(CASE WHEN drug_class IS NULL OR TRIM(drug_class)='' THEN 1 ELSE 0 END) AS missing_drug_class
FROM medication_orders;

-- 9. Query plan / index lab: compare before and after index creation.
EXPLAIN QUERY PLAN SELECT * FROM medication_orders WHERE encounter_id='AE00001';
CREATE INDEX IF NOT EXISTS idx_orders_encounter_date ON medication_orders(encounter_id,order_date);
EXPLAIN QUERY PLAN SELECT * FROM medication_orders WHERE encounter_id='AE00001' AND order_date>='2025-06-01';

-- 10. CTE: encounters with both an SBP and medication order; avoid row multiplication.
WITH has_sbp AS (SELECT DISTINCT encounter_id FROM lab_observations WHERE code='SBP'),
has_order AS (SELECT DISTINCT encounter_id FROM medication_orders)
SELECT COUNT(*) AS encounters_with_both
FROM encounters e JOIN has_sbp s USING(encounter_id) JOIN has_order o USING(encounter_id);

-- 11. Safe aggregate: aggregate facts independently before joining.
WITH lab AS (
 SELECT encounter_id,AVG(value) AS mean_sbp
 FROM lab_observations WHERE code='SBP' GROUP BY encounter_id
), med AS (
 SELECT encounter_id,COUNT(*) AS order_n
 FROM medication_orders GROUP BY encounter_id
)
SELECT COUNT(*) AS encounter_n, ROUND(AVG(lab.mean_sbp),2) AS mean_encounter_sbp,
       SUM(med.order_n) AS total_orders
FROM encounters e LEFT JOIN lab USING(encounter_id) LEFT JOIN med USING(encounter_id);
