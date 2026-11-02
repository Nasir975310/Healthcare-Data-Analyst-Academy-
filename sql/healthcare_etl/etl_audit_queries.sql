-- Healthcare Data Analyst Academy v2.4.0 — ETL audit queries
-- Run against assignments/outputs/healthcare_etl_training.db in SQLite.

-- 1. Latest pipeline runs
SELECT run_id, source_mode, encounter_rows, order_rows, loaded_encounters,
       loaded_orders, quarantined_orders, status, finished_at
FROM etl_run_log
ORDER BY finished_at DESC;

-- 2. Encounter mart grain check
SELECT COUNT(*) AS rows, COUNT(DISTINCT encounter_id) AS distinct_keys
FROM mart_encounters;

-- 3. Medication order mart grain check
SELECT COUNT(*) AS rows, COUNT(DISTINCT order_id) AS distinct_keys
FROM mart_medication_orders;

-- 4. Quarantined order records and reasons
SELECT order_id, encounter_id, reason
FROM quarantine_orders
ORDER BY order_id;

-- 5. Data-quality findings by run
SELECT run_id, dataset, field, rule, severity, issue_count, detail
FROM data_quality_results
ORDER BY run_id DESC, severity, dataset, field;

-- 6. Encounter-level order count (left join preserves zero-order encounters)
SELECT e.encounter_id, COUNT(o.order_id) AS order_count
FROM mart_encounters e
LEFT JOIN mart_medication_orders o ON o.encounter_id=e.encounter_id
GROUP BY e.encounter_id
ORDER BY order_count DESC, e.encounter_id;

-- 7. Monthly order quantity
SELECT substr(order_date,1,7) AS order_month, SUM(quantity) AS ordered_quantity
FROM mart_medication_orders
GROUP BY substr(order_date,1,7)
ORDER BY order_month;

-- 8. Do not infer dispensing/administration/adherence from order records.
