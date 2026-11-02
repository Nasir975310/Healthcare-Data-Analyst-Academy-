#!/usr/bin/env python3
"""Heuristic local portfolio hygiene scan; not a security certification."""
import argparse, json, re
from pathlib import Path

PATTERNS={
 "private_key":re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
 "api_token_assignment":re.compile(r'(?i)(api_key|access_token|secret).{0,10}[:=].{0,10}.{16,}'),
 "password_assignment":re.compile(r'(?i)password.{0,10}[:=].{0,10}.{8,}')
}
EXCLUDED_DIRS={".git",".venv","venv","__pycache__"}
EXCLUDED_SUFFIXES={".pyc",".sqlite",".db",".log"}
def scan(path):
    root=Path(path); findings=[]; scanned=0
    for f in root.rglob("*"):
        if not f.is_file() or any(part in EXCLUDED_DIRS for part in f.parts): continue
        if f.name == "repository_preflight.py": continue  # do not scan this scanner's own detection expressions
        if f.suffix.lower() in EXCLUDED_SUFFIXES or f.name==".env": 
            findings.append({"file":str(f.relative_to(root)),"type":"sensitive_or_generated_file","line":None})
            continue
        try:
            if f.stat().st_size>2_000_000: continue
            content=f.read_text(encoding="utf-8",errors="ignore")
        except OSError: continue
        scanned+=1
        for number,line in enumerate(content.splitlines(),1):
            for label,pattern in PATTERNS.items():
                if pattern.search(line):
                    findings.append({"file":str(f.relative_to(root)),"type":label,"line":number})
    return {"scanned_text_files":scanned,"finding_count":len(findings),"findings":findings,
            "caveat":"Heuristic scan only. It can miss secrets and produce false positives; inspect the full repository and use a dedicated secret scanner before publication."}
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--path",default=str(Path(__file__).resolve().parents[1]));a=p.parse_args()
    print(json.dumps(scan(a.path),indent=2))
