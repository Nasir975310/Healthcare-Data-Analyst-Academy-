# v5.19.0 — Project Execution & Collaboration Environment

A local-first workspace for healthcare analytics projects. It creates a GitHub-ready project scaffold, Python/SQL/R entry points, project plan, task board, reviewer feedback log, change-request register, activity log, release snapshots with SHA-256 file hashes, structural validation, and a heuristic readiness report.

## Quick start

```bash
python scripts/workspace.py init --path ./my_healthcare_project --title "Hypertension prescribing audit" --owner "Analytics team"
python scripts/workspace.py status --path ./my_healthcare_project
python scripts/workspace.py task --path ./my_healthcare_project --id T-001 --status in_progress
python scripts/workspace.py feedback --path ./my_healthcare_project --reviewer "Clinical reviewer" --item "Cohort definition" --status revision_required --comment "Clarify index date"
python scripts/workspace.py change --path ./my_healthcare_project --title "Revise cohort window" --impact high --reason "Stakeholder requested new window"
python scripts/workspace.py snapshot --path ./my_healthcare_project --version 0.1.0 --note "Baseline before analysis"
python scripts/workspace.py validate --path ./my_healthcare_project
```

## Operating boundaries

The activity log is append-only by this tool but is not tamper-proof or a regulated audit trail. Snapshot records hash files at the time of snapshot; they do not freeze files or guarantee reproducibility. The readiness score is a heuristic. The tool does not execute arbitrary analysis scripts, synchronize users, manage permissions, validate clinical methods, or certify privacy/regulatory compliance. Use an approved version-control and access-control system for team collaboration. Never commit PHI, credentials, or client-confidential data.
