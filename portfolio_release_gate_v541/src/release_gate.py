#!/usr/bin/env python3
"""Compare learner-captured local execution evidence with v5.40 reference artifacts."""
from __future__ import annotations
import argparse, csv, hashlib, json
from pathlib import Path

EXPECTED=("quality_report.json","department_summary.csv","sha256_manifest.json")

def sha256(p:Path)->str:
    h=hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def load_json(p:Path):
    return json.loads(p.read_text(encoding="utf-8"))

def compare(local_dir:Path, reference_dir:Path)->dict:
    report_path=local_dir/"local_run_report.json"
    if not report_path.is_file():
        return {"status":"NOT_RUN","reason":"local_run_report.json not found; no local execution evidence was supplied.","checks":[]}
    local=load_json(report_path)
    checks=[]
    commands=local.get("commands",[])
    all_zero=bool(commands) and all(x.get("exit_code")==0 for x in commands)
    checks.append({"check":"all_commands_exit_zero","passed":all_zero,"detail":f"{sum(x.get('exit_code')==0 for x in commands)}/{len(commands)} commands exited zero"})
    captured={x.get("file"):x for x in local.get("captured_outputs",[])}
    for name in EXPECTED:
        lp=local_dir/name; rp=reference_dir/name
        exists=lp.is_file() and rp.is_file()
        same=exists and sha256(lp)==sha256(rp)
        checks.append({"check":f"{name}_present","passed":exists,"detail":"local and reference files must both exist"})
        if exists:
            checks.append({"check":f"{name}_matches_reference","passed":same,"detail":"SHA-256 exact match" if same else "SHA-256 differs; investigate source, code, environment or nondeterminism"})
        declared=captured.get(name)
        checks.append({"check":f"{name}_declared_hash_valid","passed":bool(declared and lp.is_file() and declared.get("sha256")==sha256(lp)),"detail":"captured manifest entry must match the local file"})
    checks.append({"check":"environment_recorded","passed":bool(local.get("platform") and local.get("python")),"detail":"platform and Python version recorded"})
    passed=all(c["passed"] for c in checks)
    return {
        "status":"PASS" if passed else "REVIEW_REQUIRED",
        "local_report":str(report_path),
        "source_project_path":local.get("project_path"),
        "checks":checks,
        "passed_checks":sum(c["passed"] for c in checks),
        "total_checks":len(checks),
        "interpretation":"A pass means captured outputs match the supplied reference and commands exited zero. It does not prove clean-clone publication, privacy clearance, authorship or employer readiness."
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--local",type=Path,required=True)
    ap.add_argument("--reference",type=Path,required=True)
    ap.add_argument("--out",type=Path,default=Path("release_gate_report.json"))
    a=ap.parse_args()
    result=compare(a.local.resolve(),a.reference.resolve())
    a.out.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":result["status"],"passed_checks":result.get("passed_checks",0),"total_checks":result.get("total_checks",0),"report":str(a.out)},indent=2))
    if result["status"]=="REVIEW_REQUIRED": raise SystemExit(1)
if __name__=="__main__": main()
