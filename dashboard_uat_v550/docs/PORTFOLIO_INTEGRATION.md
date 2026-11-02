# Portfolio integration gate

## Required evidence before publication
1. Successful browser acceptance run on the user's workstation (`evidence/uat_result.json`, status `PASS`).
2. Screenshots: initial dashboard, one filtered state, reset state, and CSV opened in a spreadsheet editor.
3. Existing v5.49 Python/JavaScript reconciliation report.
4. README with synthetic-data provenance, metric definitions, limitations, setup steps, and test commands.
5. Hygiene scan confirming no real patient data, credentials, local paths, or unrelated files.

## Claims matrix
| Claim | Allowed now? | Evidence needed |
|---|---|---|
| Built a responsive HTML/JS dashboard | Yes, as local artifact | Source files |
| Added independent metric reconciliation | Yes, automated release QA | v5.49 QA outputs |
| Browser-tested on Ryoku | No | User-side Playwright PASS |
| Published on GitHub | No | Public/private repository URL and commit |
| Deployed for clinical use | No | Formal validation, governance, security, and institutional approval |

Do not treat passing synthetic-data tests as clinical validation.
