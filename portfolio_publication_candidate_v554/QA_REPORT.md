# Portfolio candidate QA report — v5.54.0

## Local build evidence
- Pipeline: passed (exit code 0).
- Unit tests: 6/6 passed.
- Repository preflight: 18 text files scanned, 0 heuristic findings.
- Fresh-directory reproduction: pipeline, tests and preflight all returned exit code 0.
- Source manifest: SHA-256 entries generated for all packaged files except the manifest itself.
- Runtime database, Python bytecode and cache directories removed from publication candidate.

## Analytical outputs from the synthetic dataset
- 24 raw rows; 1 duplicate removed; 23 deduplicated rows.
- 20 eligible completed encounters; 18 completed encounters with valid wait values.
- Cardiology: n=7, mean wait 21.29 minutes.
- General Medicine: n=5 valid waits, mean 32.60 minutes.
- Orthopaedics: n=6, mean wait 33.67 minutes.

## Limitations
All data are fictional synthetic teaching data. The summaries are descriptive, not causal, clinically validated or generalizable to real hospitals. The preflight scanner is heuristic and is not a security audit.

## External gates not completed
No GitHub repository was created or pushed; remote CI was not run; no remote clean clone was verified; no license was selected; no independent human privacy/provenance review was completed.
