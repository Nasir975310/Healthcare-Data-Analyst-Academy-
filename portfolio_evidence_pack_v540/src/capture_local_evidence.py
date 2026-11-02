#!/usr/bin/env python3
"""Run the v5.38 synthetic project and capture safe, inspectable evidence files."""
from __future__ import annotations
import argparse, hashlib, json, platform, shutil, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--project",type=Path,required=True,help="Path to portfolio_execution_reproducibility_v538")
    ap.add_argument("--destination",type=Path,default=Path("local_run"))
    args=ap.parse_args()
    project=args.project.resolve(); dest=args.destination.resolve()
    if not (project/"src/run_project.py").is_file(): raise SystemExit("Cannot find src/run_project.py under --project")
    dest.mkdir(parents=True,exist_ok=True)
    commands=[
        [sys.executable,"src/run_project.py"],
        [sys.executable,"-m","unittest","discover","-s","tests","-v"],
        [sys.executable,"scripts/repository_preflight.py"]
    ]
    records=[]
    for cmd in commands:
        p=subprocess.run(cmd,cwd=project,capture_output=True,text=True)
        records.append({"command":cmd,"exit_code":p.returncode,"stdout":p.stdout,"stderr":p.stderr})
    outputs=project/"outputs"
    copied=[]
    for name in ("quality_report.json","department_summary.csv","sha256_manifest.json"):
        source=outputs/name
        if source.exists():
            target=dest/name; shutil.copy2(source,target)
            copied.append({"file":name,"sha256":sha256(target),"bytes":target.stat().st_size})
    report={
        "captured_utc":datetime.now(timezone.utc).isoformat(),
        "platform":platform.platform(),
        "python":sys.version,
        "project_path":str(project),
        "commands":records,
        "captured_outputs":copied,
        "all_commands_exit_zero":all(x["exit_code"]==0 for x in records),
        "scope":"Local run evidence only; does not prove clean-clone status, public publication, privacy clearance or independent review."
    }
    (dest/"local_run_report.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"all_commands_exit_zero":report["all_commands_exit_zero"],"captured_outputs":copied,"report":str(dest/"local_run_report.json")},indent=2))
    if not report["all_commands_exit_zero"]: raise SystemExit(1)
if __name__=="__main__": main()
