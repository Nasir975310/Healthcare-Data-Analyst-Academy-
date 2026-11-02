from pathlib import Path
import pandas as pd
BASE=Path(__file__).resolve().parents[1]; OUT=BASE/"outputs"; OUT.mkdir(exist_ok=True)
df=pd.read_csv(BASE/"data/antihypertensive_due_cohort.csv")
required=["patient_id","age_years","baseline_sbp_mmhg","followup_sbp_mmhg","prescribed_any_antihypertensive"]
complete=df.dropna(subset=required).copy()
complete=complete.loc[complete.age_years.between(18,110)&complete.baseline_sbp_mmhg.between(60,260)&complete.followup_sbp_mmhg.between(60,260)]
complete["sbp_change_mmhg"]=complete.followup_sbp_mmhg-complete.baseline_sbp_mmhg
by_group=complete.groupby("prescribed_any_antihypertensive",as_index=False).agg(n=("patient_id","nunique"),baseline_mean_sbp=("baseline_sbp_mmhg","mean"),followup_mean_sbp=("followup_sbp_mmhg","mean"),mean_change_sbp=("sbp_change_mmhg","mean"))
by_group[["baseline_mean_sbp","followup_mean_sbp","mean_change_sbp"]]=by_group[["baseline_mean_sbp","followup_mean_sbp","mean_change_sbp"]].round(2)
by_group.to_csv(OUT/"due_group_summary.csv",index=False)
classes=complete.groupby("antihypertensive_class",as_index=False).agg(patients=("patient_id","nunique"))
classes.to_csv(OUT/"due_class_counts.csv",index=False)
print({"raw_n":len(df),"complete_plausible_n":len(complete),"paired_n":int(complete.sbp_change_mmhg.notna().sum()),"group_summary":by_group.to_dict("records")})
print("Interpretation: descriptive synthetic observational comparison only; confounding and treatment selection prevent causal claims.")
