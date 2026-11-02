# Stabilization and acceptance guide — v5.60.3

## 1. Extract and inspect
Extract the ZIP into a writable directory. Read `README.md`, `SHOWCASE.md`, `ACADEMY_CATALOG.md`, `MODULE_COMPATIBILITY_MATRIX.md` and this guide.

## 2. Open the academy
Open `index.html` in Firefox or Chromium. Test navigation, project-library links, curriculum content and local assets. For browser restrictions, run `python -m http.server 8000` from the academy root and open `http://localhost:8000/`.

## 3. Run maintained tests
Install pytest, then run:

```bash
python -m pip install pytest
python -B -m pytest -q
```

This runs only the six maintained career release-gate suites. Expected baseline: 36 passed, 11 unittest subtests.

## 4. Run historical module audit

```bash
python -B scripts/verify_full_academy.py --timeout 30 --jobs 2
```

The command runs each discovered `tests/` directory in a separate pytest process and writes `FULL_TEST_REPORT.json`. It reports passed, failed, timed out and dependency/import-error outcomes. Resolve dependencies using each module's README/requirements. Do not treat a partial or not-run report as a pass.

## 5. Run release checks

```bash
python -B scripts/verify_release.py
python -B scripts/validate_release_docs.py
python -B scripts/scan_sensitive_patterns.py
```

The sensitive-pattern scanner is heuristic; review findings manually. It cannot certify absence of PHI or secrets.

## 6. Browser acceptance
See `dashboard_uat_v550/README.md` for the Playwright/Chromium test. Browser acceptance must be run on the target Ryoku workstation; it is not certified by this build.

## 7. Publication gate
Choose a license only after deciding reuse permissions and reviewing third-party assets. Review `SECURITY.md`, `DATA_HANDLING_POLICY.md`, all datasets, notebooks, logs, outputs, screenshots and Git history before public sharing. No license is granted by this archive.
