-- Inspect before/after index design using EXPLAIN (ANALYZE, BUFFERS).
EXPLAIN (ANALYZE, BUFFERS)
SELECT department_key,COUNT(*)
FROM analytics.fact_encounter
WHERE date_key BETWEEN 20260101 AND 20261231
GROUP BY department_key;

-- Candidate composite index; justify using workload evidence, not habit.
CREATE INDEX IF NOT EXISTS ix_fact_date_dept_cover
ON analytics.fact_encounter(date_key,department_key) INCLUDE(los_days,encounter_count);

-- Inspect index use and table size (requires permissions).
SELECT schemaname,tablename,indexname,idx_scan,idx_tup_read,idx_tup_fetch
FROM pg_stat_user_indexes WHERE schemaname='analytics';
