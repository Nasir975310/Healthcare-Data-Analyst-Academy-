#!/usr/bin/env python3
"""Lightweight, transparent checklist scorer for a take-home submission."""
import argparse
import json
from pathlib import Path

CHECKS = {
    "states_grain": ("States analysis grain", lambda s: bool(s.get("grain", "").strip())),
    "defines_cohort": ("Defines cohort and exclusions", lambda s: len(s.get("inclusion_rules", [])) >= 2 and len(s.get("exclusion_rules", [])) >= 1),
    "sql_uses_distinct_or_dedup": ("Addresses duplicate handling in SQL", lambda s: any(x in s.get("sql", "").lower() for x in ("distinct", "row_number", "group by"))),
    "sql_has_time_grouping": ("Groups by reporting period", lambda s: any(x in s.get("sql", "").lower() for x in ("date_trunc", "strftime", "week", "month"))),
    "python_checks_missing": ("Python checks missingness", lambda s: any(x in s.get("python", "").lower() for x in ("isna", "isnull", "notna"))),
    "python_checks_duplicates": ("Python checks duplicates", lambda s: "duplicat" in s.get("python", "").lower()),
    "reports_reconciliation": ("Reports row-count reconciliation", lambda s: bool(s.get("row_count_reconciliation", "").strip())),
    "states_limitations": ("States at least one limitation", lambda s: len(s.get("limitations", [])) >= 1),
    "has_qa_tests": ("Includes at least three QA checks", lambda s: len(s.get("qa_checks", [])) >= 3),
    "privacy_statement": ("States synthetic/de-identified data boundary", lambda s: any(x in s.get("data_privacy", "").lower() for x in ("synthetic", "de-identified"))),
}

def score(payload):
    results = []
    for key, (label, fn) in CHECKS.items():
        try:
            passed = bool(fn(payload))
        except (AttributeError, TypeError):
            passed = False
        results.append({"id": key, "label": label, "passed": passed})
    passed = sum(x["passed"] for x in results)
    return {"passed": passed, "total": len(results), "percent": round(passed / len(results) * 100), "checks": results,
            "interpretation": "Checklist completeness only; not a measure of analytical correctness, employability or employer acceptance."}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to JSON submission checklist")
    parser.add_argument("--output", help="Optional path to write JSON result")
    args = parser.parse_args()
    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    result = score(payload)
    rendered = json.dumps(result, indent=2)
    if args.output:
        Path(args.output).write_text(rendered + "\\n", encoding="utf-8")
    print(rendered)
    return 0 if result["passed"] == result["total"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
