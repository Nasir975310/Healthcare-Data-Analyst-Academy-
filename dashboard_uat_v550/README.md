# Chromium Dashboard UAT — v5.53.0

The runner starts its own local HTTP server and runs five real browser tests against the packaged dashboard. No separate terminal or manually started server is required.

## Recommended Ryoku / Arch Linux workflow

From the extracted Academy root:

```fish
cd dashboard_uat_v550
python -m venv .venv
source .venv/bin/activate.fish
python -m pip install --upgrade pip playwright
sudo pacman -S chromium
PLAYWRIGHT_CHROMIUM_EXECUTABLE=/usr/bin/chromium python scripts/run_browser_acceptance.py
```

If you prefer Playwright-managed Chromium, omit the `pacman` install and run:

```fish
python -m playwright install chromium
python scripts/run_browser_acceptance.py
```

Bash users: activate with `source .venv/bin/activate`.

## Runner behavior

- Starts a local HTTP server bound to `127.0.0.1:8765`.
- Serves the dashboard from the release's own files.
- Detects Chromium on PATH, or honors `PLAYWRIGHT_CHROMIUM_EXECUTABLE`.
- Runs five browser tests and checks browser page errors.
- Shuts down the local server even if the test process fails.
- Writes actual results to `evidence/uat_result.json`.

Change the port if necessary: `UAT_PORT=8766 python scripts/run_browser_acceptance.py`.

## Acceptance checks

1. Dashboard returns HTTP 200 and KPIs populate.
2. Drug-class filter changes the record count; reset restores the original count.
3. Both comorbidity states return records without classifying unknown status as yes/no.
4. CSV export downloads the expected filename and contains headers and data.
5. A 390px viewport does not create horizontal page overflow.

A `PASS` requires all five tests to execute and pass. Missing Playwright is `NOT_RUN`; browser launch, navigation, assertion or JavaScript errors are `FAIL`. The checked-in evidence JSON is only a pending template and is not proof of execution.

## Scope and limitations

The dashboard data are synthetic. These tests validate UI behavior and packaging, not clinical validity, causality, production readiness, or security for real patient data.
