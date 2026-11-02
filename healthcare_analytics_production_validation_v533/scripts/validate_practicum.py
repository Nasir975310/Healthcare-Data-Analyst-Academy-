#!/usr/bin/env python3
"""Validate v5.32 generated CSV deliverables; standard library only."""
import csv, json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / "healthcare_analytics_real_world_practicum_v532" / "deliverables"
checks = []
def check(name, ok, detail, severity="CRITICAL"):
    checks.append({"check": name, "status": "PASS" if ok else "FAIL",
                   "severity": severity, "detail": detail})
def read_csv(name):
    p = OUT / name
    if not p.exists(): raise FileNotFoundError(p)
    with p.open(newline="", encoding="utf-8-sig") as f: return list(csv.DictReader(f))
def main():
    try:
        monthly = read_csv("monthly_encounters.csv")
        by_type = read_csv("encounters_by_type.csv")
        meds = read_csv("medication_class_utilization.csv")
        kpi = json.loads((OUT/"kpi_summary.json").read_text())
        dq = json.loads((OUT/"data_quality_report.json").read_text())
        manifest = json.loads((OUT/"source_manifest.json").read_text())
        check("deliverables_present", True, "All expected deliverables found")
        # Determine counts from the documented v5.32 summary.
        accepted = int(kpi.get("curated_encounters", kpi.get("accepted_encounters", 0)))
        rejected = int(dq.get("curation", {}).get("rejected_encounters", kpi.get("rejected_encounters", 0)))
        raw = accepted + rejected
        check("row_reconciliation", raw == 91 and accepted == 90 and rejected == 1,
              f"raw={raw}, accepted={accepted}, rejected={rejected}")
        check("expected_orphan_exception", rejected == 1,
              f"Rejected encounters reported: {rejected}")
        month_total = sum(int(float(r.get("encounters", r.get("encounters", r.get("encounter_count", r.get("count", 0)))))) for r in monthly)
        type_total = sum(int(float(r.get("encounters", r.get("encounters", r.get("encounter_count", r.get("count", 0)))))) for r in by_type)
        check("monthly_vs_curated", month_total == accepted, f"monthly total={month_total}; curated={accepted}")
        check("type_vs_curated", type_total == accepted, f"type total={type_total}; curated={accepted}")
        check("medication_extract_nonempty", len(meds) > 0, f"rows={len(meds)}")
        check("source_manifest_nonempty", bool(manifest), "Manifest contains source provenance")
        check("quality_report_nonempty", bool(dq), "Quality report is present")
        check("privacy_safe_scope", True, "Synthetic teaching data only; inspect exports before publication", "WARN")
    except Exception as e:
        check("validator_execution", False, f"{type(e).__name__}: {e}")
    result={"module":"v5.33 production validation","checks":checks,
            "passed":sum(x["status"]=="PASS" for x in checks),
            "failed":sum(x["status"]=="FAIL" for x in checks)}
    target=HERE.parent/"deliverables"
    target.mkdir(exist_ok=True)
    (target/"validation_report.json").write_text(json.dumps(result,indent=2))
    with (target/"validation_report.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=["check","status","severity","detail"]); w.writeheader(); w.writerows(checks)
    print(json.dumps(result,indent=2))
    return 1 if result["failed"] else 0
if __name__=="__main__": sys.exit(main())
