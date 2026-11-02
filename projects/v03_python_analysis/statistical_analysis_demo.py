"""Descriptive and inferential demonstration on synthetic data only."""
from pathlib import Path
import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "datasets" / "v03_python"
OUT = ROOT / "projects" / "v03_python_analysis" / "reports"
OUT.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA / "encounters.csv")
df["systolic_bp"] = pd.to_numeric(df["systolic_bp"], errors="coerce")
df["length_of_stay_days"] = pd.to_numeric(df["length_of_stay_days"], errors="coerce")
df["encounter_type"] = df["encounter_type"].astype("category")

sbp = df["systolic_bp"].dropna()
print("SBP n:", len(sbp), "missing:", int(df["systolic_bp"].isna().sum()))
print("Mean:", round(sbp.mean(),2), "SD:", round(sbp.std(ddof=1),2))
print("Median:", round(sbp.median(),2), "IQR:", round(sbp.quantile(.75)-sbp.quantile(.25),2))

# Demonstration only: independent-group comparison of two encounter categories.
group_a = df.loc[df["encounter_type"]=="IPD","systolic_bp"].dropna()
group_b = df.loc[df["encounter_type"]=="OPD","systolic_bp"].dropna()
if len(group_a) >= 2 and len(group_b) >= 2:
    result = stats.ttest_ind(group_a, group_b, equal_var=False, nan_policy="omit")
    print("Welch t-test (IPD vs OPD):", result)
    print("Group n:", len(group_a), len(group_b))

# Exploratory OLS association, not causal inference.
model_df = df[["length_of_stay_days","systolic_bp","encounter_type"]].dropna()
if len(model_df) >= 10:
    model = smf.ols("length_of_stay_days ~ systolic_bp + C(encounter_type)", data=model_df).fit()
    print(model.summary())
    model_df.assign(fitted=model.fittedvalues, residual=model.resid).to_csv(OUT/"ols_diagnostics_data.csv",index=False)

print("WARNING: synthetic educational data; repeated patient encounters may violate independence.")
print("Do not interpret these p-values or coefficients as clinical evidence or causal effects.")
