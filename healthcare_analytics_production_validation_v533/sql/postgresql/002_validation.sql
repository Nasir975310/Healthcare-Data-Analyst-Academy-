-- Duplicate encounter IDs in raw input
SELECT encounter_id, COUNT(*) AS n
FROM hda_raw.encounters
GROUP BY encounter_id HAVING COUNT(*) > 1;

-- Orphan patient references in raw input
SELECT r.source_row_id, r.encounter_id, r.patient_id
FROM hda_raw.encounters r
LEFT JOIN hda_curated.dim_patient p USING (patient_id)
WHERE p.patient_id IS NULL;

-- Curated-to-raw reconciliation (must explain exclusions)
SELECT
  (SELECT COUNT(*) FROM hda_raw.encounters) AS raw_rows,
  (SELECT COUNT(*) FROM hda_curated.fact_encounter) AS accepted_rows,
  (SELECT COUNT(*) FROM hda_curated.encounter_exceptions) AS exception_rows;

-- Key and date sanity
SELECT COUNT(*) AS null_or_invalid
FROM hda_curated.fact_encounter
WHERE encounter_id IS NULL OR patient_id IS NULL OR encounter_date IS NULL;

-- KPI base: one row per encounter.
SELECT date_trunc('month', encounter_date)::date AS month,
       COUNT(*) AS encounter_count,
       COUNT(DISTINCT patient_id) AS unique_patients
FROM hda_curated.fact_encounter
GROUP BY 1 ORDER BY 1;
