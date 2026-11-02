# v5.43.0 — Portfolio Handoff & External Evidence Verification

This cumulative release adds a structured external-evidence gate. It checks repository and release metadata, commit identity across the repository/clean clone/CI run, clean-clone test exit code and log SHA-256, and explicit privacy/provenance review flags.

The gate starts at `NOT_RUN`: this build did not publish to GitHub, run GitHub Actions, perform a clean clone from a remote or obtain independent review. Unit-test fixtures validate the logic only.
