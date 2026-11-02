# Release notes — v5.60.0

## Vacancy Sourcing & Evidence Capture

### Added
- User-supplied vacancy excerpt capture with UTC timestamp and SHA-256 manifest.
- Vacancy source registry with strict schema, dates, status and URL validation.
- Duplicate candidates using canonical URL and employer/role/location heuristics.
- Deadline checks and explainable profile-to-vacancy prioritisation.
- Shortlist HTML and JSON reports.
- Source capture protocol and shortlist decision rules.

### QA
- 6/6 automated tests passed.
- Evidence capture CLI executed and SHA-256 manifest produced.
- Shortlist CLI executed on three fictional records.
- Duplicate group S-001/S-003 matched expected result.
- JSON report parsed and archive integrity checked.

### Limitations
- No live web retrieval, scraping, employer verification or application submission.
- User-supplied excerpts and evidence files are not authenticated.
- Priority scores are heuristic, not hiring probabilities.
