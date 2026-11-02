-- SQLite reference: unique patients with at least one active antihypertensive order
SELECT COUNT(DISTINCT patient_id) AS unique_patients_treated
FROM encounters
WHERE order_status = 'Active'
  AND drug_class = 'Antihypertensive'
  AND admit_date >= '2026-01-01'
  AND admit_date < '2026-02-01';

-- Department-level numerator and patient denominator
SELECT department,
       COUNT(DISTINCT CASE WHEN order_status='Active'
                            AND drug_class='Antihypertensive'
                           THEN patient_id END) AS treated_patients,
       COUNT(DISTINCT patient_id) AS all_patients
FROM encounters
GROUP BY department
ORDER BY department;
