# v5.60.2 — Maintenance release

This is a maintenance release over the v5.60.0 feature baseline.

## Fixes
- Root `pytest -q` now targets the six maintained career workflow test suites. This avoids import collisions from legacy modules that reuse generic test filenames and local package names.
- The academy navigation now labels the Projects section as a project library and links to existing project guides instead of incorrectly presenting it as planned.
- Added `scripts/verify_full_academy.py` for isolated per-directory legacy test execution and a JSON report. This is a supplementary audit tool; optional tests may need module-specific dependencies.

## Verified in this build environment
- 36 tests passed across the six maintained career suites (11 unittest subtests).
- All 205 Python files passed AST syntax parsing in the earlier focused baseline; rerun syntax check against this archive as part of packaging.
- Static index reference checks are required at packaging time.

## Known limitation
The browser sandbox returned `ERR_BLOCKED_BY_ADMINISTRATOR` for both localhost and file URL navigation. Therefore the Chromium dashboard suite and visual browser acceptance could not be certified here. Run the dedicated dashboard UAT script on the target Ryoku machine.

## Scope boundaries
No live vacancy search, employer verification, job application, GitHub publication, remote CI, Power BI PBIX generation or user-workstation UAT is claimed.
