#!/usr/bin/env python3
"""Execute reproducible local Python, CSV-to-SQLite, read-only SQL, and declarative data pipelines."""
from __future__ import annotations
import argparse, csv, hashlib, json, os, re, sqlite3, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

def utc(): return datetime.now(timezone.utc).isoformat()
def sha(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()
def load_json(p,default):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default
def save_json(p,obj):
    p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(obj,indent=2),encoding="utf-8")
def project_path(p):
    p=Path(p).resolve()
    if not (p/"project.json").is_file(): raise FileNotFoundError(f"Not a recognized project workspace: {p}")
    return p
def record_run(project,kind,command,status,started,duration,inputs,outputs,log_path,exit_code):
    runs=project/"governance"/"execution_runs.json"
    arr=load_json(runs,[])
    rec={"run_id":f"RUN-{len(arr)+1:04d}","kind":kind,"command":command,"status":status,
         "started_utc":started,"duration_seconds":round(duration,3),"inputs":inputs,"outputs":outputs,
         "log":str(log_path.relative_to(project)) if log_path.is_relative_to(project) else str(log_path),
         "exit_code":exit_code}
    arr.append(rec); save_json(runs,arr)
    with (project/"governance"/"activity_log.jsonl").open("a",encoding="utf-8") as f:
        f.write(json.dumps({"timestamp":utc(),"event":"execution_run_recorded","details":rec})+"\n")
    return rec
def run_python(project,script_path,timeout=120):
    project=project_path(project); src=Path(script_path)
    if not src.is_absolute(): src=project/src
    src=src.resolve()
    if not src.is_file(): raise FileNotFoundError(src)
    started=utc(); t=time.monotonic()
    logdir=project/"outputs"/"execution_logs"; logdir.mkdir(parents=True,exist_ok=True)
    logfile=logdir/f"python_{len(list(logdir.glob('python_*.log')))+1:04d}.log"
    env=os.environ.copy(); env["HDA_PROJECT_ROOT"]=str(project)
    try:
        cp=subprocess.run([sys.executable,str(src)],cwd=project,env=env,capture_output=True,text=True,timeout=timeout)
        code=cp.returncode; status="succeeded" if code==0 else "failed"
        body=f"COMMAND: {sys.executable} {src}\nEXIT CODE: {code}\n\n--- STDOUT ---\n{cp.stdout}\n--- STDERR ---\n{cp.stderr}"
    except subprocess.TimeoutExpired as e:
        code=124; status="timeout"
        body=f"COMMAND: {sys.executable} {src}\nTIMEOUT: {timeout}s\n\n--- STDOUT ---\n{e.stdout or ''}\n--- STDERR ---\n{e.stderr or ''}"
    logfile.write_text(body,encoding="utf-8")
    rec=record_run(project,"python",str(src),status,started,time.monotonic()-t,[{"path":str(src.relative_to(project)) if src.is_relative_to(project) else str(src),"sha256":sha(src)}],[],logfile,code)
    return rec
def validate_identifier(name):
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*",name): raise ValueError(f"Unsafe SQL identifier: {name}")
    return name
def load_csv_sqlite(project,csv_path,table):
    project=project_path(project); src=Path(csv_path)
    if not src.is_absolute(): src=project/src
    src=src.resolve(); table=validate_identifier(table)
    if not src.is_file(): raise FileNotFoundError(src)
    with src.open(newline="",encoding="utf-8-sig") as f:
        reader=csv.DictReader(f)
        if not reader.fieldnames: raise ValueError("CSV must contain a header row")
        cols=[validate_identifier(c) for c in reader.fieldnames]
        rows=list(reader)
    db=project/"data"/"processed"/"analytics.sqlite"; db.parent.mkdir(parents=True,exist_ok=True)
    con=sqlite3.connect(db)
    try:
        col_sql=", ".join('"'+c+'" TEXT' for c in cols)
        con.execute(f'DROP TABLE IF EXISTS "{table}"')
        con.execute(f'CREATE TABLE "{table}" ({col_sql})')
        placeholders=", ".join("?" for _ in cols)
        con.executemany(f'INSERT INTO "{table}" VALUES ({placeholders})',[[r.get(c) for c in reader.fieldnames] for r in rows])
        con.commit()
    finally: con.close()
    rec={"database":str(db.relative_to(project)),"table":table,"rows_loaded":len(rows),"columns":cols,"source_sha256":sha(src),"database_sha256":sha(db)}
    save_json(project/"outputs"/"last_csv_load.json",rec)
    with (project/"governance"/"activity_log.jsonl").open("a",encoding="utf-8") as f:f.write(json.dumps({"timestamp":utc(),"event":"csv_loaded_to_sqlite","details":rec})+"\n")
    return rec
def read_only_query(project,sql,output_name="query_result.csv",limit=100000):
    project=project_path(project)
    normalized=sql.strip()
    if not normalized: raise ValueError("SQL query is empty")
    # Only one SELECT or WITH statement. SQLite's read-only connection and authorizer provide a second boundary.
    if not re.match(r"(?is)^(select|with)\b",normalized): raise ValueError("Only SELECT or WITH queries are allowed")
    if ";" in normalized.rstrip(";"): raise ValueError("Multiple SQL statements are not allowed")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+\.csv",output_name): raise ValueError("Output must be a simple CSV filename")
    db=project/"data"/"processed"/"analytics.sqlite"
    if not db.is_file(): raise FileNotFoundError("SQLite database not found; load a CSV first")
    uri="file:"+quote(str(db))+"?mode=ro"
    con=sqlite3.connect(uri,uri=True)
    def authorizer(action,arg1,arg2,dbname,source):
        denied={sqlite3.SQLITE_INSERT,sqlite3.SQLITE_UPDATE,sqlite3.SQLITE_DELETE,sqlite3.SQLITE_ALTER_TABLE,
                sqlite3.SQLITE_DROP_TABLE,sqlite3.SQLITE_DROP_INDEX,sqlite3.SQLITE_CREATE_TABLE,
                sqlite3.SQLITE_CREATE_INDEX,sqlite3.SQLITE_ATTACH,sqlite3.SQLITE_DETACH,
                sqlite3.SQLITE_PRAGMA,sqlite3.SQLITE_TRANSACTION}
        return sqlite3.SQLITE_DENY if action in denied else sqlite3.SQLITE_OK
    con.set_authorizer(authorizer)
    try:
        cur=con.execute(normalized)
        cols=[d[0] for d in cur.description or []]
        rows=cur.fetchmany(limit+1)
        if len(rows)>limit: raise ValueError(f"Query exceeded row limit ({limit}); add a WHERE clause or LIMIT")
    finally: con.close()
    out=project/"outputs"/output_name; out.parent.mkdir(parents=True,exist_ok=True)
    with out.open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(cols); w.writerows(rows)
    return {"rows":len(rows),"columns":cols,"output":str(out.relative_to(project)),"sha256":sha(out)}
def run_pipeline(project,config_path):
    project=project_path(project); cfgp=Path(config_path)
    if not cfgp.is_absolute(): cfgp=project/cfgp
    cfg=json.loads(cfgp.read_text(encoding="utf-8"))
    src=Path(cfg["input"])
    if not src.is_absolute(): src=project/src
    if not src.is_file(): raise FileNotFoundError(src)
    with src.open(newline="",encoding="utf-8-sig") as f:
        reader=csv.DictReader(f); fields=list(reader.fieldnames or []); rows=list(reader)
    rows_input=len(rows)
    for step in cfg.get("steps",[]):
        op=step.get("op")
        if op=="drop_duplicates":
            key=step.get("key")
            if key not in fields: raise ValueError(f"Unknown duplicate key: {key}")
            seen=set(); unique=[]
            for row in rows:
                if row.get(key) not in seen: seen.add(row.get(key)); unique.append(row)
            rows=unique
        elif op=="filter_equals":
            col=step.get("column")
            if col not in fields: raise ValueError(f"Unknown filter column: {col}")
            rows=[r for r in rows if r.get(col)==str(step.get("value",""))]
        elif op=="rename":
            old,new=step.get("from"),step.get("to")
            if old not in fields or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*",str(new)): raise ValueError("Invalid rename")
            if new in fields: raise ValueError(f"Rename target already exists: {new}")
            fields[fields.index(old)]=new
            for r in rows: r[new]=r.pop(old)
        elif op=="select_columns":
            selected=step.get("columns",[])
            if not selected or any(c not in fields for c in selected): raise ValueError("Invalid selected columns")
            fields=selected; rows=[{c:r.get(c,"") for c in fields} for r in rows]
        else: raise ValueError(f"Unsupported pipeline operation: {op}")
    out=Path(cfg.get("output","data/processed/pipeline_output.csv"))
    if not out.is_absolute(): out=project/out
    out.parent.mkdir(parents=True,exist_ok=True)
    with out.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
    return {"input":str(src.relative_to(project)) if src.is_relative_to(project) else str(src),"input_sha256":sha(src),
            "rows_input":rows_input,"rows_output":len(rows),"columns":fields,
            "output":str(out.relative_to(project)) if out.is_relative_to(project) else str(out),"output_sha256":sha(out),
            "steps":cfg.get("steps",[])}
def main():
    ap=argparse.ArgumentParser(description=__doc__); sub=ap.add_subparsers(dest="cmd",required=True)
    p=sub.add_parser("run-python"); p.add_argument("--project",required=True,type=Path); p.add_argument("--script",required=True); p.add_argument("--timeout",type=int,default=120)
    p=sub.add_parser("load-csv"); p.add_argument("--project",required=True,type=Path); p.add_argument("--input",required=True); p.add_argument("--table",required=True)
    p=sub.add_parser("query-sql"); p.add_argument("--project",required=True,type=Path); p.add_argument("--sql",required=True); p.add_argument("--output",default="query_result.csv")
    p=sub.add_parser("run-pipeline"); p.add_argument("--project",required=True,type=Path); p.add_argument("--config",required=True)
    p=sub.add_parser("runs"); p.add_argument("--project",required=True,type=Path)
    a=ap.parse_args()
    if a.cmd=="run-python":
        rec=run_python(a.project,a.script,a.timeout); result=rec
        if rec["status"]!="succeeded": print(json.dumps(result,indent=2)); raise SystemExit(rec["exit_code"])
    elif a.cmd in {"load-csv","query-sql","run-pipeline"}:
        project=project_path(a.project); started=utc(); t=time.monotonic()
        if a.cmd=="load-csv": result=load_csv_sqlite(project,a.input,a.table); kind="csv_load"; command=f"load-csv {a.input} -> {a.table}"
        elif a.cmd=="query-sql": result=read_only_query(project,a.sql,a.output); kind="sqlite_readonly_query"; command=a.sql
        else: result=run_pipeline(project,a.config); kind="csv_pipeline"; command=a.config
        logdir=project/"outputs"/"execution_logs"; logdir.mkdir(parents=True,exist_ok=True)
        log=logdir/f"{kind}_{len(list(logdir.glob(kind+'_*.json')))+1:04d}.json"
        log.write_text(json.dumps(result,indent=2),encoding="utf-8")
        record_run(project,kind,command,"succeeded",started,time.monotonic()-t,[],[{"path":str(result.get("output",result.get("database","")))}],log,0)
    else: result=load_json(project_path(a.project)/"governance"/"execution_runs.json",[])
    print(json.dumps(result,indent=2))
if __name__=="__main__": main()
