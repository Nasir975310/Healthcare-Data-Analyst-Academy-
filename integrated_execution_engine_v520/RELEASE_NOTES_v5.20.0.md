# Healthcare Data Analyst Academy v5.20.0

## Healthcare Analytics Integrated Execution Engine

### Delivered
- Execute trusted local Python scripts using the active interpreter, timeout handling, stdout/stderr capture, source hash and run metadata.
- Import CSV files into a project SQLite database with identifier validation.
- Execute one read-only SQLite SELECT/WITH query with read-only connection mode, mutation-denying authorizer, and a 100,000-row result cap.
- Export query results to CSV.
- Run declarative CSV pipelines: drop duplicates, filter exact values, rename columns and select columns.
- Record Python, CSV load, SQL query and pipeline runs in project execution history and local logs.
- Added synthetic demonstration data, end-to-end workflow and eight automated tests.
- Integrated Academy navigation and module guide.

### Limitations and safety
- Python scripts run with the current user's permissions; execution is not sandboxed. Run only trusted code.
- SQLite import stores columns as TEXT; type casting and semantic validation must be explicit.
- SQL support is SQLite only. PostgreSQL, R, DAX and Power Query are not executed.
- Pipeline operations are intentionally limited and do not replace a full ETL orchestrator.
- Logs and run metadata are not tamper-proof audit records.
- Do not process patient data without authorization, privacy review and appropriate access controls.
