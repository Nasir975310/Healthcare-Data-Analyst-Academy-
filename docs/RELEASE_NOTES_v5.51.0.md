# v5.51.0 — Chromium-compatible dashboard acceptance

This release improves the v5.50 browser acceptance suite so it works with either Playwright-managed Chromium or a system Chromium installation (including CachyOS/Arch Linux). The runner now treats skipped browser tests as `REVIEW_REQUIRED`, never as a pass.

## Run on CachyOS / Ryoku
1. Install Chromium: `sudo pacman -S chromium`
2. Start the dashboard server from `interactive_clinical_bi_dashboard_v548`: `python -m http.server 8000`
3. In a second terminal, from the Academy root: `cd dashboard_uat_v550`
4. Create/activate a virtual environment and install Playwright: `python -m venv .venv && source .venv/bin/activate && pip install playwright`
5. Run: `PLAYWRIGHT_CHROMIUM_EXECUTABLE=/usr/bin/chromium python scripts/run_browser_acceptance.py`

Alternatively, use `python -m playwright install chromium` and run without the executable environment variable.

## Evidence rules
A successful result requires all four browser tests to execute, not skip. The generated evidence file records browser/test output. A passing test in this build environment does not establish that the user's own laptop has been tested.
