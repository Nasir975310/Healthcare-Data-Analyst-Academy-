# v5.44.0 — Portfolio Release Candidate Builder

## Delivered
- A reusable builder verifies all 14 entries in the v5.42 sample project's source manifest.
- A heuristic scan found zero credential-marker or source hygiene findings. Generated `outputs/` and Python cache artifacts are excluded from the source-only bundle.
- The sample project's automated tests and pipeline both exited 0.
- A separate ZIP candidate was created and CRC-checked.
- Academy root navigation, README and CHANGELOG were updated.

## QA
- New module tests: 6/6 passed.
- v5.43 handoff gate tests: 6/6 passed.
- v5.42 publication exporter tests: 4/4 passed.
- Sample project tests: 6/6 passed during candidate build and again after fresh extraction.
- Sample pipeline: exit code 0 during candidate build and fresh extraction.
- Fresh-extraction repository preflight: 0 findings across 14 scanned text files.
- Candidate archive SHA-256: `5ba8a573d16f34b60fa4367f64c9359c3f058808d01c798a1eed8c6d25540934`.

## Limits and pending evidence
The candidate is a locally validated educational project built on synthetic data. The scanner is heuristic, not a security certification. No license was selected, no GitHub repository was created or pushed, no live GitHub Actions run was observed, no remote clean clone was performed, and no independent privacy/provenance review was obtained. Do not claim those milestones as complete.
