#!/usr/bin/env python3
"""Conservative text scan for likely secrets and direct identifiers; review findings manually."""
from pathlib import Path
import re, sys
root=Path(__file__).resolve().parents[1]
exclude={'.git','.venv','venv','node_modules','__pycache__'}
patterns={
 'private_key':re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
 'aws_access_key':re.compile(r'\bAKIA[0-9A-Z]{16}\b'),
 'generic_api_token':re.compile(r'(?i)(api[_-]?key|access[_-]?token|client[_-]?secret)\s*[:=]\s*[\"\'][A-Za-z0-9_\-]{20,}[\"\']'),
 'email_address':re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'),
}
allowed_ext={'.py','.md','.txt','.json','.yml','.yaml','.csv','.sql','.html','.js','.css','.sh','.toml','.ini'}
findings=[]
for p in root.rglob('*'):
 if not p.is_file() or p.suffix.lower() not in allowed_ext or any(x in exclude for x in p.parts): continue
 try: data=p.read_text(encoding='utf-8')
 except Exception: continue
 for name,pat in patterns.items():
  for m in pat.finditer(data):
   line=data.count('\n',0,m.start())+1
   source_line=data.splitlines()[line-1] if line <= len(data.splitlines()) else ''
   if 'fake' in source_line.lower() or 'SECRET_PATTERNS' in source_line or (p.name == 'scan_sensitive_patterns.py' and 'BEGIN PRIVATE KEY' in source_line): continue
   findings.append((p.relative_to(root).as_posix(),line,name,m.group(0)[:70]))
if findings:
 print('Potential sensitive-pattern matches (manual review required):')
 for f in findings: print(f'{f[0]}:{f[1]} [{f[2]}] {f[3]}')
 print('This heuristic scan can produce false positives and cannot certify absence of PHI/secrets.')
 raise SystemExit(1)
print('PASS: no configured sensitive-pattern matches. This heuristic scan is not a privacy certification.')
