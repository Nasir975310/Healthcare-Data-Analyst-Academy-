# Security, backup and restore practical

Run only in the disposable training database.

```sql
CREATE ROLE analyst_readonly LOGIN PASSWORD 'set-a-local-password';
GRANT CONNECT ON DATABASE hda_training TO analyst_readonly;
GRANT USAGE ON SCHEMA hda TO analyst_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA hda TO analyst_readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA hda GRANT SELECT ON TABLES TO analyst_readonly;
```
Test as analyst_readonly: SELECT should work; INSERT/UPDATE/DELETE should fail. Do not grant CREATE or ownership to an analyst role. For a real organisation, align role design with approved identity management and audit requirements.

## Backup / restore
```bash
pg_dump -h localhost -U hda_admin -d hda_training -Fc -f hda_training.dump
createdb -h localhost -U hda_admin hda_restore_test
pg_restore -h localhost -U hda_admin -d hda_restore_test --no-owner hda_training.dump
```
Compare row counts in both databases and run `SELECT count(*)` for all four tables. Keep backups encrypted, access-controlled and retention-managed. A successful dump is not proof of recoverability: schedule restore tests.

## Migration discipline
1. Record current schema version and baseline counts.
2. Write a forward migration and a rollback/compensation plan.
3. Test on a restored copy.
4. Validate constraints, row counts, application queries and execution plans.
5. Obtain approval, schedule the change, log the result and retain recovery options.
