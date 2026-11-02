from pathlib import Path
import pandas as pd
BASE=Path(__file__).resolve().parents[1]; OUT=BASE/"outputs"; OUT.mkdir(exist_ok=True)
df=pd.read_csv(BASE/"data/pharmacovigilance_cases.csv")
checks=[
("missing_case_id",int(df.case_id.isna().sum()),"high"),
("duplicate_case_id",int(df.case_id.duplicated().sum()),"high"),
("event_after_receipt",int((df.event_onset_day>df.report_received_day).sum()),"high"),
("negative_age",int((df.patient_age_years<0).sum()),"high"),
("duplicate_candidate_flag",int(df.duplicate_candidate_flag.sum()),"review")
]
pd.DataFrame(checks,columns=["check","rows","severity"]).to_csv(OUT/"pv_quality_log.csv",index=False)
summary=df.groupby(["suspect_drug","serious_flag"],as_index=False).agg(case_records=("case_id","count"))
summary.to_csv(OUT/"pv_descriptive_counts.csv",index=False)
print({"case_records":len(df),"quality_checks":checks,"duplicate_candidates_require_manual_review":int(df.duplicate_candidate_flag.sum())})
print("No causality, signal, expectedness or confirmed-duplicate assessment is performed.")
