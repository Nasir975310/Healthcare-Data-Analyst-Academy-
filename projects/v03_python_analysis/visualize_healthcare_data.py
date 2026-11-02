"""Create reproducible charts from the synthetic encounter data."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "datasets" / "v03_python"
OUT = ROOT / "projects" / "v03_python_analysis" / "reports"
OUT.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA / "encounters.csv")
df["admission_date"] = pd.to_datetime(df["admission_date"], errors="coerce")
df["systolic_bp"] = pd.to_numeric(df["systolic_bp"], errors="coerce")
dept = pd.read_csv(DATA / "departments.csv")
df = df.merge(dept[["department_id","department_name"]], on="department_id", how="left", validate="many_to_one")

fig, ax = plt.subplots(figsize=(8,5))
df["systolic_bp"].dropna().plot.hist(ax=ax, bins=12, edgecolor="black")
ax.set(title="Distribution of recorded systolic blood pressure", xlabel="Systolic blood pressure (mmHg)", ylabel="Encounter count")
fig.tight_layout(); fig.savefig(OUT/"sbp_distribution.png", dpi=160); plt.close(fig)

summary = df.groupby("department_name").agg(mean_sbp=("systolic_bp","mean"), nonmissing_n=("systolic_bp","count")).sort_values("mean_sbp")
fig, ax = plt.subplots(figsize=(8,5))
ax.bar(summary.index.astype(str), summary["mean_sbp"])
ax.set(title="Mean recorded SBP by department", xlabel="Department", ylabel="Mean SBP (mmHg)")
ax.tick_params(axis="x", rotation=25)
for i,(value,n) in enumerate(zip(summary["mean_sbp"],summary["nonmissing_n"])):
    ax.text(i,value,f"n={n}",ha="center",va="bottom",fontsize=8)
fig.tight_layout(); fig.savefig(OUT/"mean_sbp_by_department.png", dpi=160); plt.close(fig)

monthly = df.set_index("admission_date").resample("MS").size()
fig, ax = plt.subplots(figsize=(8,5))
ax.plot(monthly.index, monthly.values, marker="o")
ax.set(title="Monthly encounter volume", xlabel="Admission month", ylabel="Encounter count")
fig.autofmt_xdate(); fig.tight_layout(); fig.savefig(OUT/"monthly_encounters.png", dpi=160); plt.close(fig)

missing = df.groupby("department_name").agg(total=("encounter_id","size"), missing_sbp=("systolic_bp",lambda x:x.isna().sum()))
missing["completeness_pct"] = 100*(missing["total"]-missing["missing_sbp"])/missing["total"]
fig, ax = plt.subplots(figsize=(8,5))
ax.bar(missing.index.astype(str), missing["completeness_pct"])
ax.set_ylim(0,100); ax.set(title="SBP recording completeness by department", xlabel="Department", ylabel="Completeness (%)")
ax.tick_params(axis="x", rotation=25)
fig.tight_layout(); fig.savefig(OUT/"sbp_completeness_by_department.png", dpi=160); plt.close(fig)
print("Saved four charts to", OUT)
