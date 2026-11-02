-- SQLite reference queries for SIM-06. Inspect row counts before interpreting totals.
SELECT COUNT(*) AS raw_order_rows FROM medication_orders_raw;
SELECT COUNT(*) AS orphan_order_rows
FROM medication_orders_raw o
LEFT JOIN encounters_raw e ON e.encounter_id=o.encounter_id
WHERE e.encounter_id IS NULL;
SELECT
  COUNT(*) AS raw_rows,
  SUM(CASE WHEN CAST(quantity AS INTEGER)<=0 THEN 1 ELSE 0 END) AS nonpositive_quantity_rows,
  SUM(CASE WHEN unit_cost_inr IS NULL OR TRIM(unit_cost_inr)='' THEN 1 ELSE 0 END) AS missing_cost_rows,
  SUM(CASE WHEN therapeutic_class IS NULL OR TRIM(therapeutic_class)='' THEN 1 ELSE 0 END) AS missing_class_rows
FROM medication_orders_raw;
-- Do not sum order rows after joining to a non-unique encounter key without deduplication.
