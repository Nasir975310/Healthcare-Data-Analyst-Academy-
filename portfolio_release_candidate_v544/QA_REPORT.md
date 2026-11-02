# v5.44.0 QA report

- Release-candidate builder unit tests: 6/6 passed.
- v5.43 handoff-gate tests: 6/6 passed.
- v5.42 publication exporter tests: 4/4 passed.
- Sample portfolio project tests: 6/6 passed during the build and again after extracting the candidate ZIP into a fresh temporary directory.
- Sample pipeline: exit code 0 during the build and after fresh extraction.
- Fresh-extraction repository preflight: 0 findings across 14 scanned text files.
- Source manifest: 14 entries checked, no mismatches.
- Source hygiene scan: 0 findings.
- Candidate ZIP CRC: passed.

The candidate builder status is `LOCAL_CANDIDATE_READY`. This validates local packaging/reproduction only. GitHub publication, remote CI, a clean clone from the remote, license decision and independent human review remain pending. The heuristic scanner is not a security certification.
