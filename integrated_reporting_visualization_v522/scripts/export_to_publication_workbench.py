#!/usr/bin/env python3
"""Copy a v5.22 evidence package into a versioned v5.17 publication handoff folder."""
import argparse, hashlib, json, shutil
from pathlib import Path
from datetime import datetime, timezone

def digest(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source",required=True,help="v5.22 generated output directory")
    ap.add_argument("--destination",required=True,help="New handoff directory, e.g. v5.17/outputs/v522_handoff")
    a=ap.parse_args(); src=Path(a.source).resolve(); dst=Path(a.destination).resolve()
    if not (src/"table1.csv").exists() or not (src/"evidence_manifest.json").exists():
        raise SystemExit("Source must contain table1.csv and evidence_manifest.json")
    if dst.exists() and any(dst.iterdir()): raise SystemExit("Destination exists and is not empty; refusing to overwrite.")
    dst.mkdir(parents=True,exist_ok=True)
    for name in ["table1.csv","executive_summary.md","technical_report.md","report_config.json","evidence_manifest.json"]:
        if (src/name).exists(): shutil.copy2(src/name,dst/name)
    if (src/"figures").exists(): shutil.copytree(src/"figures",dst/"figures",dirs_exist_ok=True)
    manifest={"handoff_created_utc":datetime.now(timezone.utc).isoformat(),"source":str(src),
              "files":[{"path":str(p.relative_to(dst)),"bytes":p.stat().st_size,"sha256":digest(p)}
                       for p in sorted(dst.rglob("*")) if p.is_file()]}
    (dst/"handoff_manifest.json").write_text(json.dumps(manifest,indent=2))
    print(json.dumps({"status":"success","destination":str(dst),"files":len(manifest["files"])},indent=2))
if __name__=="__main__": main()
