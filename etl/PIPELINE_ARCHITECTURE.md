# ETL pipeline architecture

```text
CSV files / mock paginated API
            |
            v
       EXTRACT
  file/page inventory + hashes
            |
            v
       RAW LAYER
 source payload preserved in SQLite
            |
            v
     VALIDATE + PROFILE
 keys / types / nulls / references
       |             |
       | pass        | reject / warn
       v             v
   TRANSFORM       QUARANTINE
 trim / type /     source row +
 normalise         rejection reason
       |
       v
   CURATED MARTS
 encounter grain / order grain
       |
       v
   SQL AUDIT + REPORTING
 run log / quality results / manifest
```

## Operational principles
1. Define grain and data contract before coding.
2. Preserve raw inputs; transformations must be reproducible.
3. Use primary keys and explicit upsert behaviour.
4. Quarantine invalid foreign references; do not silently drop them.
5. Preserve NULL when a value is unknown or not supplied.
6. Record checksums and run-level row counts.
7. Separate warnings from fatal validation failures.
8. Test idempotency and late-arriving update behaviour before claiming incremental capability.

The supplied implementation is a local batch training pipeline. It is not a streaming, CDC, high-availability, or production clinical integration platform.
