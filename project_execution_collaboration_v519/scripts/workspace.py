#!/usr/bin/env python3
"""Local-first healthcare analytics project workspace and delivery governance CLI."""
from __future__ import annotations
import argparse, csv, hashlib, json, os, re, shutil, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

def now(): return datetime.now(timezone.utc).isoformat()
def load(path, default):
    if not path.exists(): return default
    return json.loads(path.read_text(encoding="utf-8"))
def save(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,indent=2),encoding="utf-8")
def digest(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()
def append_event(project,event,details):
    p=project/"governance"/"activity_log.jsonl"; p.parent.mkdir(parents=True,exist_ok=True)
    with p.open("a",encoding="utf-8") as f: f.write(json.dumps({"timestamp":now(),"event":event,"details":details},ensure_ascii=False)+"\n")
def init_project(path,title,owner):
    if path.exists() and any(path.iterdir()): raise FileExistsError(f"Project directory is not empty: {path}")
    for d in ["data/raw","data/processed","src/python","src/sql","src/r","tests","reports","docs","governance","outputs"]: (path/d).mkdir(parents=True,exist_ok=True)
    meta={"title":title,"owner":owner,"created_utc":now(),"workspace_version":"5.19.0","status":"active"}
    save(path/"project.json",meta)
    save(path/"governance"/"tasks.json",[
      {"id":"T-001","title":"Confirm scope and analysis question","status":"todo","priority":"high","owner":owner},
      {"id":"T-002","title":"Approve data source and governance","status":"todo","priority":"high","owner":owner},
      {"id":"T-003","title":"Define cohort and variables","status":"todo","priority":"high","owner":owner},
      {"id":"T-004","title":"Implement reproducible analysis","status":"todo","priority":"medium","owner":owner},
      {"id":"T-005","title":"Validate outputs and peer review","status":"todo","priority":"high","owner":owner},
      {"id":"T-006","title":"Prepare client handover","status":"todo","priority":"medium","owner":owner}])
    save(path/"governance"/"review_feedback.json",[])
    save(path/"governance"/"change_requests.json",[])
    save(path/"governance"/"releases.json",[])
    (path/"src/python"/"analysis.py").write_text('"""Analysis entry point. Replace only with approved, reproducible methods."""\nfrom pathlib import Path\n\nPROJECT_ROOT = Path(__file__).resolve().parents[2]\n\nif __name__ == "__main__":\n    print("Workspace ready. Add approved analysis steps and tests.")\n',encoding="utf-8")
    (path/"src/sql"/"analysis.sql").write_text("-- SQL analysis template: document dialect, source tables, cohort, and date window.\n-- Never embed credentials or expose patient-level records in public outputs.\nSELECT 1 AS workspace_smoke_test;\n",encoding="utf-8")
    (path/"src/r"/"analysis.R").write_text('# R analysis template\nmessage("Workspace ready. Add approved analysis steps and tests.")\n',encoding="utf-8")
    (path/"tests"/"README.md").write_text("# Tests\nAdd unit tests for transformations, cohort rules, and derived metrics. Keep synthetic fixtures separate from governed source data.\n",encoding="utf-8")
    (path/".gitignore").write_text(".venv/\nvenv/\n__pycache__/\n.pytest_cache/\n.env\n*.pem\n*.key\ndata/raw/\ndata/patient_level/\n*.sqlite\n*.db\noutputs/\n",encoding="utf-8")
    (path/"README.md").write_text(f"# {title}\n\nOwner: {owner}\n\nStart with `project.json` and `docs/PROJECT_PLAN.md`. Use `python workspace.py status` to inspect governance status.\n\nDo not commit patient-level data, credentials, or client-confidential material.\n",encoding="utf-8")
    (path/"docs"/"PROJECT_PLAN.md").write_text("# Project plan\n\n## Analysis question\nDefine the decision and intended use.\n\n## Population and cohort\nDocument eligibility, exclusions, index date, follow-up, and unit of analysis.\n\n## Variables and outcomes\nDefine operational definitions, units, time windows, and source lineage.\n\n## Methods\nSpecify descriptive/inferential methods, assumptions, missing-data strategy, and sensitivity analyses.\n\n## Governance\nRecord authorization, classification, access controls, retention, and reviewer approvals.\n",encoding="utf-8")
    append_event(path,"project_initialized",{"title":title,"owner":owner})
    return path
def update_task(project,task_id,status):
    tasks=load(project/"governance"/"tasks.json",[])
    found=False
    for t in tasks:
        if t["id"]==task_id:
            if status not in {"todo","in_progress","blocked","done"}: raise ValueError("Invalid task status")
            t["status"]=status; t["updated_utc"]=now(); found=True
    if not found: raise KeyError(f"Unknown task: {task_id}")
    save(project/"governance"/"tasks.json",tasks); append_event(project,"task_updated",{"id":task_id,"status":status})
def add_record(project,filename,record,event):
    p=project/"governance"/filename; records=load(p,[]); record["created_utc"]=now(); records.append(record); save(p,records); append_event(project,event,record)
def validate_project(project):
    problems=[]
    for rel in ["project.json","governance/tasks.json","governance/review_feedback.json","governance/change_requests.json","governance/releases.json","src/python/analysis.py","src/sql/analysis.sql","src/r/analysis.R","docs/PROJECT_PLAN.md"]:
        if not (project/rel).exists(): problems.append(f"Missing required file: {rel}")
    try:
        meta=load(project/"project.json",{})
        if not meta.get("title"): problems.append("Project title is missing")
        tasks=load(project/"governance/tasks.json",[])
        ids=[t.get("id") for t in tasks]
        if len(ids)!=len(set(ids)): problems.append("Duplicate task IDs")
        for t in tasks:
            if t.get("status") not in {"todo","in_progress","blocked","done"}: problems.append(f"Invalid status for task {t.get('id')}")
    except Exception as e: problems.append(f"Invalid governance JSON: {e}")
    return problems
def readiness(project):
    checks=[
      ("scope","Analysis question and scope documented",(project/"docs"/"PROJECT_PLAN.md").exists() and "Define the decision" not in (project/"docs"/"PROJECT_PLAN.md").read_text(encoding="utf-8")),
      ("source_governance","Source authorization and classification recorded",False),
      ("cohort","Cohort and variable definitions approved",False),
      ("code","Python, SQL and R entry points present",all((project/p).exists() for p in ["src/python/analysis.py","src/sql/analysis.sql","src/r/analysis.R"])),
      ("tests","Test strategy documented",(project/"tests"/"README.md").exists()),
      ("peer_review","At least one review marked accepted",any(x.get("status")=="accepted" for x in load(project/"governance"/"review_feedback.json",[]))),
      ("change_control","No unresolved high-impact change requests",not any(x.get("impact")=="high" and x.get("status") not in {"approved","rejected","implemented"} for x in load(project/"governance"/"change_requests.json",[]))),
      ("tasks","All tasks complete",bool(load(project/"governance"/"tasks.json",[])) and all(t.get("status")=="done" for t in load(project/"governance"/"tasks.json",[]))),
      ("release","A release record exists",bool(load(project/"governance"/"releases.json",[]))),
      ("handover","Handover documentation exists",(project/"docs"/"HANDOVER.md").exists())
    ]
    passed=sum(bool(x[2]) for x in checks)
    return {"score_percent":round(passed*100/len(checks)),"passed":passed,"total":len(checks),"checks":[{"id":i,"label":l,"passed":bool(v)} for i,l,v in checks],
      "interpretation":"Heuristic readiness indicator only; it is not clinical, privacy, regulatory, or client acceptance certification."}
def snapshot(project,version,note):
    files=[]
    for p in sorted(project.rglob("*")):
        if p.is_file() and ".git" not in p.parts and "__pycache__" not in p.parts and p.name!="releases.json":
            files.append({"path":str(p.relative_to(project)),"sha256":digest(p),"bytes":p.stat().st_size})
    rec={"version":version,"note":note,"created_utc":now(),"file_count":len(files),"files":files}
    p=project/"governance"/"releases.json"; arr=load(p,[]); arr.append(rec); save(p,arr); append_event(project,"release_snapshot_created",{"version":version,"file_count":len(files)})
    return rec
def status(project):
    return {"project":load(project/"project.json",{}),"tasks":load(project/"governance"/"tasks.json",[]),
      "feedback_count":len(load(project/"governance"/"review_feedback.json",[])),
      "change_requests":load(project/"governance"/"change_requests.json",[]),
      "readiness":readiness(project),"validation_errors":validate_project(project)}
def main():
    ap=argparse.ArgumentParser(description=__doc__); sub=ap.add_subparsers(dest="cmd",required=True)
    p=sub.add_parser("init"); p.add_argument("--path",required=True,type=Path); p.add_argument("--title",required=True); p.add_argument("--owner",default="Project team")
    p=sub.add_parser("status"); p.add_argument("--path",required=True,type=Path)
    p=sub.add_parser("task"); p.add_argument("--path",required=True,type=Path); p.add_argument("--id",required=True); p.add_argument("--status",required=True)
    p=sub.add_parser("feedback"); p.add_argument("--path",required=True,type=Path); p.add_argument("--reviewer",required=True); p.add_argument("--item",required=True); p.add_argument("--status",choices=["open","accepted","revision_required"],default="open"); p.add_argument("--comment",default="")
    p=sub.add_parser("change"); p.add_argument("--path",required=True,type=Path); p.add_argument("--title",required=True); p.add_argument("--impact",choices=["low","medium","high"],default="medium"); p.add_argument("--status",choices=["proposed","approved","rejected","implemented"],default="proposed"); p.add_argument("--reason",default="")
    p=sub.add_parser("snapshot"); p.add_argument("--path",required=True,type=Path); p.add_argument("--version",required=True); p.add_argument("--note",default="")
    p=sub.add_parser("validate"); p.add_argument("--path",required=True,type=Path)
    a=ap.parse_args()
    if a.cmd=="init": init_project(a.path,a.title,a.owner); result={"created":str(a.path)}
    elif a.cmd=="status": result=status(a.path)
    elif a.cmd=="task": update_task(a.path,a.id,a.status); result={"updated":a.id,"status":a.status}
    elif a.cmd=="feedback":
        add_record(a.path,"review_feedback.json",{"reviewer":a.reviewer,"item":a.item,"status":a.status,"comment":a.comment},"review_feedback_added"); result={"recorded":True}
    elif a.cmd=="change":
        add_record(a.path,"change_requests.json",{"id":f"CR-{len(load(a.path/'governance'/'change_requests.json',[]))+1:03d}","title":a.title,"impact":a.impact,"status":a.status,"reason":a.reason},"change_request_added"); result={"recorded":True}
    elif a.cmd=="snapshot": result=snapshot(a.path,a.version,a.note)
    else: result={"errors":validate_project(a.path)}
    print(json.dumps(result,indent=2))
if __name__=="__main__": main()
