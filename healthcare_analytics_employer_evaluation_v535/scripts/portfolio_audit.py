#!/usr/bin/env python3
"""Conservative portfolio hygiene scan; findings require human review."""
import pathlib, re, json, sys
ROOT=pathlib.Path(sys.argv[1]).resolve() if len(sys.argv)>1 else pathlib.Path.cwd()
SKIP={".git",".venv","venv","node_modules","__pycache__"}
PATTERNS={
 "private_key":re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
 "token_like":re.compile(r"(?i)(api[_-]?key|access[_-]?token|client[_-]?secret)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}"),
 "password_assignment":re.compile(r"(?i)password\s*[:=]\s*['\"][^'\"]{8,}['\"]")
}
findings=[]; scanned=0
for p in ROOT.rglob("*"):
    if not p.is_file() or any(part in SKIP for part in p.parts): continue
    if p.suffix.lower() not in {".py",".sql",".md",".txt",".json",".yml",".yaml",".csv",".html",".js",".env"}: continue
    try:
        if p.stat().st_size>2_000_000: continue
        content=p.read_text(encoding="utf-8",errors="ignore")
    except OSError: continue
    scanned+=1
    for label,pattern in PATTERNS.items():
        for m in pattern.finditer(content):
            line=content.count("\n",0,m.start())+1
            findings.append({"type":label,"file":str(p.relative_to(ROOT)),"line":line,
                "review":"Potential secret; inspect manually. Matched value is not emitted."})
result={"root":str(ROOT),"files_scanned":scanned,"potential_findings":len(findings),
        "findings":findings,"status":"REVIEW_REQUIRED" if findings else "NO_PATTERN_MATCH",
        "caveat":"Heuristic scan only; absence of matches does not prove safety. Use a dedicated secret scanner and human review."}
out=pathlib.Path.cwd()/"portfolio_audit.json"
out.write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
sys.exit(1 if findings else 0)
