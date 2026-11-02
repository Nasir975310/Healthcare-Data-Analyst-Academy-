# v5.43.0 — Portfolio Handoff & External Evidence Verification

This module closes the gap between a locally prepared portfolio export and a genuinely published, independently reproducible repository.

## Evidence gate

- `NOT_RUN`: no meaningful handoff evidence supplied.
- `PENDING_EVIDENCE`: one or more required fields are missing.
- `REVIEW_REQUIRED`: evidence conflicts, fails checks or contains invalid values.
- `PASS`: required fields are present and basic commit, CI, clone, hash and review assertions are consistent.

A PASS is a consistency check of user-supplied evidence, not live GitHub verification, legal/privacy certification or an employment-readiness verdict.

## Run

```bash
python -m unittest portfolio_handoff_evidence_v543.tests.test_handoff_gate -v
python portfolio_handoff_evidence_v543/src/handoff_gate.py \
  --evidence portfolio_handoff_evidence_v543/templates/HANDOFF_EVIDENCE.json \
  --out portfolio_handoff_evidence_v543/evidence/gate_report.json
```

The template intentionally returns `PENDING_EVIDENCE`. Follow `docs/USER_HANDOFF_STEPS.md` to capture real evidence.
