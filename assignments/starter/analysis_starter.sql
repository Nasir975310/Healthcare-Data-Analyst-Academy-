-- SIM-02: SQL prescribing and encounter analysis
-- Import the supplied CSV files into SQLite tables named:
--   encounters
--   medication_orders
-- All records are synthetic.

-- 1. Check source row counts.
SELECT 'encounters' AS table_name, COUNT(*) AS row_count FROM encounters
UNION ALL
SELECT 'medication_orders', COUNT(*) FROM medication_orders;

-- 2. Check encounter and order key uniqueness.
SELECT COUNT(*) AS rows, COUNT(DISTINCT encounter_id) AS unique_encounters
FROM encounters;

SELECT COUNT(*) AS rows, COUNT(DISTINCT order_id) AS unique_orders
FROM medication_orders;

-- 3. TODO: encounter count by department.

-- 4. TODO: order count by therapeutic class and order status.

-- 5. TODO: count unique encounters represented in the order table.

-- 6. TODO: aggregate orders per encounter in a CTE before joining
--    to encounter-level information. Explain why this avoids
--    treating order rows as unique encounters.
