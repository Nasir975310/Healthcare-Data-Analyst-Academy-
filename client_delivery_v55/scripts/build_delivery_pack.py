#!/usr/bin/env python3
"""Build a traceable client handoff folder and ZIP from a CSV and optional artifacts."""
from __future__ import annotations
import argparse, hashlib, json, shutil, zipfile
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd

def sha(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def copy_artifact(src, dest_dir, label, inventory):
    if not src: return
    p=Path(src).expanduser().resolve()
    if not p.is_file(): raise FileNotFoundError(f"{label} not found: {p}")
    dest=dest_dir/p.name
    if p != dest.resolve(): shutil.copy2(p,dest)
    inventory.append({"role":label,"file":dest.name,"bytes":dest.stat().st_size,"sha256":sha(dest)})

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--project",required=True); ap.add_argument("--input",required=True)
    ap.add_argument("--output-dir",default="delivery_output"); ap.add_argument("--report")
    ap.add_argument("--dashboard"); ap.add_argument("--data-dictionary")
    ap.add_argument("--metric-contract"); ap.add_argument("--owner",default="Not specified")
    ap.add_argument("--period",default="Not specified")
    a=ap.parse_args()
    src=Path(a.input).expanduser().resolve()
    if not src.is_file(): raise FileNotFoundError(src)
    df=pd.read_csv(src)
    out=Path(a.output_dir).expanduser().resolve()
    pack=out/"client_delivery_pack"
    if pack.exists(): shutil.rmtree(pack)
    pack.mkdir(parents=True)
    inventory=[]
    copy_artifact(src,pack,"source_dataset",inventory)
    copy_artifact(a.report,pack,"report",inventory)
    copy_artifact(a.dashboard,pack,"dashboard",inventory)
    copy_artifact(a.data_dictionary,pack,"data_dictionary",inventory)
    copy_artifact(a.metric_contract,pack,"metric_contract",inventory)
    fields=[]
    for c in df.columns:
        fields.append({"field":str(c),"dtype":str(df[c].dtype),"missing":int(df[c].isna().sum()),
                       "missing_percent":round(float(df[c].isna().mean()*100),2) if len(df) else 0})
    profile={"rows":int(len(df)),"columns":int(len(df.columns)),"duplicate_rows":int(df.duplicated().sum()),
             "fields":fields}
    (pack/"dataset_profile.json").write_text(json.dumps(profile,indent=2))
    inventory.append({"role":"generated_dataset_profile","file":"dataset_profile.json",
                      "bytes":(pack/"dataset_profile.json").stat().st_size,"sha256":sha(pack/"dataset_profile.json")})
    checklist=Path(__file__).resolve().parents[1]/"templates/CLIENT_HANDOFF_CHECKLIST.md"
    shutil.copy2(checklist,pack/checklist.name)
    inventory.append({"role":"handoff_checklist","file":checklist.name,"bytes":checklist.stat().st_size,"sha256":sha(checklist)})
    (pack/"HANDOFF_README.md").write_text(f"""# Client delivery: {a.project}

- Owner: {a.owner}
- Reporting period: {a.period}
- Generated (UTC): {datetime.now(timezone.utc).isoformat()}
- Source rows: {len(df)}
- Source columns: {len(df.columns)}
- Fully duplicated rows: {int(df.duplicated().sum())}

## Included artifacts
See `artifact_manifest.json` for filenames, roles, sizes and SHA-256 checksums.

## Interpretation and limitations
This package inventories supplied artifacts and profiles the CSV. It does not certify accuracy, completeness, privacy compliance, clinical validity or fitness for a particular decision. Confirm row grain, inclusion/exclusion criteria, metric denominators, source provenance and independent reconciliation. Descriptive statistics do not establish causality.

## Data governance
The package may contain sensitive data if the supplied source does. Review access permissions and disclosure risk before sharing. Never publish identifiable patient data or assume this packaging step de-identifies data.
""")
    inventory.append({"role":"handoff_readme","file":"HANDOFF_README.md","bytes":(pack/"HANDOFF_README.md").stat().st_size,"sha256":sha(pack/"HANDOFF_README.md")})
    manifest={"project":a.project,"owner":a.owner,"period":a.period,"generated_utc":datetime.now(timezone.utc).isoformat(),
              "source_dataset":{"file":src.name,"sha256":sha(src),"rows":len(df),"columns":len(df.columns)},
              "artifacts":inventory,"profile_file":"dataset_profile.json",
              "disclaimer":"Inventory and descriptive profile only; no certification, clinical validation or causal inference."}
    (pack/"artifact_manifest.json").write_text(json.dumps(manifest,indent=2))
    zip_path=out/"client_delivery_pack.zip"
    if zip_path.exists(): zip_path.unlink()
    with zipfile.ZipFile(zip_path,"w",zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(pack.rglob("*")):
            if p.is_file(): z.write(p,p.relative_to(out))
    with zipfile.ZipFile(zip_path) as z:
        bad=z.testzip()
        if bad: raise RuntimeError(f"ZIP integrity error: {bad}")
    print(json.dumps({"pack":str(pack),"zip":str(zip_path),"files":len(list(pack.glob("*"))),
                      "zip_sha256":sha(zip_path),"rows":len(df),"columns":len(df.columns)},indent=2))
if __name__=="__main__": main()
