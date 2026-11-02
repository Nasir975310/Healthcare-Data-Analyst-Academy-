# v5.44.0 — Portfolio Release Candidate Builder

Builds a clean ZIP of the v5.42 sample portfolio project only after checking its source manifest, scanning for common credential markers and runtime artifacts, running its tests and executing its pipeline. The archive contains the project source and documentation, not generated runtime databases/logs.

## Run from the Academy root

```bash
python portfolio_release_candidate_v544/src/release_candidate.py \
  --project github_portfolio_publication_v542/sample_export \
  --out-zip portfolio_release_candidate_v544/output/synthetic_outpatient_portfolio_candidate.zip \
  --report portfolio_release_candidate_v544/output/LOCAL_CANDIDATE_REPORT.json
```

Run module tests:

```bash
python -m unittest discover -s portfolio_release_candidate_v544/tests -v
```

`LOCAL_CANDIDATE_READY` means only that the local source passed these checks and was packaged. It is not a GitHub publication, remote CI, clean remote clone, human privacy review, license approval, Power BI validation or employer acceptance. The scanner is heuristic, not a security product. Inspect every file and confirm data rights before publishing.
