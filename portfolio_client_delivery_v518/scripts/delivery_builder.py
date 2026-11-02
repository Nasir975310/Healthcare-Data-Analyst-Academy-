#!/usr/bin/env python3
"""Build a reproducible, client-ready healthcare analytics project handover package."""
from __future__ import annotations
import argparse, csv, hashlib, json, platform, re, shutil, sys, zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

SENSITIVE_NAME = re.compile(r"(patient.?name|full.?name|first.?name|last.?name|email|phone|mobile|address|mrn|medical.?record|aadhaar|ssn|dob|date.?of.?birth)", re.I)
def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024), b""): h.update(chunk)
    return h.hexdigest()

def read_csv(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader=csv.DictReader(f)
        rows=list(reader)
        return reader.fieldnames or [], rows

def build(source: Path, out: Path, title: str, audience: str, objective: str, owner: str):
    if not source.is_file(): raise FileNotFoundError(source)
    fields, rows=read_csv(source)
    if not fields: raise ValueError("Input CSV must contain a header row.")
    out.mkdir(parents=True, exist_ok=True)
    (out/"data").mkdir(exist_ok=True)
    (out/"docs").mkdir(exist_ok=True)
    (out/"reports").mkdir(exist_ok=True)
    shutil.copy2(source, out/"data"/source.name)
    missing=Counter()
    for row in rows:
        for k,v in row.items():
            if v is None or not str(v).strip(): missing[k]+=1
    dictionary=[]
    for f in fields:
        vals=[r.get(f,"") for r in rows if str(r.get(f,"")).strip()]
        dictionary.append({"field":f,"inferred_type":infer_type(vals),"non_missing":len(vals),
                           "missing":len(rows)-len(vals),"missing_percent":round((len(rows)-len(vals))*100/len(rows),2) if rows else 0,
                           "unique_values":len(set(vals))})
    sensitive=[f for f in fields if SENSITIVE_NAME.search(f)]
    manifest={
      "project_title":title,"generated_utc":datetime.now(timezone.utc).isoformat(),
      "owner_or_team":owner,"intended_audience":audience,"analysis_objective":objective,
      "input_file":source.name,"input_sha256":sha256(source),"row_count":len(rows),
      "column_count":len(fields),"columns":fields,"python_version":sys.version.split()[0],
      "platform":platform.platform(),"generator":"portfolio_client_delivery_v518/scripts/delivery_builder.py",
      "data_classification":"REVIEW_REQUIRED" if sensitive else "NOT_CLASSIFIED_BY_AUTOMATED_SCAN",
      "potentially_sensitive_column_names":sensitive,
      "limitations":["Automated name scan is not a privacy assessment.","No clinical validity, statistical correctness, or regulatory compliance is certified by packaging.","Synthetic data must be labelled as synthetic; real data requires approved governance."]
    }
    (out/"project_manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
    (out/"data_dictionary.json").write_text(json.dumps(dictionary,indent=2),encoding="utf-8")
    (out/"data_dictionary.csv").write_text(csv_text(["field","inferred_type","non_missing","missing","missing_percent","unique_values"],dictionary),encoding="utf-8")
    env={"python":sys.version.split()[0],"platform":platform.platform(),
         "python_packages":{"pandas":"record exact installed version before execution","numpy":"record exact installed version before execution","matplotlib":"record exact installed version before execution"},
         "reproducibility_note":"This manifest records runtime identity, not a fully resolved dependency lock. Generate a platform-specific lock with pip freeze or conda env export after validating the project environment."}
    (out/"environment_manifest.json").write_text(json.dumps(env,indent=2),encoding="utf-8")
    tech=f"""# Technical analysis report\n\n## Project\n{title}\n\n## Objective\n{objective}\n\n## Dataset profile\n- Rows: {len(rows)}\n- Columns: {len(fields)}\n- Source file: `{source.name}`\n- SHA-256: `{sha256(source)}`\n\n## Data quality profile\n| Field | Type (inferred) | Missing | Missing % | Unique |\n|---|---|---:|---:|---:|\n"""
    for d in dictionary: tech+=f"| {d['field']} | {d['inferred_type']} | {d['missing']} | {d['missing_percent']}% | {d['unique_values']} |\n"
    tech+="""\n## Methods and reproducibility\nThis delivery generator profiles CSV structure and missingness. It does not run inferential analysis, validate clinical definitions, or establish causality. Record analysis code, inclusion criteria, transformations, software versions, and reviewer sign-off in the project repository.\n\n## Privacy and governance\n"""
    tech+=("Potentially sensitive field names were detected: "+", ".join(sensitive)+". Do not distribute until privacy review, authorization, and de-identification are completed.\n" if sensitive else "No obvious sensitive field names were detected. This is not proof that the dataset is anonymous or safe to share; inspect free text, rare combinations, dates, and indirect identifiers.\n")
    (out/"reports"/"technical_report.md").write_text(tech,encoding="utf-8")
    executive=f"""# Executive summary\n\n**Project:** {title}  \n**Prepared for:** {audience}  \n**Project owner:** {owner}\n\n## Decision context\n{objective}\n\n## Dataset at a glance\n- {len(rows):,} records and {len(fields)} fields\n- Source fingerprint: `{sha256(source)[:16]}…`\n- Automated structural profiling completed\n\n## Findings and interpretation\nThis package contains a dataset profile, not a clinical outcome analysis. Populate this section only after analysis results have been independently checked. Distinguish observed associations from causal effects and include uncertainty, denominators, and time period.\n\n## Recommended next steps\n1. Confirm cohort, index date, eligibility, exclusions, and outcome definitions.\n2. Reconcile data lineage and missingness with the source system.\n3. Run the approved analysis plan and peer review all outputs.\n4. Obtain privacy, clinical, and client acceptance before external distribution.\n"""
    (out/"reports"/"executive_summary.md").write_text(executive,encoding="utf-8")
    case=f"""# Portfolio case study: {title}\n\n## Problem\n{objective}\n\n## Approach\nDescribe source systems, cohort construction, cleaning, analysis methods, validation, and stakeholder review. Never publish patient-level data or confidential client information.\n\n## Evidence to include\n- Dataset provenance and synthetic/real-data status\n- Data dictionary and quality checks\n- Reproducible SQL/Python/R code and environment lock\n- De-identified aggregate tables and visualizations\n- Limitations, reviewer feedback, and version history\n\n## Outcome\nInsert only verified project outcomes. Do not invent impact, savings, accuracy, or clinical benefit.\n\n## Skills demonstrated\nData profiling · documentation · reproducibility · healthcare data governance · client communication\n"""
    (out/"docs"/"portfolio_case_study.md").write_text(case,encoding="utf-8")
    acceptance={"project_scope_confirmed":False,"source_authorized":False,"data_classification_reviewed":False,
      "phi_and_identifiers_reviewed":False,"cohort_and_variable_definitions_approved":False,
      "transformations_reproducible":False,"analysis_code_versioned":False,"results_independently_reproduced":False,
      "denominators_and_missingness_checked":False,"charts_and_tables_labelled":False,
      "limitations_documented":False,"executive_report_reviewed":False,"technical_report_reviewed":False,
      "client_acceptance_recorded":False,"handover_access_and_retention_confirmed":False}
    (out/"qa_acceptance_checklist.json").write_text(json.dumps(acceptance,indent=2),encoding="utf-8")
    handover=f"""# Client handover\n\n## Contents\n- `project_manifest.json`: input fingerprint and project metadata\n- `data_dictionary.csv` / `.json`: field-level structural profile\n- `environment_manifest.json`: runtime information and lockfile guidance\n- `reports/executive_summary.md`: stakeholder-facing summary template\n- `reports/technical_report.md`: technical profile and caveats\n- `docs/portfolio_case_study.md`: safe portfolio narrative template\n- `qa_acceptance_checklist.json`: delivery gate\n- `data/`: copied source dataset\n\n## Handover controls\n1. Confirm recipient authorization and approved transfer channel.\n2. Review the dataset classification and remove prohibited identifiers.\n3. Supply exact analysis code and a resolved environment lock.\n4. Record report version, reviewer, acceptance date, and retention/deletion requirements.\n5. Retain only the minimum necessary data under the applicable agreement.\n\n**Important:** This generator does not certify privacy, clinical validity, regulatory compliance, or client acceptance.\n"""
    (out/"HANDOVER.md").write_text(handover,encoding="utf-8")
    (out/"README.md").write_text(f"# {title}\n\nClient-ready project scaffold generated by HDA Academy v5.18.0.\n\nStart with `HANDOVER.md`, review `project_manifest.json`, then complete `qa_acceptance_checklist.json`. Replace templates only with verified results.\n",encoding="utf-8")
    # Package every file except the output archive itself.
    archive=out.parent/(out.name+"_handover.zip")
    with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
        for p in sorted(out.rglob("*")):
            if p.is_file(): z.write(p,p.relative_to(out.parent))
    return {"output_dir":str(out),"archive":str(archive),"rows":len(rows),"columns":len(fields),"sensitive_name_flags":sensitive,"files":sum(p.is_file() for p in out.rglob("*"))}

def infer_type(vals):
    if not vals: return "empty"
    try:
        [int(v) for v in vals]; return "integer"
    except ValueError: pass
    try:
        [float(v) for v in vals]; return "numeric"
    except ValueError: pass
    low=[v.lower() for v in vals]
    if all(v in {"true","false","yes","no","0","1"} for v in low): return "boolean_like"
    return "string_or_date"

def csv_text(headers, rows):
    import io
    s=io.StringIO(); w=csv.DictWriter(s,fieldnames=headers); w.writeheader(); w.writerows(rows); return s.getvalue()

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input",required=True,type=Path); ap.add_argument("--output",required=True,type=Path)
    ap.add_argument("--title",default="Healthcare Analytics Project")
    ap.add_argument("--audience",default="Healthcare analytics stakeholder")
    ap.add_argument("--objective",default="Describe the analysis question and intended decision.")
    ap.add_argument("--owner",default="Project team")
    a=ap.parse_args()
    print(json.dumps(build(a.input,a.output,a.title,a.audience,a.objective,a.owner),indent=2))
if __name__=="__main__": main()
