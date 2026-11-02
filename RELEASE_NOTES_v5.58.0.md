# Release notes — v5.58.0

## Application Performance & Career Intelligence

### Added
- CSV application tracker ingestion with required-column, unique-ID, allowed-stage and ISO date validation.
- Submitted, response-stage proxy, interview and offer metrics with explicit denominators.
- CV-version descriptive counts and rejection-reason aggregation.
- Standalone HTML dashboard and JSON summary.
- Weekly review protocol and privacy/recruitment safety checklist.

### QA
- 6/6 automated tests passed.
- Sample CLI run passed on a fictional six-row dataset.
- Output JSON parsed successfully.
- HTML output includes escaping for user-controlled content.

### Limitations
- Metrics are only as accurate as the manually maintained tracker.
- Response-stage proxy is not response-time analysis.
- CV-version comparisons are not causal.
- No live vacancy search, employer verification, external submissions or hiring prediction.
