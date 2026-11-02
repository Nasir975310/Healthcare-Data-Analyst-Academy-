#!/usr/bin/env python3
"""Validate externally captured portfolio handoff evidence without fabricating PASS."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
from datetime import datetime, timezone

REQUIRED = {
    "repository": ["url", "default_branch", "commit_sha", "visibility"],
    "publication": ["published_at", "release_tag", "release_url"],
    "clean_clone": ["clone_url", "clone_commit_sha", "clone_test_command", "clone_test_exit_code", "clone_test_log_sha256"],
    "ci": ["workflow_url", "run_id", "conclusion", "run_commit_sha"],
    "review": ["reviewer", "reviewed_at", "privacy_review", "provenance_review", "limitations_acknowledged"],
}
SHA = re.compile(r"^[0-9a-f]{40,64}$")
HASH = re.compile(r"^[0-9a-f]{64}$")
URL = re.compile(r"^https://")

def assess(data: dict) -> dict:
    missing=[]; issues=[]
    if not isinstance(data,dict):
        return {"status":"REVIEW_REQUIRED","missing":["evidence object must be a JSON object"],"issues":[],"scope":"External publication and handoff evidence only; not a general job-readiness certification."}
    for section, fields in REQUIRED.items():
        obj=data.get(section)
        if not isinstance(obj,dict):
            missing.extend(f"{section}.{f}" for f in fields); continue
        for f in fields:
            if obj.get(f) in (None, ""):
                missing.append(f"{section}.{f}")
    if missing:
        return {"status":"NOT_RUN" if not data or all(not isinstance(data.get(s),dict) for s in REQUIRED) else "PENDING_EVIDENCE",
                "missing":missing,"issues":issues,"scope":"External publication and handoff evidence only; not a general job-readiness certification."}
    r,p,c,ci,v=(data[k] for k in ("repository","publication","clean_clone","ci","review"))
    for key,obj in [("repository.url",r),("publication.release_url",p),("clean_clone.clone_url",c),("ci.workflow_url",ci)]:
        val=obj["url"] if key=="repository.url" else obj.get("release_url") if key=="publication.release_url" else obj.get("clone_url") if key=="clean_clone.clone_url" else obj.get("workflow_url")
        if not URL.match(str(val)): issues.append(f"{key} must be an https URL")
    for key,val in [("repository.commit_sha",r["commit_sha"]),("clean_clone.clone_commit_sha",c["clone_commit_sha"]),("ci.run_commit_sha",ci["run_commit_sha"])]:
        if not SHA.match(str(val)): issues.append(f"{key} must be a 40- or 64-character hexadecimal commit hash")
    if not HASH.match(str(c["clone_test_log_sha256"])): issues.append("clean_clone.clone_test_log_sha256 must be a 64-character SHA-256")
    if c["clone_test_exit_code"] != 0: issues.append("clean-clone test command did not exit 0")
    if ci["conclusion"] != "success": issues.append("GitHub Actions conclusion is not success")
    if ci["run_commit_sha"] != r["commit_sha"] or c["clone_commit_sha"] != r["commit_sha"]: issues.append("publication, clean clone and CI evidence do not refer to the same commit")
    if v["privacy_review"] is not True: issues.append("privacy review has not been explicitly passed")
    if v["provenance_review"] is not True: issues.append("data/source provenance review has not been explicitly passed")
    if v["limitations_acknowledged"] is not True: issues.append("reviewer has not acknowledged scope and limitations")
    if r["visibility"] not in ("public","private"): issues.append("repository.visibility must be public or private")
    status="PASS" if not issues else "REVIEW_REQUIRED"
    return {"status":status,"missing":[],"issues":issues,"checked_at_utc":datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
            "commit_sha":r["commit_sha"],"scope":"Evidence consistency for repository publication, clean-clone reproduction, CI and documented human review only.",
            "caveat":"A PASS validates supplied fields and cross-references; it does not independently authenticate GitHub, reviewer identity, privacy compliance or the truth of uploaded evidence."}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument("--evidence",type=Path,required=True);ap.add_argument("--out",type=Path,required=True);a=ap.parse_args()
    try: data=json.loads(a.evidence.read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError) as e: raise SystemExit(f"Cannot read evidence JSON: {e}")
    report=assess(data);a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":report["status"],"missing_count":len(report["missing"]),"issue_count":len(report["issues"]),"report":str(a.out)},indent=2))
    if report["status"]!="PASS": raise SystemExit(2)
if __name__=="__main__":main()
