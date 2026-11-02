# PostgreSQL execution guide

1. Install PostgreSQL 14+ and start the service using your distribution's service manager.
2. Create a dedicated database and non-superuser role for the practicum.
3. Execute `sql/postgresql/001_schema.sql`, then load the synthetic v5.32 encounter CSV into `hda_raw.encounters` using `\copy` with explicit column mapping.
4. Populate `hda_curated.dim_patient` from the patient source.
5. Apply documented deduplication and orphan handling before inserting curated facts.
6. Execute `002_validation.sql`; save outputs and explain raw = accepted + exceptions.
7. Test `003_migration_template.sql` in a disposable database before production.
8. Capture PostgreSQL version, row counts, query plans (`EXPLAIN (ANALYZE, BUFFERS)`), and test results.

Never use a superuser for routine analytics. Restrict schemas and tables with GRANT. Use parameterized queries, TLS where remote, backups and least privilege. The scripts are reference assets and have not been run against a PostgreSQL server in this build.
