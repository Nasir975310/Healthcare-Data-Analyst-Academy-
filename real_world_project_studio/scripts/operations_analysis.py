from pathlib import Path
import pandas as pd
BASE=Path(__file__).resolve().parents[1]; OUT=BASE/"outputs"; OUT.mkdir(exist_ok=True)
df=pd.read_csv(BASE/"data/operations_encounters.csv",parse_dates=["admission_date","discharge_date"])
issues=[]
for col in ["encounter_id","patient_id","department","admission_date","discharge_date","length_of_stay_days"]:
    n=int(df[col].isna().sum())
    if n: issues.append({"check":f"missing_{col}","rows":n,"severity":"high"})
dup=int(df["encounter_id"].duplicated().sum())
if dup: issues.append({"check":"duplicate_encounter_id","rows":dup,"severity":"high"})
bad=int((df["discharge_date"]<df["admission_date"]).sum())
if bad: issues.append({"check":"discharge_before_admission","rows":bad,"severity":"high"})
neg=int((df["length_of_stay_days"]<0).sum())
if neg: issues.append({"check":"negative_los","rows":neg,"severity":"high"})
valid=df.drop_duplicates("encounter_id").loc[lambda x:(x.discharge_date>=x.admission_date)&(x.length_of_stay_days>=0)]
dept=valid.groupby("department",as_index=False).agg(encounters=("encounter_id","nunique"),mean_los_days=("length_of_stay_days","mean"),supplied_flag_count=("readmission_flag","sum"))
dept["mean_los_days"]=dept["mean_los_days"].round(2)
dept.to_csv(OUT/"operations_department_kpis.csv",index=False)
pd.DataFrame(issues,columns=["check","rows","severity"]).to_csv(OUT/"operations_quality_log.csv",index=False)
summary={"source_rows":len(df),"valid_encounters":len(valid),"unique_patients":int(valid.patient_id.nunique()),"mean_los_days":round(float(valid.length_of_stay_days.mean()),2),"supplied_flag_rate_pct":round(float(valid.readmission_flag.mean()*100),2),"duplicate_encounter_ids":dup,"invalid_chronology":bad}
pd.Series(summary).to_json(OUT/"operations_summary.json",indent=2)
print(summary)
