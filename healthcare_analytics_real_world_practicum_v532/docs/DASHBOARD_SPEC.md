# Power BI dashboard specification

## Page 1 — Executive operations
Cards: patients, source encounters, curated encounters, completed, cancelled and scheduled. Line/column chart: monthly encounters by status. Include reporting period and refresh timestamp.

## Page 2 — Encounter operations
Bar chart: encounter count by type. Matrix: month x status. Ensure counts use curated encounter fact and define whether cancelled/scheduled records are included.

## Page 3 — Pharmacy orders
Bar chart: medication orders by drug class and medication. Label all visuals as orders; do not call them dispensed medicines or adherence.

## Page 4 — Observations
Show paired systolic/diastolic distributions and sample counts with mmHg units. Use descriptive labels and avoid clinical-control claims.

## Page 5 — Data quality
Show source vs curated row counts, orphan patient keys, rejected encounter IDs, duplicates, invalid values and integrity checks.

## Model rules
Use one-to-many dimensions-to-facts, single-direction filtering by default. Do not directly join observation and medication facts. If using encounter as a conformed dimension/bridge, document cardinality and measures.
