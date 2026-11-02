-- Portable SQL reference (SQLite/PostgreSQL-style; adjust date functions if needed)
CREATE VIEW vw_encounter_department AS
SELECT department, site,
       COUNT(DISTINCT encounter_id) AS encounter_count,
       COUNT(DISTINCT patient_id) AS distinct_patient_count,
       AVG(length_of_stay_days) AS mean_los_days,
       AVG(CAST(readmission_30d AS REAL)) * 100.0 AS synthetic_readmission_flag_pct
FROM encounters
GROUP BY department, site;

CREATE VIEW vw_medication_class AS
SELECT drug_class,
       COUNT(DISTINCT order_id) AS order_lines,
       SUM(CASE WHEN generic_documented = 1 THEN 1 ELSE 0 END) AS generic_documented,
       100.0 * SUM(CASE WHEN generic_documented = 1 THEN 1 ELSE 0 END) / COUNT(*) AS generic_documentation_pct
FROM medication_orders
GROUP BY drug_class;

-- Validate before combining facts: medication_orders is at order-line grain.
