# Healthcare SQL Mastery Laboratory

## Dialect and database
These challenges use SQLite SQL. The ready-to-query database is `assignments/healthcare_sql_mastery.db` in the Academy root. It contains synthetic data only.

Open the database directly in DBeaver: **Database > New Database Connection > SQLite**, then select the `.db` file. Alternatively, use:
```bash
sqlite3 assignments/healthcare_sql_mastery.db
```
On Windows PowerShell:
```powershell
sqlite3 .\assignments\healthcare_sql_mastery.db
```

## Challenge sequence
The interactive Academy's SQL Mastery area contains 11 progressive challenges. Attempt each task before expanding the hint or worked solution. `challenges.sql` provides a printable query prompt set; `solutions.sql` contains reference queries.

## Important
- Encounters table grain: one row per encounter.
- Medication orders table grain: one row per medication order.
- `readmission_30d_flag` is a synthetic teaching flag, not a validated readmission measure.
- Medication orders do not prove dispensing, administration or adherence.
- Do not use real patient data in this practice database.

## Fish shell note
If you use Fish on Ryoku, run `sqlite3 assignments/healthcare_sql_mastery.db` directly. No virtual environment is required for SQLite CLI work. If you prefer DBeaver, open the database file through a SQLite connection.

## SQL dialect note
This pack uses SQLite syntax and date handling. When transferring the skills to PostgreSQL, SQL Server, MySQL or BigQuery, check dialect differences in date functions, type casting, window functions, identifier quoting and query-plan tools.
