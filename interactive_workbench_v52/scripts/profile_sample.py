from pathlib import Path
import pandas as pd, json, hashlib
BASE=Path(__file__).resolve().parents[1]
source=BASE/"data/workbench_sample.csv"
out=BASE/"output"; out.mkdir(exist_ok=True)
df=pd.read_csv(source)
profile=[]
for col in df.columns:
    s=df[col]
    numeric=pd.to_numeric(s,errors="coerce")
    row={"column":col,"dtype":str(s.dtype),"rows":len(s),"missing":int(s.isna().sum()),"missing_pct":round(float(s.isna().mean()*100),2),"distinct":int(s.nunique(dropna=True))}
    if numeric.notna().sum() and numeric.notna().sum()>=max(3,len(s)//2):
        row.update({"numeric_count":int(numeric.notna().sum()),"min":float(numeric.min()),"max":float(numeric.max()),"mean":round(float(numeric.mean()),3)})
    profile.append(row)
result={"source":"workbench_sample.csv","rows":len(df),"columns":len(df.columns),"duplicate_encounter_ids":int(df["encounter_id"].duplicated(keep=False).sum()),"profile":profile,
"limitations":["Synthetic training data","Type inference is heuristic","No clinical validity or causal assessment"]}
(out/"profile.json").write_text(json.dumps(result,indent=2))
(out/"profile.md").write_text("# CSV profile\n\n"+f"- Rows: {len(df)}\n- Columns: {len(df.columns)}\n- Duplicate encounter-ID rows: {result['duplicate_encounter_ids']}\n\n"+"\n".join(f"- **{x['column']}**: {x['missing']} missing ({x['missing_pct']}%), {x['distinct']} distinct" for x in profile))
print(json.dumps({k:result[k] for k in ["rows","columns","duplicate_encounter_ids"]},indent=2))
