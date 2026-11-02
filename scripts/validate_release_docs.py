#!/usr/bin/env python3
"""Reject duplicate changelog version headers and unresolved placeholder tokens."""
from pathlib import Path
import re, sys
root=Path(__file__).resolve().parents[1]
text=(root/'CHANGELOG.md').read_text(encoding='utf-8')
headers=re.findall(r'^##\s+(v\d+\.\d+\.\d+)\b',text,re.M)
seen=set(); dup=[]
for v in headers:
    if v in seen: dup.append(v)
    seen.add(v)
patterns=[r'\[INSERT[^\]]*\]',r'\bTBD\b',r'<\s*(?:insert|placeholder)[^>]*>',r'\[PLACEHOLDER\]']
problems=[]
for p in [root/'CHANGELOG.md', root/'RELEASE_NOTES_v5.60.3.md']:
    s=p.read_text(encoding='utf-8',errors='replace')
    for pat in patterns:
        for m in re.finditer(pat,s,re.I): problems.append(f'{p.relative_to(root)}:{s.count(chr(10),0,m.start())+1}: {m.group(0)}')
if dup: print('Duplicate changelog versions:',', '.join(sorted(set(dup))))
if problems: print('Placeholder markers:',*problems,sep='\n')
if dup or problems: raise SystemExit(1)
print(f'PASS: {len(headers)} unique changelog version headers; no unresolved markers in root release notes.')
