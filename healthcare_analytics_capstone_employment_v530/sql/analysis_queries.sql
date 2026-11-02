-- SQLite-compatible analytical checks; all source data are synthetic.
-- 1. Encounter volume by month and status.
SELECT substr(encounter_date,1,7) AS year_month, status, COUNT(*) AS encounters
FROM fact_encounter GROUP BY 1,2 ORDER BY 1,2;

-- 2. Encounter counts by type.
SELECT encounter_type, COUNT(*) AS encounters
FROM fact_encounter GROUP BY encounter_type ORDER BY encounters DESC;

-- 3. Medication utilization by drug class.
SELECT drug_class, COUNT(*) AS orders, COUNT(DISTINCT encounter_id) AS encounters
FROM fact_medication GROUP BY drug_class ORDER BY orders DESC;

-- 4. BP descriptive summary by encounter (do not interpret as diagnostic/control status).
SELECT encounter_id,
 MAX(CASE WHEN measure='Systolic BP' THEN value END) AS systolic_mmHg,
 MAX(CASE WHEN measure='Diastolic BP' THEN value END) AS diastolic_mmHg
FROM fact_observation GROUP BY encounter_id;

-- 5. Referential integrity exceptions.
SELECT e.encounter_id, e.patient_id FROM fact_encounter e
LEFT JOIN dim_patient p ON p.patient_id=e.patient_id WHERE p.patient_id IS NULL;
