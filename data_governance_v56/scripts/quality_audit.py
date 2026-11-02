#!/usr/bin/env python3
"""Rule-based CSV quality audit with issue register, lineage and hashes."""
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd

SEVERITY_WEIGHT={"critical":10,"high":5,"medium":2,"low":1}
def digest(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",required=True);ap.add_argument("--output-dir",default="quality_output")
    ap.add_argument("--rules",default=str(Path(__file__).resolve().parents[1]/"rules.json"))
    ap.add_argument("--project",default="Healthcare dataset quality audit")
    ap.add_argument("--owner",default="Not specified");ap.add_argument("--version",default="1.0")
    a=ap.parse_args();src=Path(a.input).resolve();out=Path(a.output_dir).resolve();out.mkdir(parents=True,exist_ok=True)
    df=pd.read_csv(src,dtype=str,keep_default_na=False);cfg=json.loads(Path(a.rules).read_text())
    issues=[];results=[]
    def add(rule,row_idx,value,message):
        issues.append({"rule_id":rule["id"],"rule":rule["name"],"severity":rule["severity"],
                       "row_number":int(row_idx+2) if row_idx is not None else None,
                       "field":rule["field"],"observed_value":str(value)[:200],"message":message})
    for rule in cfg["rules"]:
        field=rule["field"];typ=rule["type"];count=0
        if field not in df.columns:
            count=len(df)
            for i in range(len(df)): add(rule,i,"","Required field missing from dataset.")
        else:
            s=df[field].astype(str).str.strip()
            if typ=="not_blank":
                bad=s.eq("")
            elif typ=="unique":
                bad=s.eq("")|s.duplicated(keep="first")
            elif typ=="valid_date":
                bad=pd.to_datetime(s,errors="coerce").isna()
            elif typ=="numeric_min":
                n=pd.to_numeric(s,errors="coerce");bad=n.isna()|(n<float(rule["min"]))
            elif typ=="numeric_range":
                n=pd.to_numeric(s,errors="coerce");bad=n.isna()|(n<float(rule["min"]))|(n>float(rule["max"]))
            else: raise ValueError(f"Unsupported rule type: {typ}")
            count=int(bad.sum())
            for i in df.index[bad]: add(rule,int(i),s.iloc[i],rule["description"])
        results.append({"rule_id":rule["id"],"name":rule["name"],"field":field,
                        "severity":rule["severity"],"failed_rows":count,"passed_rows":len(df)-count,
                        "pass_rate_percent":round(100*(len(df)-count)/max(len(df),1),2)})
    profile=[]
    for c in df.columns:
        blank=int(df[c].astype(str).str.strip().eq("").sum())
        profile.append({"field":c,"dtype_inferred":str(pd.to_numeric(df[c],errors="coerce").dtype),
                        "missing_or_blank":blank,"missing_percent":round(100*blank/max(len(df),1),2),
                        "distinct_nonblank":int(df.loc[df[c].astype(str).str.strip().ne(""),c].nunique())})
    weighted=sum(x["failed_rows"]*SEVERITY_WEIGHT[x["severity"]] for x in results)
    max_weight=max(len(df)*sum(SEVERITY_WEIGHT[x["severity"]] for x in results),1)
    score=round(max(0,100*(1-weighted/max_weight)),2)
    issue_df=pd.DataFrame(issues,columns=["rule_id","rule","severity","row_number","field","observed_value","message"])
    issue_df.to_csv(out/"issue_register.csv",index=False)
    (out/"field_profile.json").write_text(json.dumps(profile,indent=2))
    (out/"rule_results.json").write_text(json.dumps(results,indent=2))
    (out/"quality_scorecard.json").write_text(json.dumps({"score_percent":score,"method":"100 × (1 − weighted failed rule-row count / maximum possible weighted count), floored at 0","severity_weights":SEVERITY_WEIGHT,"failed_rule_rows":sum(x["failed_rows"] for x in results),"rules":len(results)},indent=2))
    lineage={"project":a.project,"owner":a.owner,"dataset_version":a.version,"generated_utc":datetime.now(timezone.utc).isoformat(),
             "source_file":src.name,"source_sha256":digest(src),"row_count":len(df),"column_count":len(df.columns),
             "rules_file_sha256":digest(Path(a.rules).resolve()),"transformations":["Read CSV as strings; preserve blanks","Apply configured field-level validation rules","Generate field profile, rule results, issue register and scorecard"],
             "limitations":["Rule-based checks do not prove data accuracy or clinical validity.","Numeric plausibility thresholds require domain-owner approval.","Score is not a certification and should not be compared across different rule sets."]}
    (out/"lineage_record.json").write_text(json.dumps(lineage,indent=2))
    manifest={"source_sha256":digest(src),"rules_sha256":digest(Path(a.rules).resolve()),"outputs":{}}
    for p in sorted(out.iterdir()):
        if p.is_file() and p.name!="audit_manifest.json":manifest["outputs"][p.name]={"sha256":digest(p),"bytes":p.stat().st_size}
    (out/"audit_manifest.json").write_text(json.dumps(manifest,indent=2))
    print(json.dumps({"rows":len(df),"columns":len(df.columns),"issues":len(issues),"score_percent":score,"output_dir":str(out)},indent=2))
if __name__=="__main__":main()
