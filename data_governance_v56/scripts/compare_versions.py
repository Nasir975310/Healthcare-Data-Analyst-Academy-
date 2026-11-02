#!/usr/bin/env python3
"""Compare two CSV snapshots by row count, columns, duplicate rows and field missingness."""
import argparse,json
from pathlib import Path
import pandas as pd

def profile(path):
    d=pd.read_csv(path,dtype=str,keep_default_na=False)
    return {"file":Path(path).name,"rows":len(d),"columns":list(d.columns),
            "duplicate_rows":int(d.duplicated().sum()),
            "missing":{c:int(d[c].astype(str).str.strip().eq("").sum()) for c in d.columns}}
def main():
    p=argparse.ArgumentParser();p.add_argument("--old",required=True);p.add_argument("--new",required=True);p.add_argument("--output",default="version_comparison.json");a=p.parse_args()
    old,new=profile(a.old),profile(a.new);fields=sorted(set(old["columns"])|set(new["columns"]))
    changes=[]
    for f in fields:
        changes.append({"field":f,"status":"added" if f not in old["columns"] else "removed" if f not in new["columns"] else "present",
                        "old_missing":old["missing"].get(f),"new_missing":new["missing"].get(f),
                        "missing_delta":(new["missing"].get(f,0)-old["missing"].get(f,0)) if f in old["columns"] and f in new["columns"] else None})
    result={"old":old,"new":new,"row_delta":new["rows"]-old["rows"],"duplicate_row_delta":new["duplicate_rows"]-old["duplicate_rows"],"field_changes":changes,
            "limitations":"Snapshot comparison is descriptive; it does not identify record-level changes or prove the reason for differences."}
    Path(a.output).write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=="__main__":main()
