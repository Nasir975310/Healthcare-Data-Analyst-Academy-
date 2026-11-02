#!/usr/bin/env python3
"""Check expected v5.38 project artifacts and user-provided review evidence."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from datetime import datetime, timezone

EXPECTED = [
    "README.md",
    "src/run_project.py",
    "tests",
    "sql",
    "data",
    "docs/data_dictionary.md",
    "docs/metric_contract.md",
    "templates/case_study.md",
    "scripts/repository_preflight.py",
]

def audit(project: Path, evidence: Path) -> dict:
    checks = []
    for rel in EXPECTED:
        p = project / rel
        checks.append({"item": rel, "present": p.exists(), "kind": "directory" if p.is_dir() else "file"})
    evidence_items = {
        "case_study_completed": evidence / "case_study_completed.md",
        "reproduction_log": evidence / "reproduction_log.md",
        "employer_scorecard": evidence / "employer_review_scorecard.md",
        "publication_gate": evidence / "publication_gate_completed.md",
    }
    ev = [{"item": k, "present": p.exists(), "nonempty": p.exists() and p.stat().st_size > 0}
          for k, p in evidence_items.items()]
    missing = [x["item"] for x in checks if not x["present"]]
    missing_evidence = [x["item"] for x in ev if not x["present"] or not x["nonempty"]]
    return {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "project_path": str(project),
        "evidence_path": str(evidence),
        "expected_artifacts": checks,
        "user_evidence": ev,
        "missing_artifacts": missing,
        "missing_evidence": missing_evidence,
        "artifact_gate": "PASS" if not missing else "FAIL",
        "user_evidence_gate": "PENDING" if missing_evidence else "EVIDENCE_FILES_PRESENT_REQUIRES_MANUAL_REVIEW",
        "limitations": [
            "Presence checks do not validate correctness or execution.",
            "This tool does not run the upstream pipeline or tests.",
            "It does not inspect GitHub, Power BI, secrets, PHI, or reviewer independence."
        ]
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", type=Path, required=True)
    ap.add_argument("--evidence", type=Path, default=Path("evidence"))
    ap.add_argument("--out", type=Path, default=Path("employer_review_report.json"))
    args = ap.parse_args()
    report = audit(args.project.resolve(), args.evidence.resolve())
    args.out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("Artifact gate:", report["artifact_gate"])
    print("User evidence gate:", report["user_evidence_gate"])
    print("Missing artifacts:", len(report["missing_artifacts"]))
    print("Missing evidence files:", len(report["missing_evidence"]))
    print("Report:", args.out)
    if report["missing_artifacts"]:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
