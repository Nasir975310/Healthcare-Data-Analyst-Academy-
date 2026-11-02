#!/usr/bin/env python3
"""Reproducible portfolio capstone analysis on synthetic healthcare operations data."""
from pathlib import Path
import pandas as pd
BASE=Path(__file__).resolve().parents[1]
DATA=BASE/"data"; OUT=BASE/"outputs"; OUT.mkdir(exist_ok=True)
enc=pd.read_csv(DATA/"hospital_operations.csv",parse_dates=["admit_date","discharge_date"])
orders=pd.read_csv(DATA/"pharmacy_orders.csv",parse_dates=["order_date"])
tickets=pd.read_csv(DATA/"analytics_service_requests.csv",parse_dates=["received_date","completed_date"])
enc["los_days"]=(enc.discharge_date-enc.admit_date).dt.days
assert enc.encounter_id.is_unique and orders.order_id.is_unique and tickets.ticket_id.is_unique
assert (enc.los_days>=0).all()
orders["extended_cost_inr"]=orders.quantity*orders.unit_cost_inr
# Retain orphan orders for quality reporting; do not silently discard
orphan=orders.loc[~orders.encounter_id.isin(enc.encounter_id)].copy()
valid=orders.loc[orders.encounter_id.isin(enc.encounter_id)].copy()
ops=enc.groupby("department").agg(encounters=("encounter_id","nunique"),mean_los_days=("los_days","mean"),readmit_flag_count=("readmit_30d_flag","sum"),mean_charge_inr=("total_charge_inr","mean")).reset_index()
rx=valid.groupby("therapeutic_class").agg(order_lines=("order_id","nunique"),quantity=("quantity","sum"),extended_cost_inr=("extended_cost_inr","sum")).reset_index()
tickets["turnaround_days"]=(tickets.completed_date-tickets.received_date).dt.days
sla=tickets.groupby(["request_type","priority"]).agg(requests=("ticket_id","nunique"),mean_turnaround_days=("turnaround_days","mean"),rework_cases=("rework_flag","sum")).reset_index()
ops.to_csv(OUT/"department_operations.csv",index=False)
rx.to_csv(OUT/"pharmacy_utilisation.csv",index=False)
sla.to_csv(OUT/"service_delivery.csv",index=False)
quality={"encounters":len(enc),"unique_encounters":int(enc.encounter_id.nunique()),"order_lines":len(orders),"unique_orders":int(orders.order_id.nunique()),"orphan_order_lines":len(orphan),"tickets":len(tickets),"negative_los":int((enc.los_days<0).sum()),"negative_turnaround":int((tickets.turnaround_days<0).sum()),"missing_unit_cost":int(orders.unit_cost_inr.isna().sum())}
(OUT/"quality_summary.json").write_text(__import__("json").dumps(quality,indent=2))
orphan.to_csv(OUT/"orphan_orders_review.csv",index=False)
print("QUALITY",quality)
print("\\nDEPARTMENT METRICS\\n",ops.round(2).to_string(index=False))
print("\\nPHARMACY CLASS METRICS\\n",rx.round(2).to_string(index=False))
