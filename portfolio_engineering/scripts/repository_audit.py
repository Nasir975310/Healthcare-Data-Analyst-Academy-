#!/usr/bin/env python3
"""Lightweight local portfolio repository audit; does not replace security scanning."""
from pathlib import Path
import re, json, sys
ROOT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path.cwd()
IGNORE={".git",".venv","venv","__pycache__",".pytest_cache","node_modules"}
PATTERNS={
 "possible_api_key":re.compile(r"(?i)(api[_-]?key|secret|access[_-]?token)\s*[:=]\s*['\"][A-Za-z0-9_\-]{12,}"),
 "possible_password":re.compile(r"(?i)(password|passwd)\s*[:=]\s*['\"][^'\"]{6,}"),
 "patient_identifier_label":re.compile(r"(?i)\b(patient_name|patient_full_name|mrn|medical_record_number|aadhaar|abha_id)\b")
}
findings=[]; files=0
for p in ROOT.rglob("*"):
    if not p.is_file() or any(part in IGNORE for part in p.parts): continue
    files+=1
    if p.suffix.lower() not in {".py",".sql",".md",".txt",".csv",".json",".yaml",".yml",".env",".html",".js"}: continue
    try: text=p.read_text(encoding="utf-8")
    except Exception: continue
    for n,line in enumerate(text.splitlines(),1):
        for label,pattern in PATTERNS.items():
            if pattern.search(line):
                findings.append({"file":str(p.relative_to(ROOT)),"line":n,"rule":label,"snippet":line[:160]})
result={"root":str(ROOT),"files_scanned":files,"findings":findings,"status":"REVIEW_REQUIRED" if findings else "NO_PATTERN_MATCHES"}
print(json.dumps(result,indent=2))
sys.exit(1 if findings else 0)
