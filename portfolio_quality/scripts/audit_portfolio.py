#!/usr/bin/env python3
"""Evidence-oriented portfolio repository audit. Heuristic checks; not a security scanner."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path
from datetime import datetime, timezone

REQUIRED_README = {
 "project purpose": [r"##\s*(project overview|overview|purpose)"],
 "data and provenance": [r"##\s*(data|dataset|data sources|data provenance)"],
 "methods": [r"##\s*(methods|methodology|approach)"],
 "reproduction instructions": [r"##\s*(reproducibility|how to run|run|installation|setup)"],
 "results": [r"##\s*(results|findings|outputs)"],
 "quality checks": [r"##\s*(quality assurance|validation|data quality|testing)"],
 "limitations": [r"##\s*(limitations|caveats|interpretation)"],
}
DOC_FILES = ["README.md", "README.MD", "readme.md"]
TEST_HINTS = ["test", "tests", "qa", "quality", "validation"]
DICT_HINTS = ["data_dictionary", "data-dictionary", "dictionary", "schema", "data_dictionary.md"]
SECRET_PATTERNS = [
 (r"(?i)-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", "private-key marker"),
 (r"(?i)\b(?:api[_-]?key|secret|password|passwd|access[_-]?token)\s*[:=]\s*[A-Za-z0-9_./+=-]{12,}", "possible hard-coded credential"),
 (r"\bsk-[A-Za-z0-9_-]{20,}\b", "possible API token"),
]
def read_text(path: Path):
 try: return path.read_text(encoding="utf-8", errors="replace")
 except OSError: return ""
def audit(repo: Path):
 repo=repo.resolve()
 if not repo.is_dir(): raise ValueError(f"Not a directory: {repo}")
 files=[p for p in repo.rglob("*") if p.is_file() and not any(x in {".git","node_modules",".venv","venv","__pycache__"} for x in p.parts)]
 rel=[p.relative_to(repo).as_posix() for p in files]
 readme=next((repo/n for n in DOC_FILES if (repo/n).is_file()),None)
 readme_text=read_text(readme) if readme else ""
 checks=[]
 def add(name,passed,detail,weight=1): checks.append({"check":name,"passed":bool(passed),"detail":detail,"weight":weight})
 add("README exists",bool(readme),str(readme.relative_to(repo)) if readme else "Add a root README.md",2)
 for label,patterns in REQUIRED_README.items():
  ok=any(re.search(p,readme_text,re.I|re.M) for p in patterns)
  add(f"README: {label}",ok,"Section found" if ok else f"Add a clearly titled section for {label}",1)
 has_env=any(Path(x).name.lower() in {"requirements.txt","pyproject.toml","environment.yml","environment.yaml","renv.lock","package.json","dockerfile"} for x in rel)
 add("Environment/dependency declaration",has_env,"Dependency/environment file found" if has_env else "Add a pinned or documented environment file",2)
 has_data_dict=any(any(h in Path(x).name.lower() for h in DICT_HINTS) for x in rel)
 add("Data dictionary or schema",has_data_dict,"Dictionary/schema-like file found" if has_data_dict else "Add field definitions, units, grain and permitted values",2)
 has_test=any(any(h in Path(x).as_posix().lower() for h in TEST_HINTS) for x in rel)
 add("Test/QA artefact",has_test,"Test/QA path found" if has_test else "Add runnable tests or a documented QA script",2)
 has_license=any(Path(x).name.lower().startswith("license") for x in rel)
 add("Licence / sharing terms",has_license,"Licence file found" if has_license else "State sharing terms or explicitly state that no licence is granted",1)
 has_gitignore=".gitignore" in [Path(x).name for x in rel]
 add("Git ignore rules",has_gitignore,".gitignore found" if has_gitignore else "Add .gitignore for environments, outputs and secrets",1)
 synthetic=re.search(r"(?i)\b(synthetic|simulated|de-identified|public dataset)\b",readme_text)
 add("Data provenance/disclosure",bool(synthetic),"README contains a data provenance disclosure cue" if synthetic else "Explicitly state whether data are synthetic, public, authorised or otherwise sourced",2)
 code_files=[p for p in files if p.suffix.lower() in {".py",".sql",".r",".R",".ipynb",".m",".dax"}]
 add("Analytical artefact present",bool(code_files),f"{len(code_files)} analytical/code artefact(s) found" if code_files else "Add the actual query, script, notebook or model definition",2)
 # Search a small, bounded set of text-like files; skip binary and generated environments.
 secret_hits=[]
 for p in files:
  if p.suffix.lower() not in {".py",".sql",".r",".R",".md",".txt",".json",".yml",".yaml",".toml",".ini",".env",".csv",".ps1",".sh"}: continue
  if p.stat().st_size>2_000_000: continue
  content=read_text(p)
  for pattern,label in SECRET_PATTERNS:
   if re.search(pattern,content):
    secret_hits.append({"file":p.relative_to(repo).as_posix(),"finding":label})
 add("No obvious embedded secrets",not secret_hits,f"{len(secret_hits)} possible pattern hit(s); inspect manually" if secret_hits else "No configured high-signal secret patterns detected",3)
 # Exclude this audit's report and common generated files from PHI heuristic.
 phi_hits=[]
 for p in files:
  if p.suffix.lower() not in {".csv",".tsv",".json",".txt",".md"} or p.stat().st_size>2_000_000: continue
  name=p.name.lower()
  if any(x in name for x in ["synthetic","fixture","sample","example","readme","report"]): continue
  text=read_text(p)[:200000]
  patterns=[(r"\b\d{3}-\d{2}-\d{4}\b","SSN-shaped value"),(r"\b[A-Z]{2}\d{6,}\b","possible identifier pattern"),(r"(?i)\bpatient[_ -]?name\b","patient-name field label")]
  for pattern,label in patterns:
   if re.search(pattern,text): phi_hits.append({"file":p.relative_to(repo).as_posix(),"finding":label})
 add("No obvious PHI-shaped patterns",not phi_hits,f"{len(phi_hits)} possible pattern hit(s); manually inspect and do not assume PHI is absent" if phi_hits else "No configured PHI heuristics triggered; manual review still required",3)
 total=sum(x["weight"] for x in checks); earned=sum(x["weight"] for x in checks if x["passed"])
 score=round(100*earned/total) if total else 0
 return {"audit_version":"1.0","generated_at":datetime.now(timezone.utc).isoformat(),"repository":str(repo),"file_count":len(files),"code_file_count":len(code_files),"score":score,"weighted_points":{"earned":earned,"possible":total},"checks":checks,"secret_pattern_hits":secret_hits,"phi_heuristic_hits":phi_hits,"interpretation":"Heuristic triage only. A high score is not proof of correctness, privacy, security, regulatory compliance, clinical validity or reproducibility. Review every finding manually."}
def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument("repository",nargs="?",default=".",help="Repository directory")
 ap.add_argument("--output",default="portfolio_audit.json",help="JSON report path")
 ap.add_argument("--strict",action="store_true",help="Exit 2 if score < 85 or any secret/PHI heuristic triggers")
 args=ap.parse_args()
 try: result=audit(Path(args.repository))
 except Exception as exc: print(f"ERROR: {exc}",file=sys.stderr); return 1
 out=Path(args.output); out.write_text(json.dumps(result,indent=2),encoding="utf-8")
 print(f"Portfolio audit: {result['score']}/100")
 for c in result["checks"]: print(f"[{'PASS' if c['passed'] else 'REVIEW'}] {c['check']}: {c['detail']}")
 print(f"JSON report: {out}")
 if args.strict and (result["score"]<85 or result["secret_pattern_hits"] or result["phi_heuristic_hits"]): return 2
 return 0
if __name__=="__main__": raise SystemExit(main())
