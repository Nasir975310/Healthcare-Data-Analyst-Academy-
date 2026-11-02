#!/usr/bin/env python3
"""Employer-style healthcare data QA assessment using synthetic CSV extracts."""
from pathlib import Path
import argparse, json, sys
import pandas as pd
BASE=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser()
p.add_argument("--fail-on-orphans",action="store_true",help="Exit non-zero when orphan order references exist")
args=p.parse_args()
data=BASE/"data"; out=BASE/"outputs"; out.mkdir(exist_ok=True)
enc=pd.read_csv(data/"encounters.csv",dtype={"encounter_id":"string","patient_key":"string"})
ord=pd.read_csv(data/"medication_orders.csv",dtype={"order_id":"string","encounter_id":"string"})
enc["admit_date"]=pd.to_datetime(enc.admit_date,errors="coerce")
enc["discharge_date"]=pd.to_datetime(enc.discharge_date,errors="coerce")
ord["order_date"]=pd.to_datetime(ord.order_date,errors="coerce")
issues=[]
def add(df,mask,source,rule,severity,detail):
    for idx in df.index[mask.fillna(False)]:
        issues.append({"source":source,"row_number":int(idx)+2,"record_id":str(df.loc[idx].iloc[0]),"rule":rule,"severity":severity,"detail":detail})
add(enc,enc.encounter_id.duplicated(keep=False),"encounters","UNIQUE_ENCOUNTER_ID","critical","Duplicate encounter key")
add(ord,ord.order_id.duplicated(keep=False),"medication_orders","UNIQUE_ORDER_ID","critical","Duplicate order key")
add(enc,enc.discharge_date<enc.admit_date,"encounters","DATE_CHRONOLOGY","high","Discharge precedes admission")
add(enc,enc.department.isna(),"encounters","REQUIRED_DEPARTMENT","medium","Department missing")
add(ord,ord.quantity.le(0),"medication_orders","POSITIVE_QUANTITY","high","Quantity must be positive")
orphans=ord.loc[~ord.encounter_id.isin(enc.encounter_id)].copy()
for idx,row in orphans.iterrows():
    issues.append({"source":"medication_orders","row_number":int(idx)+2,"record_id":str(row.order_id),"rule":"VALID_ENCOUNTER_REFERENCE","severity":"high","detail":f"Orphan encounter reference {row.encounter_id}"})
enc["los_days"]=(enc.discharge_date-enc.admit_date).dt.days
department=enc.groupby("department",dropna=False).agg(encounters=("encounter_id","nunique"),mean_los_days=("los_days","mean"),supplied_readmission_flag_count=("readmission_30d","sum")).reset_index()
orders=ord.groupby("drug_class",dropna=False).agg(order_lines=("order_id","nunique"),quantity=("quantity","sum"),extended_cost=("quantity",lambda s:0)).reset_index()
# Calculate value separately without losing the grouping grain
value=ord.assign(extended_cost=ord.quantity*ord.unit_cost).groupby("drug_class",dropna=False).extended_cost.sum().reset_index()
orders=orders.drop(columns=["extended_cost"]).merge(value,on="drug_class",how="left")
pd.DataFrame(issues,columns=["source","row_number","record_id","rule","severity","detail"]).to_csv(out/"issue_log.csv",index=False)
department.to_csv(out/"department_summary.csv",index=False)
orders.to_csv(out/"drug_class_summary.csv",index=False)
orphan_value=float((orphans.quantity*orphans.unit_cost).sum())
summary={"encounter_rows":len(enc),"unique_encounter_ids":int(enc.encounter_id.nunique()),"order_rows":len(ord),"unique_order_ids":int(ord.order_id.nunique()),"orphan_order_rows":len(orphans),"orphan_order_value":round(orphan_value,2),"issue_count":len(issues),"critical_issue_count":sum(x["severity"]=="critical" for x in issues),"negative_los_count":int((enc.los_days<0).sum()),"invalid_date_count":int(enc.admit_date.isna().sum()+enc.discharge_date.isna().sum())}
(out/"qa_summary.json").write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
if summary["critical_issue_count"]>0 or (args.fail_on_orphans and summary["orphan_order_rows"]>0): sys.exit(2)
