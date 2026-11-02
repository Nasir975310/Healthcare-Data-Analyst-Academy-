#!/usr/bin/env python3
"""Evaluate project acceptance without treating missing external proof as success."""
import json, pathlib, sys
HERE=pathlib.Path(__file__).resolve().parent
E=HERE.parent/"evidence"
def load(name):
 p=E/name
 if not p.exists(): return None
 try:return json.loads(p.read_text())
 except Exception:return None
local=load("local_evidence.json")
pg=load("postgres_validation.json")
pb=load("powerbi_validation.json")
gh=load("github_publication.json")
checks=[
 {"gate":"Local Python/SQLite evidence","status":"PASS" if local and local.get("local_status")=="PASS" else "FAIL"},
 {"gate":"PostgreSQL container validation","status":"PASS" if pg and pg.get("status")=="PASS" else "PENDING"},
 {"gate":"Power BI Desktop validation","status":"PASS" if pb and pb.get("status")=="PASS" else "PENDING"},
 {"gate":"GitHub publication evidence","status":"PASS" if gh and gh.get("status")=="PASS" else "PENDING"}
]
failed=any(x["status"]=="FAIL" for x in checks)
pending=any(x["status"]=="PENDING" for x in checks)
result={"checks":checks,"overall":"NOT_ACCEPTED" if failed else ("PARTIALLY_VERIFIED" if pending else "ACCEPTED"),
        "note":"Only evidence files with status PASS count. Review evidence provenance before accepting."}
print(json.dumps(result,indent=2))
sys.exit(1 if failed else (2 if pending else 0))
