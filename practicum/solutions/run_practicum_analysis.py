#!/usr/bin/env python3
"""Reference practicum analysis; synthetic training data only."""
from pathlib import Path
import pandas as pd, numpy as np, json, hashlib
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data"; OUT=ROOT/"outputs"; OUT.mkdir(exist_ok=True)
def read(name): return pd.read_csv(DATA/name)
def profile(df,name):
    return {"dataset":name,"rows":int(len(df)),"columns":list(df.columns),
            "missing_by_column":{k:int(v) for k,v in df.isna().sum().items()},
            "duplicate_full_rows":int(df.duplicated().sum())}
enc=read("encounters.csv"); orders=read("medication_orders.csv"); tickets=read("service_tickets.csv")
enc["admission_date"]=pd.to_datetime(enc["admission_date"],errors="coerce")
enc["discharge_date"]=pd.to_datetime(enc["discharge_date"],errors="coerce")
orders["order_date"]=pd.to_datetime(orders["order_date"],errors="coerce")
tickets["opened_at"]=pd.to_datetime(tickets["opened_at"],errors="coerce")
tickets["closed_at"]=pd.to_datetime(tickets["closed_at"],errors="coerce")
issues=[]
for name,df,key in [("encounters",enc,"encounter_id"),("orders",orders,"order_id"),("tickets",tickets,"ticket_id")]:
    for _,r in df[df[key].isna() | df[key].duplicated(keep=False)].iterrows():
        issues.append({"dataset":name,"record_key":str(r.get(key)),"issue":"missing_or_duplicate_primary_key"})
orphan=orders.loc[~orders.encounter_id.isin(enc.encounter_id)].copy()
for _,r in orphan.iterrows(): issues.append({"dataset":"orders","record_key":r.order_id,"issue":"orphan_encounter_reference"})
for _,r in orders[orders.unit_cost_inr.isna()].iterrows(): issues.append({"dataset":"orders","record_key":r.order_id,"issue":"missing_unit_cost"})
for _,r in enc[enc.baseline_sbp.isna()].iterrows(): issues.append({"dataset":"encounters","record_key":r.encounter_id,"issue":"missing_baseline_sbp"})
for _,r in tickets[tickets.closed_at.isna()].iterrows(): issues.append({"dataset":"tickets","record_key":r.ticket_id,"issue":"open_or_missing_close_timestamp"})
enc["month"]=enc.admission_date.dt.to_period("M").astype(str)
monthly=enc.groupby(["month","department"],dropna=False).agg(encounters=("encounter_id","count"),mean_los=("length_of_stay_days","mean"),median_los=("length_of_stay_days","median"),supplied_readmission_flags=("readmission_30d_flag","sum"),flag_rate=("readmission_30d_flag","mean")).reset_index()
order_counts=orders.groupby("encounter_id").size().rename("order_lines")
enc_orders=enc.set_index("encounter_id").join(order_counts).fillna({"order_lines":0}).reset_index()
department=enc_orders.groupby("department").agg(encounters=("encounter_id","count"),mean_los=("length_of_stay_days","mean"),median_los=("length_of_stay_days","median"),order_lines=("order_lines","sum"),order_lines_per_encounter=("order_lines","mean"),readmission_flag_rate=("readmission_30d_flag","mean")).reset_index()
# DUE subset: order rows with antihypertensive class; this is order-level pattern only.
htn=orders[orders.drug_class.eq("Antihypertensive")].copy()
htn_summary=htn.groupby("generic_name",dropna=False).agg(order_lines=("order_id","count"),quantity=("quantity","sum"),missing_unit_cost=("unit_cost_inr",lambda s:int(s.isna().sum()))).reset_index()
bp=enc.dropna(subset=["baseline_sbp","followup_sbp"]).copy()
bp["paired_sbp_change"]=bp.followup_sbp-bp.baseline_sbp
bp_summary={"eligible_pairs":int(len(bp)),"mean_change_mmhg":float(bp.paired_sbp_change.mean()) if len(bp) else None,
            "median_change_mmhg":float(bp.paired_sbp_change.median()) if len(bp) else None,
            "interpretation":"Descriptive paired change among complete records; not a treatment effect."}
tickets["resolution_clock_hours"]=(tickets.closed_at-tickets.opened_at).dt.total_seconds()/3600
closed=tickets[tickets.closed_at.notna()].copy()
ticket_summary=closed.groupby(["priority","client_type"]).resolution_clock_hours.agg(ticket_count="count",median_hours="median",p90_hours=lambda x:x.quantile(.9)).reset_index()
ticket_backlog=tickets[tickets.closed_at.isna()][["ticket_id","priority","client_type","status"]]
for name,df in [("encounters",enc),("orders",orders),("tickets",tickets)]:
    # no PHI; source files are synthetic and hashes are for reproducibility.
    pass
for filename,df in [("monthly_department_kpis.csv",monthly),("department_kpis.csv",department),("antihypertensive_order_patterns.csv",htn_summary),("ticket_resolution_kpis.csv",ticket_summary),("open_ticket_backlog.csv",ticket_backlog),("data_quality_issue_log.csv",pd.DataFrame(issues))]:
    df.to_csv(OUT/filename,index=False)
(OUT/"data_profile.json").write_text(json.dumps([profile(enc,"encounters"),profile(orders,"orders"),profile(tickets,"tickets")],indent=2,default=str))
(OUT/"paired_bp_summary.json").write_text(json.dumps(bp_summary,indent=2))
summary={"encounter_rows":len(enc),"order_rows":len(orders),"orphan_orders":len(orphan),"missing_order_cost":int(orders.unit_cost_inr.isna().sum()),"antihypertensive_order_lines":len(htn),"complete_paired_sbp":len(bp),"ticket_rows":len(tickets),"closed_tickets":len(closed),"open_or_missing_close":int(tickets.closed_at.isna().sum()),"mean_los_days":float(enc.length_of_stay_days.mean()),"supplied_readmission_flags":int(enc.readmission_30d_flag.sum()),"supplied_flag_rate":float(enc.readmission_30d_flag.mean())}
(OUT/"summary.json").write_text(json.dumps(summary,indent=2))
hashes={}
for p in sorted(DATA.glob("*.csv")): hashes[p.name]=hashlib.sha256(p.read_bytes()).hexdigest()
(OUT/"source_sha256.json").write_text(json.dumps(hashes,indent=2))
print(json.dumps(summary,indent=2))
