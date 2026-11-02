-- Run after the Python pipeline creates deliverables/hospital_analytics.sqlite.
-- 1. Monthly activity
SELECT substr(encounter_date,1,7) AS month, COUNT(*) AS encounters,
       SUM(status='Completed') AS completed,
       SUM(status='Cancelled') AS cancelled,
       SUM(status='Scheduled') AS scheduled
FROM fact_encounter GROUP BY 1 ORDER BY 1;

-- 2. Medication class mix (orders, not dispensing or adherence)
SELECT drug_class, COUNT(*) AS medication_orders
FROM fact_medication GROUP BY drug_class ORDER BY medication_orders DESC;

-- 3. BP values paired at encounter grain
SELECT encounter_id,
       MAX(CASE WHEN measure='Systolic BP' THEN value END) AS systolic_mmHg,
       MAX(CASE WHEN measure='Diastolic BP' THEN value END) AS diastolic_mmHg
FROM fact_observation GROUP BY encounter_id;

-- 4. Orphan encounter records retained in staging, not curated fact
SELECT s.* FROM stg_encounter s
LEFT JOIN dim_patient p ON p.patient_id=s.patient_id
WHERE p.patient_id IS NULL;

-- 5. Compare staging and curated counts
SELECT (SELECT COUNT(*) FROM stg_encounter) AS staged,
       (SELECT COUNT(*) FROM fact_encounter) AS curated;
