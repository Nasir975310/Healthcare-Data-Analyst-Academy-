-- Healthcare SQL Mastery: challenge prompts
-- Work in assignments/healthcare_sql_mastery.db

-- SQL-01 | 1 · Foundations | Inspect the tables and establish the grain
-- Before analysing any healthcare dataset, establish what each row represents and how many records are available.
-- TASK: Return the row count and distinct key count for both tables. Identify the grain of each table in one sentence.
-- Write your query below.


-- SQL-02 | 1 · Foundations | Filter a defined reporting period
-- The operations team requests encounters admitted during the first quarter of 2026.
-- TASK: Return encounter ID, admission date, department and length of stay for admissions from 1 January through 31 March 2026, ordered from newest to oldest.
-- Write your query below.


-- SQL-03 | 2 · Aggregation | Build department-level operational metrics
-- A department manager wants encounter volume and mean length of stay by department.
-- TASK: Return one row per department with encounter_count and mean_los_days rounded to two decimals.
-- Write your query below.


-- SQL-04 | 2 · Aggregation | Find therapeutic classes with high order volume
-- The pharmacy analytics team wants classes with at least 20 medication-order records.
-- TASK: Count orders by therapeutic class and return only classes with 20 or more orders.
-- Write your query below.


-- SQL-05 | 3 · Joins | Join encounters to medication orders safely
-- A clinical analytics colleague asks for order counts by department.
-- TASK: Return department and medication_order_count, counting orders assigned to encounters in each department.
-- Write your query below.


-- SQL-06 | 3 · Joins | Measure encounter coverage with LEFT JOIN
-- The team wants to know how many encounters have at least one medication order and how many have none.
-- TASK: Return each department's total encounters, encounters with at least one order, and encounters with no orders.
-- Write your query below.


-- SQL-07 | 4 · CTEs | Create an encounter-level medication summary
-- A quality analyst needs a dataset with one row per encounter and its number of medication orders.
-- TASK: Create a CTE that aggregates orders by encounter, then join it to encounters. Return encounter ID, department, LOS and order_count, including encounters with zero orders.
-- Write your query below.


-- SQL-08 | 4 · Window functions | Rank departments by mean length of stay
-- The operations director wants departments ranked by mean length of stay, retaining tied ranks.
-- TASK: Return department, encounter_count, mean_los_days and rank, with highest mean LOS ranked first.
-- Write your query below.


-- SQL-09 | 5 · Healthcare metrics | Calculate the supplied 30-day flag proportion
-- A quality team asks for the proportion of encounters marked with the supplied readmission flag.
-- TASK: Calculate total encounters, flagged encounters and flagged proportion as a percentage. Clearly label this as a supplied synthetic flag.
-- Write your query below.


-- SQL-10 | 5 · Data quality | Run key, chronology and referential-integrity checks
-- Before publishing a report, run basic data-quality checks on keys, dates and foreign-key relationships.
-- TASK: Write queries that identify duplicate encounter IDs, duplicate order IDs, discharge dates before admission dates, and medication orders referencing missing encounters.
-- Write your query below.


-- SQL-11 | 6 · Performance and interview | Inspect a query plan and justify an index
-- A recurring report filters medication orders by therapeutic class and status. You need to explain how SQLite accesses the table.
-- TASK: Inspect the query plan for a class/status filter. Compare the plan before and after creating an index on (therapeutic_class, order_status).
-- Write your query below.
