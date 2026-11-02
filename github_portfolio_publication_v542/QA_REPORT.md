# QA Report — v5.42.0

## Executed in release build environment
- v5.42 exporter/scanner tests: **4/4 passed**.
- Actual sample repository export: **14 source/case-study files plus generated README, workflow and manifest**.
- Sample repository's v5.38 tests: **5/5 passed**.
- Sample repository pipeline: **exit code 0**.
- Sample repository preflight: **0 findings**.
- Publication scanner after removing generated Python bytecode caches: **0 findings**.
- Exporter refuses to overwrite a non-empty destination.
- Secret-pattern fixture is detected by the heuristic scanner.
- Python compilation across Academy: **0 errors**.
- Roadmap JavaScript syntax (`node --check`): **passed**.
- Academy HTML duplicate IDs: **0**; v5.42 navigation link present.

## Scanner limitation observed
Running Python tests creates `__pycache__` bytecode files. The scanner correctly flags these as forbidden artifacts. They were removed from the sample export before the final zero-finding scan. Keep caches out of published repositories; `.gitignore` is included, but inspect actual staged files before committing.

## Not performed
- No GitHub repository creation or push.
- No license selection.
- No live GitHub Actions execution.
- No fresh clone from a published remote.
- No independent legal/privacy review.

The zero-finding heuristic scan is not a security certification. Manual review of all files, provenance, history and permissions remains required.
