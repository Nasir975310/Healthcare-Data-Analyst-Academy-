#!/usr/bin/env python3
"""Run the focused acceptance suite for the v5.55-v5.60 career workflow."""
from __future__ import annotations
import ast
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUITES = [
    ("career_launch_kit_v555", 5),
    ("application_intelligence_v556", 7),
    ("application_execution_interview_v557", 6),
    ("application_performance_career_intelligence_v558", 6),
    ("job_search_source_vacancy_verification_v559", 6),
    ("vacancy_sourcing_evidence_capture_v560", 6),
]

def main() -> int:
    total = 0
    failed = []
    for module, expected in SUITES:
        cmd = [sys.executable, "-B", "-m", "unittest", "discover", "-s", f"{module}/tests", "-v"]
        result = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = result.stdout
        marker = next((line for line in reversed(output.splitlines()) if line.startswith("Ran ")), "summary missing")
        count = int(marker.split()[1]) if marker.startswith("Ran ") else 0
        total += count
        status = "PASS" if result.returncode == 0 and count == expected else "FAIL"
        print(f"{status:4} {module}: {marker}; expected={expected}")
        if status == "FAIL":
            failed.append((module, output[-4000:]))
    SKIP_PARTS = {'.git', '.venv', 'venv', '__pycache__', 'node_modules'}
    python_files = [p for p in ROOT.rglob("*.py") if not any(part in SKIP_PARTS for part in p.parts)]
    syntax_errors = []
    for path in python_files:
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except Exception as exc:  # report exact path and parser error
            syntax_errors.append((path, exc))
    print(f"AST: {len(python_files) - len(syntax_errors)}/{len(python_files)} Python files parsed")
    for path, exc in syntax_errors:
        print(f"AST FAIL {path}: {exc}")
    if failed or syntax_errors:
        for module, output in failed:
            print(f"\n--- {module} failure detail ---\n{output}")
        return 1
    print(f"ACCEPTANCE PASS: {total} tests across {len(SUITES)} suites")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
