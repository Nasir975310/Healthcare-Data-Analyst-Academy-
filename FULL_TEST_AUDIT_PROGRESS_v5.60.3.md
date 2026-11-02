# v5.60.3 Historical Test Audit — Progress

Generated: 2026-11-02.

Discovered test directories: **69**. Execution complete: **false**.

| Status | Count |
|---|---:|
| passed | 33 |
| timed_out | 16 |
| no_tests_collected | 2 |
| not_run | 18 |

This is an incomplete historical test-directory sweep, not certification. A passing directory is not proof of full academy correctness; timeouts are inconclusive; no-tests means pytest found no runnable tests.

Resume from the academy root:
```bash
python -B scripts/verify_full_academy.py --timeout 30 --jobs 1 --resume --output FULL_TEST_REPORT.json
```

Retry timeouts separately with a longer limit. Do not mark them passed manually. Browser UAT is still pending on the target workstation.
