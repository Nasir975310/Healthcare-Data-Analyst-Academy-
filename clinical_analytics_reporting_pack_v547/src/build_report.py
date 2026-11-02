from pathlib import Path
import json, math
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
BASE=Path(__file__).resolve().parents[2]/"clinical_medication_utilization_case_study_v546"
OUT=Path(__file__).resolve().parents[1]/"outputs"
def main():
 raw=pd.read_csv(BASE/"data/synthetic_hypertension_records.csv")
 d=raw.drop_duplicates("record_id",keep="first")
 clean=d[d.primary_drug_class.notna() & d.baseline_sbp_mmhg.between(70,250)].copy()
 clean["fu_valid"]=clean.followup_sbp_mmhg.where(clean.followup_sbp_mmhg.between(70,250))
 p=clean.dropna(subset=["fu_valid"]).copy();p["change"]=p.baseline_sbp_mmhg-p.fu_valid
 groups=[]
 for cls,g in p.groupby("primary_drug_class",sort=True):
  x=g.change.astype(float).to_numpy();n=len(x);m=float(x.mean());sd=float(x.std(ddof=1));se=sd/math.sqrt(n);c=float(stats.t.ppf(.975,n-1))
  groups.append({"primary_drug_class":cls,"n":n,"mean_sbp_change":round(m,2),"sd_sbp_change":round(sd,2),"ci95_low":round(m-c*se,2),"ci95_high":round(m+c*se,2),"mean_baseline_sbp":round(float(g.baseline_sbp_mmhg.mean()),2),"mean_followup_sbp":round(float(g.fu_valid.mean()),2)})
 x=p.change.to_numpy();tt=stats.ttest_1samp(x,0);w=stats.wilcoxon(x);a=stats.f_oneway(*[g.change.to_numpy() for _,g in p.groupby("primary_drug_class")])
 q={"raw_rows":len(raw),"unique_ids":d.record_id.nunique(),"clean_rows":len(clean),"paired_sbp_rows":len(p),"missing_followup_sbp_in_clean":int(clean.followup_sbp_mmhg.isna().sum()),"implausible_followup_sbp_in_clean":int((clean.followup_sbp_mmhg.notna()&~clean.followup_sbp_mmhg.between(70,250)).sum())}
 result={"quality":q,"overall_paired_sbp_change":{"n":len(x),"mean_mmhg":round(float(x.mean()),2),"sd_mmhg":round(float(x.std(ddof=1)),2),"ci95_mmhg":[round(float(x.mean()-stats.t.ppf(.975,len(x)-1)*stats.sem(x)),2),round(float(x.mean()+stats.t.ppf(.975,len(x)-1)*stats.sem(x)),2)],"paired_t_statistic":float(tt.statistic),"paired_t_p_value":float(tt.pvalue),"wilcoxon_statistic":float(w.statistic),"wilcoxon_p_value":float(w.pvalue)},"by_primary_drug_class":groups,"exploratory_between_class_anova":{"f_statistic":float(a.statistic),"p_value":float(a.pvalue)}}
 OUT.mkdir(exist_ok=True);(OUT/"analysis_results.json").write_text(json.dumps(result,indent=2));pd.DataFrame(groups).to_csv(OUT/"class_level_summary.csv",index=False)
 plt.figure(figsize=(10,5.6));labels=[g["primary_drug_class"] for g in groups];means=[g["mean_sbp_change"] for g in groups];lo=[g["mean_sbp_change"]-g["ci95_low"] for g in groups];hi=[g["ci95_high"]-g["mean_sbp_change"] for g in groups];plt.bar(labels,means,yerr=[lo,hi],capsize=4);plt.ylabel("Mean paired SBP change (mmHg)");plt.title("Mean systolic BP change by primary drug class");plt.xticks(rotation=22,ha="right");plt.tight_layout();plt.savefig(OUT/"sbp_change_by_class.png",dpi=180);plt.close()
 plt.figure(figsize=(8,5));plt.hist(x,bins=18,edgecolor="black");plt.xlabel("Paired SBP change (mmHg; baseline − follow-up)");plt.ylabel("Number of records");plt.title("Distribution of paired systolic BP change");plt.tight_layout();plt.savefig(OUT/"sbp_change_distribution.png",dpi=180);plt.close()
if __name__=="__main__":main()
