from pathlib import Path
import pandas as pd, json
BASE=Path(__file__).resolve().parents[1]
df=pd.read_csv(BASE/'data/dashboard_sample.csv',parse_dates=['admit_date'])
out=BASE/'output';out.mkdir(exist_ok=True)
summary={
 'rows':int(len(df)),
 'unique_patients':int(df.patient_id.nunique()),
 'departments':df.groupby('department').size().sort_values(ascending=False).to_dict(),
 'disposition':df.groupby('disposition').size().to_dict(),
 'mean_los_days':round(float(df.los_days.mean()),2),
 'sbp_completeness_pct':round(float(df.sbp.notna().mean()*100),2),
 'period_start':df.admit_date.min().date().isoformat(),
 'period_end':df.admit_date.max().date().isoformat(),
 'limitations':['Synthetic data','Encounter row grain assumed','SBP completeness is not BP control or care quality']
}
(out/'demo_summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
