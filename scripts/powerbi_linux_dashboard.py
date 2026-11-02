from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assignments" / "data"

st.set_page_config(page_title="HDA Synthetic Hospital Dashboard", layout="wide")
st.title("Hospital Operations & Medication Utilisation")
st.caption("Synthetic training data · Not a clinical decision-support system")

enc = pd.read_csv(DATA / "pbi_dim_encounter.csv", parse_dates=["admission_date"])
metrics = pd.read_csv(DATA / "pbi_fact_encounter_metrics.csv", parse_dates=["discharge_date"])
orders = pd.read_csv(DATA / "pbi_fact_medication_orders.csv", parse_dates=["order_date"])
dept = pd.read_csv(DATA / "pbi_dim_department.csv")
payer = pd.read_csv(DATA / "pbi_dim_payer.csv")
drug = pd.read_csv(DATA / "pbi_dim_drug.csv")

enc = enc.merge(metrics, on="encounter_id", how="left", validate="one_to_one")
enc = enc.merge(dept, on="department_key", how="left", validate="many_to_one")
enc = enc.merge(payer, on="payer_key", how="left", validate="many_to_one")
orders = orders.merge(enc[["encounter_id","department","payer_type","admission_date"]], left_on="encounter_key", right_on="encounter_id", how="left", validate="many_to_one")
orders = orders.merge(drug[["drug_key","drug_name","therapeutic_class"]], on="drug_key", how="left", suffixes=("","_dim"), validate="many_to_one")
orders["therapeutic_class"] = orders["therapeutic_class_dim"].fillna(orders["therapeutic_class"])
orders["order_month"] = orders["order_date"].dt.to_period("M").astype(str)
enc["admission_month"] = enc["admission_date"].dt.to_period("M").astype(str)

with st.sidebar:
    st.header("Filters")
    departments = sorted(enc["department"].dropna().unique().tolist())
    selected_depts = st.multiselect("Department", departments, default=departments)
    payers = sorted(enc["payer_type"].dropna().unique().tolist())
    selected_payers = st.multiselect("Payer", payers, default=payers)
    months = sorted(enc["admission_month"].dropna().unique().tolist())
    selected_months = st.multiselect("Admission month", months, default=months)
    st.caption("Admission-month filter scopes encounter KPIs. Order page uses order date for its own trend.")

fenc = enc[enc["department"].isin(selected_depts) & enc["payer_type"].isin(selected_payers) & enc["admission_month"].isin(selected_months)]
enc_keys = set(fenc["encounter_id"])
ford = orders[orders["encounter_key"].isin(enc_keys)]

c1,c2,c3,c4 = st.columns(4)
c1.metric("Encounter count", f"{fenc['encounter_id'].nunique():,}")
c2.metric("Mean LOS (days)", f"{fenc['length_of_stay_days'].mean():.2f}" if fenc["length_of_stay_days"].notna().any() else "—")
flag_count = fenc["readmission_30d_flag"].sum(min_count=1)
flag_den = fenc["readmission_30d_flag"].notna().sum()
c3.metric("Supplied flag proportion", f"{flag_count/flag_den:.1%}" if flag_den else "—")
c4.metric("Medication order rows", f"{len(ford):,}")
st.caption("The supplied flag is not independently validated. Medication orders do not prove dispensing, administration or adherence.")

left,right=st.columns(2)
with left:
    bydept=fenc.groupby("department",dropna=False).agg(encounters=("encounter_id","nunique")).reset_index().sort_values("encounters",ascending=False)
    st.subheader("Encounters by department")
    st.plotly_chart(px.bar(bydept,x="department",y="encounters"),use_container_width=True)
with right:
    los=fenc.groupby("department",dropna=False).agg(mean_los=("length_of_stay_days","mean")).reset_index().sort_values("mean_los",ascending=False)
    st.subheader("Mean length of stay by department")
    st.plotly_chart(px.bar(los,x="department",y="mean_los"),use_container_width=True)

st.subheader("Admission-month encounter volume")
trend=fenc.groupby("admission_month",dropna=False).agg(encounters=("encounter_id","nunique")).reset_index().sort_values("admission_month")
st.plotly_chart(px.line(trend,x="admission_month",y="encounters",markers=True),use_container_width=True)

st.divider()
st.header("Medication utilisation")
o1,o2,o3=st.columns(3)
o1.metric("Order rows",f"{len(ford):,}")
o2.metric("Ordered quantity",f"{ford['quantity'].sum():,.0f}")
o3.metric("Synthetic order value",f"₹{ford['line_total_inr'].sum(skipna=True):,.2f}")
class_mix=ford.groupby("therapeutic_class",dropna=False).agg(order_rows=("order_id","count")).reset_index().sort_values("order_rows",ascending=False)
st.plotly_chart(px.bar(class_mix,x="order_rows",y="therapeutic_class",orientation="h"),use_container_width=True)
st.caption("Order quantity is not dispensing or administration. Costs are synthetic; missing-cost rows are excluded from the synthetic value sum.")

st.divider()
st.header("Data quality exceptions")
missing_cost=int(orders["unit_cost_inr"].isna().sum())
blank_class=int(orders["therapeutic_class"].fillna("").astype(str).str.strip().eq("").sum())
orphan=int((~orders["encounter_key"].isin(enc["encounter_id"])).sum())
q1,q2,q3=st.columns(3)
q1.metric("Missing unit cost rows",missing_cost)
q2.metric("Blank therapeutic class rows",blank_class)
q3.metric("Orphan encounter references",orphan)
exceptions=orders[orders["unit_cost_inr"].isna() | orders["therapeutic_class"].fillna("").astype(str).str.strip().eq("") | ~orders["encounter_key"].isin(enc["encounter_id"])]
st.dataframe(exceptions[["order_id","encounter_key","drug_name","therapeutic_class","unit_cost_inr","quantity"]],use_container_width=True,hide_index=True)
st.caption("This Streamlit/Plotly sample is a Linux-compatible learning alternative. It is not Power BI Desktop, DAX, Power Query or a PBIX file.")
