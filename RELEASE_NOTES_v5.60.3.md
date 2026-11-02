# v5.60.3 — Release integrity and audit alignment

## Changes
- Restored `scripts/verify_full_academy.py`, the previously documented but missing audit utility.
- Added `FULL_TEST_REPORT.json` generation with per-test-directory outcomes. The report explicitly distinguishes pass, failure, timeout, import/dependency errors and not-run states.
- Added `MODULE_COMPATIBILITY_MATRIX.md/.json` as an inventory of test-bearing course packs and their module-local execution conventions. It is not a compatibility guarantee.
- Added root `.gitignore`, `SECURITY.md`, `DATA_HANDLING_POLICY.md` and `LICENSE_DECISION_REQUIRED.md`. No license was selected without the owner's permission decision.
- Updated CI to run maintained root tests, isolated historical test audit, static syntax validation, release-document checks and heuristic sensitive-pattern scanning.
- Consolidated duplicate changelog version headings.

## Verification scope
- Maintained root suite: 36 passed, 11 unittest subtests passed.
- Full-academy test-directory inventory: 69 test directories discovered.
- The supplementary audit utility was executed. The full historical suite did not complete within the available execution window; timeout and import/dependency statuses must remain visible in `FULL_TEST_REPORT.json`. No claim of full historical-suite success is made.
- Browser UAT remains manual/optional and requires execution on the target workstation.

## Remaining owner decisions / external acceptance
- Select an appropriate license only after reviewing third-party assets and reuse intent.
- Run the full isolated audit in a normal development environment with module dependencies installed.
- Execute browser UAT on Ryoku.
- Review sensitive-pattern scan findings manually; heuristic scanning is not PHI certification.
- Publish only after privacy, provenance, licensing and clean-clone review.
