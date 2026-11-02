-- SQLX-01: Safe encounter-to-order join
SELECT COUNT(*) AS joined_rows, COUNT(DISTINCT e.encounter_id) AS encounters FROM encounters e LEFT JOIN medication_orders o ON o.encounter_id=e.encounter_id;

-- SQLX-02: Window ranking
WITH d AS (SELECT department, AVG(length_of_stay_days) mean_los FROM encounters GROUP BY department) SELECT department, ROUND(mean_los,2), DENSE_RANK() OVER(ORDER BY mean_los DESC) AS rnk FROM d ORDER BY rnk,department;

-- SQLX-03: 30-day readmission proxy
SELECT department, COUNT(*) AS n, SUM(readmission_30d_flag) AS flagged, ROUND(100.0*SUM(readmission_30d_flag)/COUNT(*),2) AS pct FROM encounters GROUP BY department;

-- SQLX-04: Latest record per patient
WITH x AS (SELECT *, ROW_NUMBER() OVER(PARTITION BY patient_id ORDER BY admission_date DESC, encounter_id DESC) rn FROM encounters) SELECT * FROM x WHERE rn=1;

-- SQLX-05: Anti-join orphan audit
SELECT o.* FROM medication_orders o WHERE NOT EXISTS (SELECT 1 FROM encounters e WHERE e.encounter_id=o.encounter_id);

-- SQLX-06: NULL-safe cost analysis
SELECT COUNT(*) total_rows, SUM(CASE WHEN unit_cost_inr IS NULL THEN 1 ELSE 0 END) missing_cost_rows, SUM(quantity*unit_cost_inr) known_value_inr FROM medication_orders;

-- SQLX-07: Rolling 7-day volume
WITH daily AS (SELECT order_date, COUNT(*) n FROM medication_orders GROUP BY order_date) SELECT order_date,n,SUM(n) OVER(ORDER BY order_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) rolling_7_rows FROM daily;

-- SQLX-08: Cohort entry and follow-up
WITH x AS (SELECT patient_id, admission_date, encounter_id, LEAD(admission_date) OVER(PARTITION BY patient_id ORDER BY admission_date) next_date FROM encounters) SELECT *, CASE WHEN julianday(next_date)-julianday(admission_date) BETWEEN 1 AND 30 THEN 1 ELSE 0 END subsequent_30d FROM x;

-- SQLX-09: Deduplicate business records
SELECT encounter_id,therapeutic_class,order_date,COUNT(*) candidate_rows FROM medication_orders GROUP BY encounter_id,therapeutic_class,order_date HAVING COUNT(*)>1;

-- SQLX-10: Conditional aggregation
WITH o AS (SELECT encounter_id,COUNT(*) order_lines,SUM(quantity*unit_cost_inr) known_cost FROM medication_orders GROUP BY encounter_id) SELECT e.department,SUM(COALESCE(o.order_lines,0)) lines,SUM(o.known_cost) known_cost FROM encounters e LEFT JOIN o ON o.encounter_id=e.encounter_id GROUP BY e.department;

-- SQLX-11: Percentile and median portability
SELECT department,length_of_stay_days FROM encounters WHERE length_of_stay_days IS NOT NULL ORDER BY department,length_of_stay_days;

-- SQLX-12: Query plan and indexing
EXPLAIN QUERY PLAN SELECT * FROM medication_orders WHERE order_date BETWEEN '2026-01-01' AND '2026-03-31';

-- SQLX-13: Cohort denominator integrity
SELECT 'encounters' entity,COUNT(DISTINCT patient_id) distinct_people,COUNT(*) rows FROM encounters UNION ALL SELECT 'orders',COUNT(DISTINCT encounter_id),COUNT(*) FROM medication_orders;

-- SQLX-14: Pivot-style aggregation
SELECT department,SUM(CASE WHEN therapeutic_class='Antihypertensive' THEN 1 ELSE 0 END) antihypertensive_lines,SUM(CASE WHEN therapeutic_class IS NULL OR therapeutic_class='' THEN 1 ELSE 0 END) unknown_class_lines FROM medication_orders o LEFT JOIN encounters e ON e.encounter_id=o.encounter_id GROUP BY department;

-- SQLX-15: Date boundary correctness
SELECT COUNT(*) FROM medication_orders WHERE order_date >= '2026-01-01' AND order_date < '2026-02-01';

-- SQLX-16: CTE cohort with exclusion
SELECT COUNT(*) eligible FROM encounters WHERE ckd_flag=1 AND baseline_sbp IS NOT NULL;

-- SQLX-17: Medication utilisation intensity
WITH o AS (SELECT encounter_id,COUNT(*) n FROM medication_orders GROUP BY encounter_id) SELECT e.department,COUNT(*) encounters, SUM(COALESCE(o.n,0)) lines,ROUND(1.0*SUM(COALESCE(o.n,0))/COUNT(*),2) lines_per_encounter FROM encounters e LEFT JOIN o ON o.encounter_id=e.encounter_id GROUP BY e.department;

-- SQLX-18: Incremental load watermark
SELECT * FROM medication_orders WHERE updated_at > '2026-03-01T00:00:00';

-- SQLX-19: Case-mix stratification
SELECT CASE WHEN age<40 THEN '<40' WHEN age<65 THEN '40-64' ELSE '65+' END age_band,diabetes_flag,COUNT(*) n,AVG(length_of_stay_days) mean_los FROM encounters GROUP BY age_band,diabetes_flag;

-- SQLX-20: Data quality exception rate
SELECT SUM(CASE WHEN baseline_sbp IS NULL THEN 1 ELSE 0 END) missing_sbp, SUM(CASE WHEN length_of_stay_days<0 THEN 1 ELSE 0 END) negative_los,COUNT(*) denominator FROM encounters;
