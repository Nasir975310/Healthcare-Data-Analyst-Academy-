#!/usr/bin/env python3
"""Validate local href/src references in root HTML entry points."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import sys
ROOT=Path(__file__).resolve().parents[1]
class Refs(HTMLParser):
    def __init__(self): super().__init__(); self.refs=[]
    def handle_starttag(self,tag,attrs):
        for k,v in attrs:
            if k in {'href','src'} and v: self.refs.append(v.strip())
checks=[]
for entry in [ROOT/'index.html',ROOT/'ROADMAP.html']:
    if not entry.exists(): continue
    parser=Refs(); parser.feed(entry.read_text(encoding='utf-8',errors='replace'))
    for ref in parser.refs:
        u=urlsplit(ref)
        if u.scheme or ref.startswith(('//','#','data:','mailto:','tel:','javascript:')): continue
        path=unquote(u.path)
        if not path: continue
        target=(entry.parent/path).resolve()
        try: target.relative_to(ROOT.resolve())
        except ValueError: checks.append((entry.name,ref,'outside_root')); continue
        if not target.exists(): checks.append((entry.name,ref,'missing'))
if checks:
    for row in checks: print('FAIL',*row)
    raise SystemExit(1)
print('PASS: local href/src references in root entry points resolve.')
