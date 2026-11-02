#!/usr/bin/env python3
"""Adjusted-vs-crude statistical validation using synthetic observational data."""
import argparse,json
from pathlib import Path
import pandas as pd
import statsmodels.formula.api as smf
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--input",default="advanced_professional_mastery/data/observational_sbp_cohort.csv");ap.add_argument("--output",default="advanced_professional_mastery/outputs/statistical_validation.json");a=ap.parse_args()
 df=pd.read_csv(a.input)
 raw_n=len(df);missing=int(df.followup_sbp.isna().sum());implausible=int((df.age_years<18).sum())
 d=df[(df.age_years.between(18,110)) & df.followup_sbp.notna()].copy()
 crude=smf.ols("followup_sbp ~ treated",data=d).fit(cov_type="HC3")
 adjusted=smf.ols("followup_sbp ~ treated + baseline_sbp + age_years + diabetes",data=d).fit(cov_type="HC3")
 coef=float(adjusted.params["treated"]);ci=adjusted.conf_int().loc["treated"].tolist()
 out={"raw_n":raw_n,"missing_followup_sbp":missing,"implausible_age_rows":implausible,"complete_case_n":len(d),"treated_n":int(d.treated.sum()),"untreated_n":int((d.treated==0).sum()),"crude_mean_followup_treated":round(float(d.loc[d.treated==1,"followup_sbp"].mean()),2),"crude_mean_followup_untreated":round(float(d.loc[d.treated==0,"followup_sbp"].mean()),2),"crude_difference_treated_minus_untreated":round(float(crude.params["treated"]),2),"crude_robust_95ci":[round(float(x),2) for x in crude.conf_int().loc["treated"]],"adjusted_treatment_coefficient":round(coef,2),"adjusted_robust_95ci":[round(float(x),2) for x in ci],"adjusted_p_value":float(adjusted.pvalues["treated"]),"adjustment_covariates":["baseline_sbp","age_years","diabetes"],"r_squared":round(float(adjusted.rsquared),3),"interpretation":"Synthetic observational illustration only. Adjustment does not remove unmeasured confounding, selection bias, measurement error or model misspecification. The coefficient is not a causal treatment effect."}
 Path(a.output).parent.mkdir(parents=True,exist_ok=True);Path(a.output).write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
if __name__=="__main__":main()
