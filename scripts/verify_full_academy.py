#!/usr/bin/env python3
"""Run test directories independently and emit a machine-readable academy audit.

This is an inventory and execution report, not a claim that every module is
fully validated. Each test directory is isolated to avoid legacy import-name
collisions. Missing optional dependencies and manual-only modules are reported.
"""
from __future__ import annotations
import argparse, json, os, re, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {'.git', '.venv', 'venv', '__pycache__', 'node_modules'}

def discover_test_dirs():
    found = []
    for p in ROOT.rglob('tests'):
        if any(part in SKIP_PARTS for part in p.parts):
            continue
        if p.is_dir() and any(x.is_file() and (x.name.startswith('test_') or x.name.endswith('_test.py')) for x in p.iterdir()):
            found.append(p)
    return sorted(found)

def run_one(path: Path, timeout: int):
    rel = path.relative_to(ROOT).as_posix()
    start = time.monotonic()
    try:
        proc = subprocess.run(
            [sys.executable, '-m', 'pytest', '-q', '--disable-warnings', '--tb=short', '--import-mode=importlib', '-c', os.devnull, str(path)],
            cwd=path.parent, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            timeout=timeout, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}
        )
        output = proc.stdout[-6000:]
        if proc.returncode == 0:
            status = 'passed'
        elif re.search(r'No module named|ModuleNotFoundError|ImportError:', output):
            status = 'dependency_missing_or_import_error'
        else:
            status = 'failed'
        return {'module': rel.rsplit('/tests', 1)[0], 'test_directory': rel,
                'status': status, 'return_code': proc.returncode,
                'duration_seconds': round(time.monotonic()-start, 2), 'output_tail': output}
    except subprocess.TimeoutExpired as exc:
        return {'module': rel.rsplit('/tests', 1)[0], 'test_directory': rel,
                'status': 'timed_out', 'return_code': None,
                'duration_seconds': round(time.monotonic()-start, 2),
                'output_tail': (exc.stdout or b'').decode(errors='replace')[-6000:] if isinstance(exc.stdout, bytes) else str(exc.stdout or '')[-6000:]}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--timeout', type=int, default=60, help='seconds per test directory')
    ap.add_argument('--output', default='FULL_TEST_REPORT.json')
    ap.add_argument('--no-run', action='store_true', help='inventory test directories without executing')
    ap.add_argument('--jobs', type=int, default=6, help='parallel isolated test directories')
    args = ap.parse_args()
    dirs = discover_test_dirs()
    results = []
    if not args.no_run:
        with ThreadPoolExecutor(max_workers=max(1,args.jobs)) as pool:
            futures = [pool.submit(run_one, p, args.timeout) for p in dirs]
            results = [f.result() for f in as_completed(futures)]
        results.sort(key=lambda r: r['test_directory'])
    if args.no_run:
        results = [{'module': p.relative_to(ROOT).as_posix().rsplit('/tests',1)[0], 'test_directory': p.relative_to(ROOT).as_posix(), 'status':'not_run', 'return_code':None, 'duration_seconds':0, 'output_tail':''} for p in dirs]
    counts = {}
    for r in results: counts[r['status']] = counts.get(r['status'], 0) + 1
    report = {'schema_version':'1.0', 'generated_at_utc':datetime.now(timezone.utc).isoformat(),
              'root_test_scope':'six maintained career suites via pytest.ini; this report inventories and runs every discovered test directory independently',
              'test_directories_discovered':len(dirs), 'counts':counts, 'results':results,
              'interpretation':'A passing test directory does not certify its entire module. Dependency errors, timeouts, and failures remain visible. Modules without tests are not represented as tested.'}
    out = ROOT / args.output
    out.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'report':str(out.relative_to(ROOT)), 'discovered':len(dirs), 'counts':counts}, indent=2))
    return 1 if any(k in counts for k in ('failed','timed_out')) else 0
if __name__ == '__main__': raise SystemExit(main())
