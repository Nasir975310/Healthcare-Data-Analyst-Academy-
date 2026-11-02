-- SQLite-compatible semantic layer views. Grain: one row per encounter.
CREATE VIEW IF NOT EXISTS vw_encounter_semantic AS
SELECT e.encounter_id, e.patient_id, e.department_id, d.department_name,
       e.encounter_date, strftime('%Y-%m', e.encounter_date) AS year_month,
       e.encounter_type, e.discharge_status, e.los_days, e.charge_inr,
       1 AS encounter_count,
       CASE WHEN e.encounter_type='IPD' THEN 1 ELSE 0 END AS ipd_encounter_flag
FROM encounters e JOIN departments d USING(department_id);

CREATE VIEW IF NOT EXISTS vw_monthly_department AS
SELECT year_month, department_name, COUNT(*) AS encounters,
       COUNT(DISTINCT patient_id) AS distinct_patients,
       SUM(charge_inr) AS total_charges_inr,
       AVG(CASE WHEN encounter_type='IPD' THEN los_days END) AS mean_ipd_los
FROM vw_encounter_semantic
GROUP BY year_month, department_name;
