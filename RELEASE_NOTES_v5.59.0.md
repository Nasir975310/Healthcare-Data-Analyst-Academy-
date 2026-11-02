# Release notes — v5.59.0

## Job Search Source & Vacancy Verification

### Added
- Vacancy registry CSV with strict schema, stage, date and URL validation.
- URL canonicalisation and duplicate source URL grouping.
- Deadline expiry checks against an explicit review date.
- Five-part human verification checklist and conservative review gate.
- Standalone HTML and JSON reports.
- Employer verification protocol and vacancy triage rules.

### QA
- 6/6 automated tests passed.
- Demo CLI execution passed with three fictional records.
- Duplicate URL group and one expired deadline matched expected demo results.
- JSON output parsed successfully; archive integrity checked.

### Limitations
- No web access or employer verification is performed.
- URL matching cannot identify every duplicate vacancy.
- Checklist completion is not a guarantee of legitimacy or safety.
