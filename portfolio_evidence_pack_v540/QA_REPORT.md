# QA Report — v5.40.0

## Executed in release build environment
- v5.40 evidence-capture utility tests: **2/2 passed**.
- v5.38 regression tests: **5/5 passed**.
- v5.38 end-to-end pipeline: **exit code 0**.
- Reference outputs re-generated and compared byte-for-byte:
  - `quality_report.json`: match
  - `department_summary.csv`: match
  - `sha256_manifest.json`: match
- Python source compilation across Academy: **0 errors**.
- Roadmap JavaScript syntax (`node --check`): **passed**.
- Academy HTML duplicate IDs: **0**.
- v5.40 Academy navigation link: **present**.

## Environment warning
Python startup emitted an `artifact_tool` spreadsheet warmup warning (`Element ordering requires an owning element collection`). The warning did not prevent tests or the pipeline from completing successfully.

## Not performed
- No reproduction on the user's CachyOS/Ryoku workstation.
- No GitHub publication or published-repository clean-clone verification.
- No Power BI execution.
- No independent employer/recruiter review.

The reference outputs represent the release build environment's run on synthetic data. The included local capture utility is intended to gather separate evidence from the user's machine.
