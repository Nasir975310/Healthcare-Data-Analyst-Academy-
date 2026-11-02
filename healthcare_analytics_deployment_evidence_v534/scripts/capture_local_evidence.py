#!/usr/bin/env python3
"""Capture local reproducibility evidence without inventing external completion."""
import hashlib, json, pathlib, platform, subprocess, sys, time
HERE=pathlib.Path(__file__).resolve().parent
MODULE=HERE.parent
ACADEMY=MODULE.parent
PRACTICUM=ACADEMY/"healthcare_analytics_real_world_practicum_v532"
V533=ACADEMY/"healthcare_analytics_production_validation_v533"
def sha256(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()
def run(args,cwd):
    p=subprocess.run(args,cwd=cwd,capture_output=True,text=True)
    return {"command":" ".join(map(str,args)),"return_code":p.returncode,
            "stdout_tail":p.stdout[-3000:],"stderr_tail":p.stderr[-1000:]}
def main():
    evidence_dir=MODULE/"evidence"; evidence_dir.mkdir(exist_ok=True)
    tests=run([sys.executable,"-m","unittest","discover","-s",str(MODULE/"tests"),"-v"],ACADEMY)
    validator=run([sys.executable,str(V533/"scripts/validate_practicum.py")],ACADEMY)
    benchmark=run([sys.executable,str(V533/"scripts/benchmark_sqlite.py")],ACADEMY)
    files=[]
    for base in [PRACTICUM/"data/raw",PRACTICUM/"deliverables"]:
        if base.exists():
            for p in sorted(base.iterdir()):
                if p.is_file() and p.suffix not in {".sqlite",".db"}:
                    files.append({"path":str(p.relative_to(ACADEMY)),"bytes":p.stat().st_size,"sha256":sha256(p)})
    result={
      "generated_at_utc":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),
      "python":sys.version.split()[0],"platform":platform.platform(),
      "checks":{"unit_tests":tests,"practicum_validator":validator,"sqlite_benchmark":benchmark},
      "external_integrations":{"postgresql":"PENDING_UNTIL_DOCKER_WORKFLOW_RUNS",
        "power_bi":"PENDING_EXTERNAL_DESKTOP_EVIDENCE","github":"PENDING_USER_REPOSITORY_PUSH"},
      "source_and_deliverable_hashes":files
    }
    result["local_status"]="PASS" if all(x["return_code"]==0 for x in [tests,validator,benchmark]) else "FAIL"
    out=evidence_dir/"local_evidence.json"
    out.write_text(json.dumps(result,indent=2))
    print(json.dumps({"local_status":result["local_status"],"evidence_file":str(out),
      "unit_tests_rc":tests["return_code"],"validator_rc":validator["return_code"],
      "benchmark_rc":benchmark["return_code"],"hashed_files":len(files)},indent=2))
    return 0 if result["local_status"]=="PASS" else 1
if __name__=="__main__":sys.exit(main())
