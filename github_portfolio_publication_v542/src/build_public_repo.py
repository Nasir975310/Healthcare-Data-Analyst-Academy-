#!/usr/bin/env python3
"""Create a focused, publication-ready staging folder for the synthetic portfolio project."""
from __future__ import annotations
import argparse, hashlib, json, shutil
from pathlib import Path

INCLUDE_FILES=[
    "data/synthetic_outpatient_encounters.csv",
    "docs/data_dictionary.md",
    "docs/metric_contract.md",
    "docs/reference_results.md",
    "docs/reproduction_and_review.md",
    "sql/analysis.sql",
    "src/run_project.py",
    "scripts/repository_preflight.py",
    "tests/test_project.py",
    ".gitignore",
    "QA_REPORT.md",
]
INCLUDE_DIRS=["data","docs","sql","src","scripts","tests"]

def digest(p:Path)->str:
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()

def build(source:Path,destination:Path,case_study:Path|None=None)->dict:
    if not (source/"src/run_project.py").is_file(): raise ValueError("Source must be the v5.38 project directory")
    if destination.exists() and any(destination.iterdir()): raise ValueError("Destination must be empty; refusing to overwrite")
    destination.mkdir(parents=True,exist_ok=True)
    copied=[]
    for rel in INCLUDE_FILES:
        p=source/rel
        if p.is_file():
            target=destination/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
            copied.append(rel)
    if case_study and case_study.is_file():
        target=destination/"CASE_STUDY.md";shutil.copy2(case_study,target);copied.append("CASE_STUDY.md")
    readme = """# Synthetic Outpatient Operations Analytics

A reproducible Python/SQLite portfolio project using a small synthetic outpatient encounter dataset.

## Question
How can encounter-level records be validated and summarized into transparent outpatient volume and wait-time measures?

## Run
Python 3.10+ is recommended. No third-party Python packages are required.

```bash
python src/run_project.py
python -m unittest discover -s tests -v
python scripts/repository_preflight.py
```

The pipeline writes quality JSON, department summary CSV, SQLite database and a SHA-256 manifest under `outputs/`. Generated runtime files should not be committed.

## Reference results
See `CASE_STUDY.md` and `docs/reference_results.md`. The dataset is synthetic; results do not describe a real hospital.

## Data and metric rules
See `docs/data_dictionary.md` and `docs/metric_contract.md`. Encounter grain, deduplication policy, eligibility criteria, valid wait-time denominator and exclusions are documented.

## Limitations
This is an educational demonstration, not clinical decision support, a validated hospital performance study, or evidence of paid professional experience. It does not establish causal relationships or clinical outcomes.

## Privacy and provenance
The included fixture is synthetic. Do not add real patient data, personal information, credentials, tokens or confidential employer data.

## License
No license is assigned by this generated export. Choose and add a license only after confirming you have the right to license all included material.
"""
    (destination/"README.md").write_text(readme,encoding="utf-8")
    copied.append("README.md")
    workflow=destination/".github/workflows/python-tests.yml"
    workflow.parent.mkdir(parents=True,exist_ok=True)
    workflow.write_text("""name: Python tests
on:
  push:
  pull_request:
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: python -m unittest discover -s tests -v
      - run: python scripts/repository_preflight.py
""",encoding="utf-8")
    copied.append(".github/workflows/python-tests.yml")
    manifest={rel:digest(destination/rel) for rel in sorted(copied)}
    (destination/"SOURCE_MANIFEST.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    return {"files_copied":len(copied),"manifest_entries":len(manifest),"destination":str(destination),"files":sorted(copied)}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",type=Path,required=True)
    p.add_argument("--destination",type=Path,required=True)
    p.add_argument("--case-study",type=Path)
    a=p.parse_args()
    result=build(a.source.resolve(),a.destination.resolve(),a.case_study.resolve() if a.case_study else None)
    print(json.dumps(result,indent=2))
if __name__=="__main__":main()
