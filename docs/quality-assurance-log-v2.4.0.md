# Quality assurance log — v2.4.0

## Executed checks
- [x] CSV pipeline completed successfully: 80 encounters, 150 orders.
- [x] Mock paginated JSON pipeline completed successfully: 80 encounters, 150 orders.
- [x] Mock API page order and advertised record totals checked by extractor.
- [x] Injected orphan reference was quarantined; 149 of 150 order rows entered the curated order mart.
- [x] Repeated run against same database kept curated row counts stable and recorded a second run.
- [x] Zero quantity with `--fail-on-errors` stopped the run with nonzero exit.
- [x] Optional unit-cost field absence handled as `source_field_not_supplied`, not mass missing-cost errors.
- [x] SQLite integrity check returned `ok`; audit SQL executed.
- [x] New ETL challenge JSON parsed and challenge IDs are unique.
- [x] New Python pipeline and API extractor passed AST syntax parsing.
- [x] New JavaScript passed `node --check`.
- [x] HTML parsed with Python HTMLParser.
- [x] Sample database and run manifest/log/quality report generated.

## Not tested / limitations
- Generic REST extractor was not connected to or tested against a live API.
- systemd timer and Windows Task Scheduler examples were not enabled or executed on the user's machine.
- No browser automation or cross-device UI test.
- No production-grade concurrency, distributed scheduling, alerting, CDC, streaming or disaster recovery.
- No clinical validation or peer review of synthetic data assumptions.

## Data interpretation safeguards
- Synthetic records only.
- Base order extract does not include unit costs; pipeline records that the field is not supplied.
- Medication orders do not prove dispensing, administration, adherence or appropriateness.
- Do not use PHI without authorisation, approved technical controls and governance.
