#!/usr/bin/env python3
"""Conservative pre-publication scan for common secret/PHI patterns and unsafe artifacts."""
from __future__ import annotations
import argparse,json,re
from pathlib import Path

SECRET_PATTERNS=[
    ("private_key",re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("github_token",re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b")),
    ("aws_access_key",re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("generic_secret_assignment",re.compile(r"(?i)\b(api[_-]?key|password|secret|access[_-]?token)\s*[:=]\s*['\"][^'\"]{8,}['\"]")),
    ("email_address",re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
]
FORBIDDEN_SUFFIXES={".sqlite",".sqlite3",".db",".pyc",".pyo",".log",".pem",".key",".p12",".pfx"}
def scan(folder:Path)->dict:
    findings=[];files=0
    for p in folder.rglob("*"):
        if not p.is_file():continue
        rel=str(p.relative_to(folder))
        if p.suffix.lower() in FORBIDDEN_SUFFIXES:findings.append({"file":rel,"type":"forbidden_file_type"})
        if p.stat().st_size>10*1024*1024:findings.append({"file":rel,"type":"file_over_10mb"})
        if p.suffix.lower() in {".png",".jpg",".jpeg",".webp",".pdf",".zip"}:continue
        try: content=p.read_text(encoding="utf-8")
        except (UnicodeDecodeError,OSError):continue
        files+=1
        for kind,pattern in SECRET_PATTERNS:
            for m in pattern.finditer(content):
                findings.append({"file":rel,"type":kind,"line":content.count("\n",0,m.start())+1})
    return {"scanned_text_files":files,"finding_count":len(findings),"findings":findings,
            "caveat":"Heuristic only: can miss secrets/PHI and flag synthetic examples. Manual review remains mandatory."}
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--repo",type=Path,required=True);ap.add_argument("--out",type=Path,default=Path("publication_scan.json"));a=ap.parse_args()
    r=scan(a.repo.resolve());a.out.write_text(json.dumps(r,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"finding_count":r["finding_count"],"report":str(a.out)},indent=2))
    if r["finding_count"]:raise SystemExit(1)
if __name__=="__main__":main()
