from pathlib import Path
import pandas as pd
BASE=Path(__file__).resolve().parents[1]
OUT=BASE/"output"
OUT.mkdir(exist_ok=True)
raw=pd.read_csv(BASE/"data/encounters_raw.csv",dtype={"encounter_id":"string","patient_id":"string"})
raw["admit_date"]=pd.to_datetime(raw["admit_date"],errors="coerce")
raw["discharge_date"]=pd.to_datetime(raw["discharge_date"],errors="coerce")
issues=pd.DataFrame(index=raw.index)
issues["duplicate_encounter_id"]=raw["encounter_id"].duplicated(keep=False)
issues["missing_encounter_id"]=raw["encounter_id"].isna() | raw["encounter_id"].str.strip().eq("")
issues["missing_patient_id"]=raw["patient_id"].isna() | raw["patient_id"].str.strip().eq("")
issues["missing_department"]=raw["department"].isna() | raw["department"].str.strip().eq("")
issues["invalid_dates"]=raw["admit_date"].isna() | raw["discharge_date"].isna() | (raw["discharge_date"]<raw["admit_date"])
issues["invalid_sbp"]=raw["sbp"].notna() & ((raw["sbp"]<60)|(raw["sbp"]>260))
issues["invalid_order_count"]=raw["order_count"].isna() | (raw["order_count"]<0)
reason_map={
"duplicate_encounter_id":"DUPLICATE_ENCOUNTER_ID","missing_encounter_id":"MISSING_ENCOUNTER_ID",
"missing_patient_id":"MISSING_PATIENT_ID","missing_department":"MISSING_DEPARTMENT",
"invalid_dates":"INVALID_DATES","invalid_sbp":"INVALID_SBP","invalid_order_count":"INVALID_ORDER_COUNT"}
reason=[]
for idx in raw.index:
    reason.append("|".join(code for col,code in reason_map.items() if bool(issues.loc[idx,col])))
raw["qa_reason_codes"]=reason
raw["qa_status"]=issues.any(axis=1).map({True:"QUARANTINE",False:"ACCEPT"})
raw.to_csv(OUT/"qa_audit_all_rows.csv",index=False)
accepted=raw[raw.qa_status=="ACCEPT"].copy()
quarantine=raw[raw.qa_status=="QUARANTINE"].copy()
accepted.to_csv(OUT/"encounters_accepted.csv",index=False)
quarantine.to_csv(OUT/"encounters_quarantine.csv",index=False)
assert len(raw)==len(accepted)+len(quarantine)
assert accepted.encounter_id.is_unique
accepted["los_days"]=(accepted.discharge_date-accepted.admit_date).dt.days
discharged=accepted[accepted.disposition=="Discharged"]
period_start=pd.Timestamp("2026-01-01")
period_end=pd.Timestamp("2026-03-02")
accepted=accepted[(accepted.admit_date>=period_start)&(accepted.admit_date<period_end)].copy()
accepted["los_days"]=(accepted.discharge_date-accepted.admit_date).dt.days
dept=accepted[accepted.department!="Emergency"].groupby("department",dropna=False).agg(encounters=("encounter_id","count"),unique_patients=("patient_id","nunique")).reset_index()
dept.to_csv(OUT/"department_summary_ex_emergency.csv",index=False)
disp=accepted.groupby("disposition").agg(encounters=("encounter_id","count")).reset_index()
disp["share_pct"]=(disp.encounters/len(accepted)*100).round(2)
disp.to_csv(OUT/"disposition_mix.csv",index=False)
discharged=accepted[accepted.disposition=="Discharged"]
los=float(discharged.los_days.mean()) if len(discharged) else None
sbp_complete=int(accepted.sbp.notna().sum())
summary={
"raw_rows":int(len(raw)),"accepted_rows":int((raw.qa_status=="ACCEPT").sum()),
"quarantined_rows":int((raw.qa_status=="QUARANTINE").sum()),
"reconciliation_pass":bool(len(raw)==len(accepted)+len(quarantine)),
"accepted_encounters_unique":bool(accepted.encounter_id.is_unique),
"reporting_period":"2026-01-01 through 2026-03-01 inclusive",
"accepted_reporting_period_rows":int(len(accepted)),
"department_comparison_excludes":"Emergency",
"discharged_encounters":int(len(discharged)),
"average_los_discharged_calendar_days":round(los,2) if los is not None else None,
"sbp_completeness_pct":round(sbp_complete/len(accepted)*100,2) if len(accepted) else None,
"issue_row_counts":{k:int(v.sum()) for k,v in issues.items()},
"limitations":["Synthetic training data only","Quarantine is rule-based and needs data-owner approval in production","SBP completeness is not BP control or clinical quality","LOS uses calendar-day difference","Department comparison excludes Emergency but overall hospital metrics retain it"]
}
(OUT/"engagement_summary.json").write_text(__import__("json").dumps(summary,indent=2))
(OUT/"qa_log.md").write_text("# QA log\n\n"+ "\n".join(f"- {k}: {v}" for k,v in summary.items()))
print(__import__("json").dumps(summary,indent=2))
