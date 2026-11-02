#!/usr/bin/env python3
"""Build and validate a clean, reproducible portfolio release-candidate archive."""
from __future__ import annotations
import argparse, hashlib, json, os, shutil, subprocess, sys, tempfile, zipfile
from datetime import datetime, timezone
from pathlib import Path

FORBIDDEN_PARTS = {'.git', '__pycache__', '.venv', 'venv', '.pytest_cache', '.mypy_cache'}
FORBIDDEN_SUFFIXES = {'.pyc', '.pyo', '.sqlite', '.sqlite3', '.db', '.log', '.zip'}
SECRET_PATTERNS = [b'ghp_', b'github_pat_', b'AKIA', b'-----BEGIN PRIVATE KEY-----']

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024), b''): h.update(chunk)
    return h.hexdigest()

def manifest_check(project: Path) -> dict:
    mf=project/'SOURCE_MANIFEST.json'
    if not mf.is_file(): return {'ok':False,'errors':['SOURCE_MANIFEST.json missing'],'checked':0}
    try: expected=json.loads(mf.read_text(encoding='utf-8'))
    except Exception as e: return {'ok':False,'errors':[f'manifest invalid: {e}'],'checked':0}
    errors=[]; checked=0
    if not isinstance(expected,dict): return {'ok':False,'errors':['manifest must be a JSON object'],'checked':0}
    for rel,digest in expected.items():
        p=project/rel
        if not p.is_file(): errors.append(f'missing: {rel}'); continue
        checked+=1
        if sha256(p)!=digest: errors.append(f'hash mismatch: {rel}')
    return {'ok':not errors,'errors':errors,'checked':checked}

def scan(project: Path) -> list[str]:
    findings=[]
    for p in project.rglob('*'):
        if not p.is_file(): continue
        rel=p.relative_to(project)
        if rel.parts and rel.parts[0] == 'outputs': continue  # generated runtime artifacts are excluded from source scans and bundles
        if any(part in FORBIDDEN_PARTS for part in rel.parts): continue  # generated/local VCS artifacts are excluded
        if p.suffix.lower() in FORBIDDEN_SUFFIXES: findings.append(f'forbidden file type: {rel}')
        if p.is_symlink(): findings.append(f'symlink not allowed: {rel}'); continue
        try: data=p.read_bytes()
        except OSError: findings.append(f'unreadable file: {rel}'); continue
        if any(token in data for token in SECRET_PATTERNS): findings.append(f'possible credential marker: {rel}')
    return findings

def run(command:list[str], cwd:Path, log:Path) -> dict:
    proc=subprocess.run(command,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    log.write_text(proc.stdout,encoding='utf-8')
    return {'command':command,'exit_code':proc.returncode,'log_sha256':sha256(log),'log':proc.stdout}

def build(project:Path, out_zip:Path, report_path:Path) -> dict:
    project=project.resolve(); out_zip=out_zip.resolve(); report_path=report_path.resolve()
    if not project.is_dir(): raise ValueError(f'project directory not found: {project}')
    out_zip.parent.mkdir(parents=True,exist_ok=True); report_path.parent.mkdir(parents=True,exist_ok=True)
    m=manifest_check(project); findings=scan(project)
    results=[]
    with tempfile.TemporaryDirectory(prefix='hda_v544_') as td:
        work=Path(td)
        if m['ok'] and not findings:
            tests=run([sys.executable,'-m','unittest','discover','-s','tests','-v'],project,work/'tests.log'); results.append(tests)
            pipeline=run([sys.executable,'src/run_project.py'],project,work/'pipeline.log'); results.append(pipeline)
            # Runtime outputs are intentionally excluded; verify project source still matches its manifest.
            post=manifest_check(project)
            if not post['ok']: findings.extend(post['errors'])
        else:
            post=m
        eligible=m['ok'] and not findings and bool(results) and all(x['exit_code']==0 for x in results) and post['ok']
        report={'schema_version':'1.0','status':'LOCAL_CANDIDATE_READY' if eligible else 'BLOCKED','created_at_utc':datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z'),'project':project.name,'manifest':m,'post_run_manifest':post,'scan_findings':findings,'executions':[{'command':x['command'],'exit_code':x['exit_code'],'log_sha256':x['log_sha256']} for x in results],'scope':'Local release-candidate validation only. This does not prove remote publication, GitHub Actions execution, independent review, or employer acceptance.'}
        if eligible:
            temp_zip=out_zip.with_suffix(out_zip.suffix+'.tmp')
            with zipfile.ZipFile(temp_zip,'w',zipfile.ZIP_DEFLATED) as z:
                for p in sorted(project.rglob('*')):
                    if not p.is_file(): continue
                    rel=p.relative_to(project)
                    if (rel.parts and rel.parts[0] == 'outputs') or any(part in FORBIDDEN_PARTS for part in rel.parts) or p.suffix.lower() in FORBIDDEN_SUFFIXES: continue
                    z.write(p,Path(project.name)/rel)
            with zipfile.ZipFile(temp_zip) as z:
                bad=z.testzip()
                if bad: findings.append(f'ZIP CRC failure: {bad}'); eligible=False
            if eligible:
                os.replace(temp_zip,out_zip); report['archive']={'path':str(out_zip),'size_bytes':out_zip.stat().st_size,'sha256':sha256(out_zip)}
            else:
                temp_zip.unlink(missing_ok=True); report['status']='BLOCKED'; report['scan_findings']=findings
        report_path.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    return report

def main():
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('--project',type=Path,required=True); ap.add_argument('--out-zip',type=Path,required=True); ap.add_argument('--report',type=Path,required=True); a=ap.parse_args()
    report=build(a.project,a.out_zip,a.report); print(json.dumps({'status':report['status'],'manifest_files_checked':report['manifest']['checked'],'scan_findings':len(report['scan_findings']),'executions':[{'command':x['command'],'exit_code':x['exit_code']} for x in report['executions']],'archive':report.get('archive'),'report':str(a.report)},indent=2))
    if report['status']!='LOCAL_CANDIDATE_READY': raise SystemExit(2)
if __name__=='__main__': main()
