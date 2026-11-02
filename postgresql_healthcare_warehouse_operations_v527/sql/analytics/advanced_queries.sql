SET search_path TO hda, public;

-- 1. Encounter sequence and time since prior encounter.
SELECT patient_id, encounter_id, encounter_date,
       ROW_NUMBER() OVER(PARTITION BY patient_id ORDER BY encounter_date, encounter_id) AS encounter_number,
       encounter_date - LAG(encounter_date) OVER(PARTITION BY patient_id ORDER BY encounter_date, encounter_id) AS days_since_previous
FROM mart_encounter_summary
ORDER BY patient_id, encounter_number;

-- 2. Monthly systolic trend; explicit analyte and unit restrictions.
SELECT date_trunc('month',d.full_date)::date AS month_start,
       AVG(f.value_numeric) AS mean_systolic_mmHg, COUNT(*) AS n
FROM fact_observation f
JOIN dim_terminology t USING(terminology_key)
JOIN dim_date d USING(date_key)
WHERE t.source_code='8480-6' AND f.unit='mmHg'
GROUP BY 1 ORDER BY 1;

-- 3. Patient cohort utilisation.
SELECT patient_id, qualifying_encounters, first_qualifying_encounter, last_qualifying_encounter
FROM mart_patient_cohort ORDER BY qualifying_encounters DESC, patient_id;

-- 4. Detect duplicate current SCD2 rows (expected zero rows).
SELECT patient_id, COUNT(*) AS current_versions
FROM dim_patient WHERE is_current GROUP BY patient_id HAVING COUNT(*)>1;

-- 5. Audit historical patient versions.
SELECT patient_id,version,valid_from,valid_to,is_current
FROM dim_patient ORDER BY patient_id,version;

-- 6. Explain plan for patient/date access path. Review actual plans on representative data.
EXPLAIN (ANALYZE, BUFFERS)
SELECT patient_key,date_key,value_numeric,unit FROM fact_observation
WHERE patient_key=1 ORDER BY date_key;
