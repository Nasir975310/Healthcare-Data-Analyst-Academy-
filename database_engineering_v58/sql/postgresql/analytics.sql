-- Monthly department trends
SELECT d.department_name, dt.calendar_year, dt.calendar_month,
       SUM(f.encounter_count) AS encounters,
       ROUND(AVG(f.los_days),2) AS mean_los_days
FROM analytics.fact_encounter f
JOIN analytics.dim_department d USING(department_key)
JOIN analytics.dim_date dt USING(date_key)
GROUP BY d.department_name,dt.calendar_year,dt.calendar_month
ORDER BY dt.calendar_year,dt.calendar_month,d.department_name;

-- Window function: department monthly encounters and month-over-month delta
WITH monthly AS (
 SELECT department_key,date_key/100 AS year_month,SUM(encounter_count) AS encounters
 FROM analytics.fact_encounter f JOIN analytics.dim_date dt USING(date_key)
 GROUP BY department_key,date_key/100
)
SELECT department_key,year_month,encounters,
       LAG(encounters) OVER(PARTITION BY department_key ORDER BY year_month) AS prior_month,
       encounters-LAG(encounters) OVER(PARTITION BY department_key ORDER BY year_month) AS change
FROM monthly ORDER BY department_key,year_month;

-- Transaction example: atomic batch update
BEGIN;
UPDATE analytics.fact_encounter SET order_count=order_count WHERE encounter_id='SYNTH-001';
COMMIT;
