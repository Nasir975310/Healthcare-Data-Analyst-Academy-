-- Healthcare warehouse analytical SQL examples (SQLite-compatible)
-- 1. Encounter-level BP trends: restrict to systolic code and unit before analysis.
SELECT d.full_date, AVG(f.value_numeric) AS mean_systolic_mmHg, COUNT(*) AS observations
FROM fact_observation f
JOIN dim_terminology t USING(terminology_key)
JOIN dim_date d USING(date_key)
WHERE t.source_code='8480-6' AND f.unit='mmHg'
GROUP BY d.full_date ORDER BY d.full_date;

-- 2. Patient-level encounter sequence using a window function.
SELECT patient_id, encounter_id, encounter_date,
       ROW_NUMBER() OVER(PARTITION BY patient_id ORDER BY encounter_date, encounter_id) AS encounter_sequence,
       LAG(encounter_date) OVER(PARTITION BY patient_id ORDER BY encounter_date, encounter_id) AS previous_encounter_date
FROM mart_encounter_summary
ORDER BY patient_id, encounter_sequence;

-- 3. Cohort utilization summary.
SELECT c.patient_id, c.qualifying_encounters, c.first_qualifying_encounter,
       c.last_qualifying_encounter
FROM mart_patient_cohort c
ORDER BY c.qualifying_encounters DESC, c.patient_id;

-- 4. Data reconciliation: every source Observation should land in the observation fact.
SELECT (SELECT COUNT(*) FROM fact_observation) AS warehouse_rows,
       (SELECT COUNT(*) FROM stg_observations) AS staging_rows;
