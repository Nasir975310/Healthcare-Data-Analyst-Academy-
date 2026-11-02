# Technical challenge — answer guidance

Attempt the challenge before reading this file.

## Expected core counts
- Raw encounters: 91.
- Accepted encounters: 90.
- Rejected encounters: 1 (`E0091`, unknown patient).
- Curated observations: 170.
- Curated medication orders: 129.
- SQLite integrity: `ok`; foreign-key violations: 0.

## SQL examples
```sql
SELECT strftime('%Y-%m', encounter_date) AS month,
       COUNT(*) AS encounters,
       COUNT(DISTINCT patient_id) AS unique_patients
FROM fact_encounter GROUP BY 1 ORDER BY 1;

SELECT encounter_type, COUNT(*) AS encounters
FROM fact_encounter GROUP BY encounter_type ORDER BY encounters DESC;

SELECT s.encounter_id, s.patient_id
FROM stg_encounter s LEFT JOIN dim_patient p
ON p.patient_id=s.patient_id WHERE p.patient_id IS NULL;

SELECT encounter_id, COUNT(*) AS n
FROM stg_encounter GROUP BY encounter_id HAVING COUNT(*) > 1;
```

## Interpretation
- Preserve the orphan in staging and report it as an exception.
- Encounter count is records, not unique patients.
- Joining one-to-many medication orders before counting encounters can multiply rows; aggregate separately or count distinct encounter keys.
- Medication orders do not prove dispensing, ingestion, adherence or persistence.
- BP averages are descriptive and do not establish diagnosis, control or treatment effect.
- Test idempotence by running twice and comparing counts and output hashes.
