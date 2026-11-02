# Release v5.52.0 — Chromium UAT Reliability

## Objective
Close the usability gap in v5.51.0: browser testing previously required a separately managed HTTP server and could classify browser launch issues as skipped tests.

## Changes
- Self-contained runner starts/stops a local HTTP server.
- Auto-detects Chromium on PATH and supports `PLAYWRIGHT_CHROMIUM_EXECUTABLE`.
- Five tests cover initial KPIs, drug filtering/reset, both comorbidity states, CSV download contents, and mobile viewport overflow.
- JavaScript page errors fail the tests.
- Evidence distinguishes `PASS`, `FAIL`, `NOT_RUN`, and `PENDING_USER_RUN`.

## Validation boundary
The package can be statically validated in the build environment. Actual Chromium UI acceptance must run on the user's Ryoku workstation. A browser test result is not claimed until the runner produces `status: PASS`.
