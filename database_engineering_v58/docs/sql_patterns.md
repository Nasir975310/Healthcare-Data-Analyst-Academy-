# SQL production patterns

- Use explicit columns rather than `SELECT *` in production queries.
- Use parameterized queries for application inputs.
- Use transactions for logically atomic writes.
- Add constraints for enforceable data invariants; validate upstream as well.
- Index based on measured query workload and inspect `EXPLAIN`/`EXPLAIN ANALYZE`.
- Avoid indiscriminate indexes: they increase write cost and storage.
- Use `LAG`/`ROW_NUMBER` for ordered comparisons and deduplication, with deterministic ordering.
- Use `COUNT(DISTINCT patient_token)` only when the question asks for unique patients, not encounter counts.
- Review permissions, backups, retention, encryption and audit logging before production use.
