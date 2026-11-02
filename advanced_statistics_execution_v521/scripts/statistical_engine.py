#!/usr/bin/env python3
"""Reproducible pandas-based statistical analysis engine for healthcare analytics."""
from __future__ import annotations
import argparse, hashlib, json, math, platform, sys, time, re
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf

def utc(): return datetime.now(timezone.utc).isoformat()
def sha(path):
 h=hashlib.sha256()
 with open(path,"rb") as f:
  for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
 return h.hexdigest()
def write_json(path,obj):
 Path(path).parent.mkdir(parents=True,exist_ok=True)
 Path(path).write_text(json.dumps(obj,indent=2,default=json_default),encoding="utf-8")
def json_default(x):
 if isinstance(x,(np.integer,)): return int(x)
 if isinstance(x,(np.floating,)): return float(x) if np.isfinite(x) else None
 if isinstance(x,(np.bool_,)): return bool(x)
 if isinstance(x,(pd.Timestamp,)): return x.isoformat()
 raise TypeError(f"Not JSON serializable: {type(x).__name__}")
def load_config(path):
 cfg=json.loads(Path(path).read_text(encoding="utf-8"))
 if not isinstance(cfg,dict): raise ValueError("Analysis configuration must be a JSON object")
 return cfg
def load_data(path):
 p=Path(path)
 if not p.is_file(): raise FileNotFoundError(p)
 if p.suffix.lower()==".csv": df=pd.read_csv(p)
 elif p.suffix.lower() in {".xlsx",".xls"}: df=pd.read_excel(p)
 elif p.suffix.lower()==".parquet": df=pd.read_parquet(p)
 else: raise ValueError("Supported input formats: CSV, XLSX/XLS, Parquet")
 if df.empty: raise ValueError("Input dataset has no records")
 if df.columns.duplicated().any(): raise ValueError("Duplicate column names are not supported")
 return df
def numeric_series(df,col):
 if col not in df: raise ValueError(f"Unknown column: {col}")
 x=pd.to_numeric(df[col],errors="coerce").dropna()
 if len(x)==0: raise ValueError(f"No numeric observations in {col}")
 return x.astype(float)
def profile(df):
 rows=[]
 for c in df.columns:
  s=df[c]; nmiss=int(s.isna().sum()); non=s.dropna()
  if pd.api.types.is_numeric_dtype(s):
   desc={"mean":float(non.mean()) if len(non) else None,"sd":float(non.std(ddof=1)) if len(non)>1 else None,
         "median":float(non.median()) if len(non) else None,"q1":float(non.quantile(.25)) if len(non) else None,
         "q3":float(non.quantile(.75)) if len(non) else None,"min":float(non.min()) if len(non) else None,"max":float(non.max()) if len(non) else None}
   typ="numeric"
  else:
   desc={"top_value":str(non.mode().iloc[0]) if len(non) and len(non.mode()) else None,
         "top_frequency":int(non.value_counts().iloc[0]) if len(non) else 0}
   typ="categorical_or_text"
  rows.append({"variable":str(c),"dtype":str(s.dtype),"inferred_type":typ,"n":len(s),"missing":nmiss,
               "missing_percent":round(nmiss*100/len(s),2),"unique_nonmissing":int(non.nunique()),**desc})
 return rows
def missing_report(df):
 out=[]
 for c in df.columns:
  n=int(df[c].isna().sum())
  out.append({"variable":str(c),"missing_n":n,"missing_percent":round(n*100/len(df),2),"complete_n":len(df)-n})
 return out
def outlier_report(df,columns):
 out=[]
 for c in columns:
  x=numeric_series(df,c); q1=float(x.quantile(.25)); q3=float(x.quantile(.75)); iqr=q3-q1
  lo=q1-1.5*iqr; hi=q3+1.5*iqr
  flagged=x[(x<lo)|(x>hi)]
  out.append({"variable":c,"method":"1.5xIQR exploratory flag","q1":q1,"q3":q3,"lower_fence":lo,"upper_fence":hi,
              "flagged_n":int(len(flagged)),"flagged_percent":round(len(flagged)*100/len(x),2),
              "flagged_index":[str(i) for i in flagged.index[:100]]})
 return out
def compare_groups(df,conf):
 col=conf["outcome"]; group=conf["group"]
 if col not in df or group not in df: raise ValueError("Unknown outcome or group column")
 data=df[[col,group]].copy(); data[col]=pd.to_numeric(data[col],errors="coerce"); data=data.dropna()
 groups=list(data[group].unique())
 if len(groups)!=2: raise ValueError("Independent two-group comparison requires exactly two observed groups")
 a=data.loc[data[group]==groups[0],col].astype(float).to_numpy()
 b=data.loc[data[group]==groups[1],col].astype(float).to_numpy()
 if len(a)<2 or len(b)<2: raise ValueError("Each group requires at least two observations")
 test=conf.get("test","welch")
 if test=="welch": res=stats.ttest_ind(a,b,equal_var=False)
 elif test=="mann_whitney": res=stats.mannwhitneyu(a,b,alternative=conf.get("alternative","two-sided"))
 else: raise ValueError("Supported tests: welch, mann_whitney")
 diff=float(np.mean(a)-np.mean(b))
 # Welch CI for mean difference
 se=math.sqrt(np.var(a,ddof=1)/len(a)+np.var(b,ddof=1)/len(b))
 dfree=(np.var(a,ddof=1)/len(a)+np.var(b,ddof=1)/len(b))**2/((np.var(a,ddof=1)/len(a))**2/(len(a)-1)+(np.var(b,ddof=1)/len(b))**2/(len(b)-1))
 crit=stats.t.ppf(.975,dfree)
 return {"outcome":col,"group":group,"groups":[str(groups[0]),str(groups[1])],"test":test,
  "n":[len(a),len(b)],"mean":[float(np.mean(a)),float(np.mean(b))],"sd":[float(np.std(a,ddof=1)),float(np.std(b,ddof=1))],
  "mean_difference_group1_minus_group2":diff,"welch_95ci":[diff-crit*se,diff+crit*se],
  "statistic":float(res.statistic),"p_value":float(res.pvalue),"interpretation":"P-value is not a measure of effect magnitude or clinical importance. Check design assumptions and multiplicity."}
def categorical_test(df,conf):
 row=conf["row"]; col=conf["column"]
 if row not in df or col not in df: raise ValueError("Unknown categorical variable")
 tab=pd.crosstab(df[row],df[col])
 if tab.shape[0]<2 or tab.shape[1]<2: raise ValueError("Contingency table must be at least 2x2")
 chi2,p,dof,expected=stats.chi2_contingency(tab,correction=False)
 return {"row":row,"column":col,"table":tab.to_dict(),"chi_square":float(chi2),"degrees_freedom":int(dof),
         "p_value":float(p),"expected_min":float(expected.min()),"expected_below_5_n":int((expected<5).sum()),
         "caution":"If expected cell counts are sparse, consider Fisher exact test for 2x2 or an appropriate exact/Monte Carlo method."}
def regression(df,conf):
 outcome=conf["outcome"]; predictors=conf["predictors"]; family=conf.get("family","linear")
 if not isinstance(predictors,list) or not predictors: raise ValueError("Regression requires a non-empty predictor list")
 for name in [outcome]+predictors:
  if not isinstance(name,str) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*",name):
   raise ValueError(f"Unsafe or unsupported formula variable name: {name}")
 needed=[outcome]+predictors
 if any(c not in df for c in needed): raise ValueError("Unknown regression variable")
 data=df[needed].dropna().copy()
 if len(data)<=len(predictors)+2: raise ValueError("Insufficient complete observations for requested model")
 formula=outcome+" ~ "+" + ".join(predictors)
 if family=="linear": model=smf.ols(formula,data=data).fit()
 elif family=="logistic":
  data[outcome]=pd.to_numeric(data[outcome],errors="raise")
  if set(data[outcome].unique())- {0,1}: raise ValueError("Logistic outcome must be coded 0/1")
  model=smf.logit(formula,data=data).fit(disp=False)
 else: raise ValueError("Supported regression families: linear, logistic")
 ci=model.conf_int()
 coeff=[]
 for name,val in model.params.items():
  coeff.append({"term":name,"coefficient":float(val),"standard_error":float(model.bse[name]),
                "p_value":float(model.pvalues[name]),"ci95_lower":float(ci.loc[name,0]),"ci95_upper":float(ci.loc[name,1]),
                "odds_ratio":float(np.exp(val)) if family=="logistic" else None})
 converged=bool(model.mle_retvals.get("converged",True)) if family=="logistic" else None
 warnings=["Complete-case analysis; missingness may bias estimates.","Associations are not causal effects.",
           "Check model specification, assumptions, influential observations and validation strategy."]
 if family=="logistic" and not converged: warnings.append("Logistic model did not converge; coefficients and intervals may be unreliable.")
 return {"family":family,"formula":formula,"n":int(model.nobs),"r_squared":float(model.rsquared) if family=="linear" else None,
         "pseudo_r_squared":float(model.prsquared) if family=="logistic" else None,"converged":converged,"coefficients":coeff,
         "warnings":warnings}
def run_analysis(input_path,config_path,outdir):
 start=time.monotonic(); cfg=load_config(config_path); df=load_data(input_path); out=Path(outdir); out.mkdir(parents=True,exist_ok=True)
 sections={"dataset":{"rows":len(df),"columns":len(df.columns),"column_names":list(map(str,df.columns)),
             "input_file":Path(input_path).name,"input_sha256":sha(input_path),"generated_utc":utc()},
          "descriptive":profile(df),"missingness":missing_report(df)}
 if cfg.get("outlier_columns"): sections["outliers"]=outlier_report(df,cfg["outlier_columns"])
 if cfg.get("group_comparison"): sections["group_comparison"]=compare_groups(df,cfg["group_comparison"])
 if cfg.get("categorical_test"): sections["categorical_test"]=categorical_test(df,cfg["categorical_test"])
 if cfg.get("regression"): sections["regression"]=regression(df,cfg["regression"])
 sections["runtime"]={"python":sys.version.split()[0],"platform":platform.platform(),"numpy":np.__version__,"pandas":pd.__version__,"scipy":__import__("scipy").__version__,"statsmodels":sm.__version__}
 sections["elapsed_seconds"]=round(time.monotonic()-start,3)
 write_json(out/"analysis_results.json",sections)
 pd.DataFrame(sections["descriptive"]).to_csv(out/"descriptive_profile.csv",index=False)
 pd.DataFrame(sections["missingness"]).to_csv(out/"missingness_report.csv",index=False)
 lines=["# Statistical analysis report","",f"**Dataset:** {Path(input_path).name}","",f"- Records: {len(df)}","- Variables: "+str(len(df.columns)),f"- Input SHA-256: `{sections['dataset']['input_sha256']}`","",
 "## Descriptive profile","| Variable | Type | Missing | Missing % | Unique |","|---|---|---:|---:|---:|"]
 for x in sections["descriptive"]: lines.append(f"| {x['variable']} | {x['inferred_type']} | {x['missing']} | {x['missing_percent']}% | {x['unique_nonmissing']} |")
 lines += ["","## Interpretation and limitations","These outputs are exploratory and require review against the prespecified analysis plan. P-values do not establish clinical importance or causality. Confirm variable definitions, sampling design, assumptions, missing-data mechanisms, multiplicity, and model diagnostics before reporting conclusions."]
 if "group_comparison" in sections:
  g=sections["group_comparison"]; lines += ["","## Group comparison",f"- Test: {g['test']}",f"- P-value: {g['p_value']:.5g}",f"- Mean difference (group 1 − group 2): {g['mean_difference_group1_minus_group2']:.4g}",f"- Welch 95% CI: {g['welch_95ci']}"]
 if "categorical_test" in sections:
  c=sections["categorical_test"]; lines += ["","## Categorical association",f"- Pearson chi-square p-value: {c['p_value']:.5g}",f"- Expected cells below 5: {c['expected_below_5_n']}"]
 if "regression" in sections:
  r=sections["regression"]; lines += ["","## Regression",f"- Model: `{r['formula']}`",f"- Complete observations: {r['n']}"]
  for c in r["coefficients"]: lines.append(f"- {c['term']}: {c['coefficient']:.4g} (95% CI {c['ci95_lower']:.4g} to {c['ci95_upper']:.4g}; p={c['p_value']:.4g})")
 (out/"statistical_report.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
 return sections
def main():
 ap=argparse.ArgumentParser(description=__doc__); ap.add_argument("--input",required=True); ap.add_argument("--config",required=True); ap.add_argument("--output",required=True)
 a=ap.parse_args(); result=run_analysis(a.input,a.config,a.output); print(json.dumps({"dataset":result["dataset"],"output":a.output,"sections":list(result)},indent=2))
if __name__=="__main__": main()
