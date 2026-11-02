# Technical assessment bank with answer guidance

Use the questions as timed practice. The answers are guidance, not a substitute for writing and running your own solution.

## Excel
1. A patient ID appears multiple times because each row is a separate encounter. How do you count unique patients?
   - Use a distinct-count approach (PivotTable Data Model or UNIQUE/COUNTA where supported); do not count rows as patients.
2. A monthly total differs from the source system. What do you check?
   - Date boundaries, status filters, duplicates, cancelled records, timezone/date parsing, inclusion rules and aggregation grain.
3. When is XLOOKUP insufficient?
   - When one key maps to multiple rows or the task requires aggregation; use a join plus aggregation, Power Query merge/grouping or a pivot.

## SQL
1. Find encounters without a matching patient.
   - `SELECT e.* FROM encounter e LEFT JOIN patient p ON p.patient_id=e.patient_id WHERE p.patient_id IS NULL;`
2. Why can joining observations and medications directly by encounter inflate totals?
   - Both are one-to-many child facts; their combination creates a Cartesian fanout within each encounter. Aggregate each fact independently or keep separate fact tables.
3. Return the latest encounter per patient.
   - `ROW_NUMBER() OVER (PARTITION BY patient_id ORDER BY encounter_date DESC, encounter_id DESC)` and filter row number 1.
4. Difference between COUNT(*) and COUNT(column)?
   - COUNT(*) counts rows; COUNT(column) excludes NULL values.

## Python / pandas
1. How do you inspect a CSV before analysis?
   - Check shape, dtypes, null counts, unique keys, duplicates, value distributions and referential integrity.
2. Why preserve raw source files?
   - Reproducibility, traceability and the ability to compare transformed output to source.
3. How do you avoid silently coercing invalid numeric values?
   - Use explicit parsing, count newly introduced nulls, retain rejected values and write a validation report.

## Power BI
1. Why prefer a star schema?
   - Clear grain, predictable filter propagation and simpler measures.
2. What is filter context?
   - The set of filters affecting a DAX expression at evaluation time; CALCULATE modifies that context.
3. How do you validate RLS?
   - Test roles with View As and representative users, including allowed and denied cases; verify every relevant table is secured through relationships.

## Healthcare analytics
1. Does a prescription/order prove the patient received or took the medicine?
   - No. Orders, dispensing, administration and adherence are distinct events.
2. Can a single elevated BP reading establish a diagnosis?
   - No. Clinical diagnosis requires appropriate measurement, context and clinician assessment.
3. Why must units and reference ranges be retained?
   - Values are uninterpretable or misleading without units, methods, population and context.

## Communication
1. A dashboard metric changes after refresh. What do you tell the client?
   - State the observed change, quantify it, identify whether it is source data, logic or refresh related, explain impact, provide next action and avoid unsupported certainty.
