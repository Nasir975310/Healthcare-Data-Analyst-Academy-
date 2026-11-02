# Portfolio release workflow

1. Review the synthetic project's README, case study, metric contract, data dictionary and limitations.
2. Inspect all included files manually. The automated scanner only catches a small set of common patterns.
3. Run the release candidate builder and retain its JSON report and archive SHA-256.
4. Extract the candidate ZIP into a new directory and run its README commands there.
5. Create a Git repository in that extracted directory only after choosing an appropriate license and repository visibility.
6. Push to a new, dedicated portfolio repository. Do not reuse an unrelated personal or application repository.
7. Capture the remote commit SHA, GitHub Actions run URL and clean-clone test log hash in the v5.43 handoff evidence template.
8. Obtain a human privacy/provenance review. Never upload real patient data or confidential employer data.

## Local commands after extraction

```bash
python src/run_project.py
python -m unittest discover -s tests -v
python scripts/repository_preflight.py
```

Expected outputs are described in `docs/reference_results.md`. The data are synthetic and are not clinical evidence.
