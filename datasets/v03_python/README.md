# Python practice data

These CSV files are exports from the academy's fictional SQLite practice database. They contain synthetic records only.

- `encounters.csv` has one row per encounter.
- `patients.csv` has one row per synthetic patient.
- `departments.csv` is a department lookup table.
- `diagnoses.csv`, `prescriptions.csv` and `laboratory_results.csv` contain multiple child rows per encounter.

Keep the grain in mind: joining multiple child tables directly can multiply rows. Use the SQL lessons' pre-aggregation pattern before producing encounter-level summaries.

The data is for programming education only. It is not representative clinical evidence and must not be used for patient-care decisions, model training or claims about a real hospital.
