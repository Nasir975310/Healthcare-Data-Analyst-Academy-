-- SQLite-compatible starter. Inspect key uniqueness and cardinality first.
SELECT COUNT(*) AS encounter_rows,
       COUNT(DISTINCT encounter_id) AS distinct_encounters
FROM encounters;

SELECT COUNT(*) AS order_rows,
       COUNT(DISTINCT order_id) AS distinct_orders,
       COUNT(DISTINCT encounter_id) AS encounters_referenced
FROM medication_orders;

-- Find orphan medication-order references.
SELECT mo.*
FROM medication_orders mo
LEFT JOIN encounters e ON e.encounter_id = mo.encounter_id
WHERE e.encounter_id IS NULL;

-- Compare unsafe joined row count with the intended encounter grain.
SELECT COUNT(*) AS joined_rows,
       COUNT(DISTINCT e.encounter_id) AS distinct_encounters
FROM encounters e
LEFT JOIN medication_orders mo ON mo.encounter_id = e.encounter_id;

-- TODO: pre-aggregate orders by encounter before joining encounter-level measures.
