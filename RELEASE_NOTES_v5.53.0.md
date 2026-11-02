# v5.53.0 — Chromium UAT execution hardening

## Changes
- Fixed test discovery so the runner executes the browser test file from its actual directory.
- Maintained system Chromium and Playwright-managed Chromium support.
- Kept server startup/shutdown inside the runner.
- Preserved five acceptance checks and strict PASS/FAIL/NOT_RUN evidence semantics.
- Added a pending-only evidence template; no browser run is claimed.

## Verification boundary
Python compilation, existing dashboard unit tests, JavaScript syntax, archive integrity and hygiene can be checked in the build environment. The actual Chromium suite must be executed on Ryoku or another workstation with a functioning Chromium GUI/headless runtime.
