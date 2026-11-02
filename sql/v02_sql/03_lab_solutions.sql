-- Selected SQL lab solutions (SQLite)
-- Lab A: count encounters by encounter type, including mean LOS.
SELECT encounter_type, COUNT(*) AS n,
       ROUND(AVG(length_of_stay_days),2) AS mean_los
FROM encounters GROUP BY encounter_type ORDER BY n DESC;

-- Lab B: list patients with 2+ encounters and retain only groups meeting threshold.
SELECT p.synthetic_patient_code, COUNT(e.encounter_id) AS encounter_count
FROM patients p JOIN encounters e ON e.patient_id=p.patient_id
GROUP BY p.patient_id, p.synthetic_patient_code
HAVING COUNT(e.encounter_id)>=2
ORDER BY encounter_count DESC, p.synthetic_patient_code;

-- Lab C: count unique primary diagnoses by diagnosis label.
SELECT diagnosis_label, COUNT(DISTINCT encounter_id) AS encounters
FROM diagnoses WHERE diagnosis_role='Primary'
GROUP BY diagnosis_label ORDER BY encounters DESC;

-- Lab D: department mean SBP, with denominator made visible.
SELECT d.department_name,
       COUNT(e.systolic_bp) AS nonmissing_sbp_n,
       ROUND(AVG(e.systolic_bp),1) AS mean_sbp
FROM departments d LEFT JOIN encounters e ON e.department_id=d.department_id
GROUP BY d.department_id,d.department_name
ORDER BY mean_sbp DESC;

-- Lab E: one row per encounter with prescription and diagnosis counts.
WITH r AS (SELECT encounter_id,COUNT(*) AS n_rx FROM prescriptions GROUP BY encounter_id),
     g AS (SELECT encounter_id,COUNT(*) AS n_dx FROM diagnoses GROUP BY encounter_id)
SELECT e.encounter_id,COALESCE(r.n_rx,0) AS n_rx,COALESCE(g.n_dx,0) AS n_dx
FROM encounters e LEFT JOIN r ON r.encounter_id=e.encounter_id
LEFT JOIN g ON g.encounter_id=e.encounter_id
ORDER BY e.encounter_id;

-- Lab F: identify the first encounter for each patient.
WITH ranked AS (
 SELECT encounter_id,patient_id,admission_date,
 ROW_NUMBER() OVER(PARTITION BY patient_id ORDER BY admission_date,encounter_id) AS rn
 FROM encounters
)
SELECT * FROM ranked WHERE rn=1 ORDER BY patient_id;
