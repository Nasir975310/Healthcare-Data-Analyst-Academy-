# Stabilization report — v5.60.3

## Release integrity repairs
- Restored `scripts/verify_full_academy.py`; it discovers test directories, runs each in an isolated pytest process, and writes `FULL_TEST_REPORT.json` with explicit outcomes.
- Added a 69-directory inventory report. Historical test directories are marked `not_run` in the packaged report because the full sweep did not complete within this build environment's execution window. This is not a pass claim.
- Preserved the six maintained career release-gate suites as the root pytest scope.
- Updated GitHub Actions to run maintained tests, supplementary isolated audit, Python syntax checks, changelog validation and a conservative sensitive-pattern scan. Browser UAT is explicitly separate and non-gating.
- Consolidated duplicate changelog version headers; validator confirms 34 unique version headings.
- Added root `.gitignore`, `SECURITY.md`, `DATA_HANDLING_POLICY.md` and `LICENSE_DECISION_REQUIRED.md`.
- Added module compatibility inventory in Markdown and JSON. The academy uses a course-pack model; dependencies and Python requirements remain module-specific and are not centrally guaranteed.

## Executed verification
- Maintained tests: 36 passed; 11 unittest subtests passed.
- Python AST: 208/208 files parsed.
- Changelog validator: passed, 34 unique version headers, no unresolved release-note markers.
- Sensitive-pattern scan: passed configured patterns after excluding known fake fixtures and detection-rule literals. This heuristic is not a PHI/privacy certification.
- Full historical isolated suite: not completed in this environment. `FULL_TEST_REPORT.json` marks all 69 discovered test directories `not_run` and the README gives the command to execute on a normal development machine.

## Known pending work
- Run `python -B scripts/verify_full_academy.py --timeout 30 --jobs 2` with all module-specific dependencies available. Review each failed, timeout, or dependency-missing result.
- Browser UAT remains unverified on Ryoku.
- License choice requires owner approval and third-party asset review; no license is granted by this release.
- Manual privacy/provenance review and clean-clone publication checks remain pending.

## Interpretation
This release is a more auditable educational repository and course-pack distribution. It is not represented as a production-ready software platform, clinically validated system, or fully tested historical codebase.
