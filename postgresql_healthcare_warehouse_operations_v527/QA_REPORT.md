# QA report — v5.27.0

- Six unit/contract tests passed.
- Python source compiled successfully.
- PostgreSQL loader uses psycopg 3 parameterized queries and a transaction boundary.
- Schema includes SCD Type 2 current-row uniqueness, validity checks, fact tables, marts and supporting indexes.
- Loader has idempotent upserts for encounter, observation and medication resources; patient attribute changes close and version dimension rows.
- Security template contains no embedded passwords.
- Live PostgreSQL integration was not run: no configured PostgreSQL service/DSN was available. SQL syntax must be validated against the target PostgreSQL version before deployment.
- Performance claims are not made from the small synthetic dataset.
