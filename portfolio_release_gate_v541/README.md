# v5.41.0 — Local Reproduction Review & Portfolio Release Gate

This release adds a deterministic comparator for the local execution evidence captured by v5.40. It distinguishes three states:
- `NOT_RUN`: no local report supplied.
- `REVIEW_REQUIRED`: evidence exists but a command failed, an artifact is missing, a hash is invalid or outputs differ.
- `PASS`: all captured commands exited zero and all three generated outputs exactly match the reference artifacts.

A `PASS` is limited to the captured execution evidence. It is not proof of a clean GitHub clone, privacy clearance, independent review, Power BI capability or job readiness.

## Run it
From the Academy root, after running the v5.40 capture utility:
```bash
python portfolio_evidence_pack_v540/src/capture_local_evidence.py \
  --project portfolio_execution_reproducibility_v538 \
  --destination portfolio_evidence_pack_v540/evidence/my_local_run

python portfolio_release_gate_v541/src/release_gate.py \
  --local portfolio_evidence_pack_v540/evidence/my_local_run \
  --reference portfolio_evidence_pack_v540/evidence/reference_run \
  --out portfolio_release_gate_v541/evidence/local_release_gate_report.json
```

## Current status in this package
No learner-side evidence was supplied to this build. Therefore the release gate is intentionally recorded as `NOT_RUN`. The automated tests use synthetic temporary fixtures only.
