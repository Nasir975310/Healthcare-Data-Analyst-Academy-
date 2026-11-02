#!/usr/bin/env python3
"""Reproducible statistical analysis for a two-group pre/post CSV study.

Requires: Python 3.10+, pandas, numpy, scipy.
This is an educational workflow, not a substitute for a prespecified SAP or
clinical/statistical review. Missingness and assumptions are reported explicitly.
"""
from __future__ import annotations
import argparse, json, math, hashlib
from pathlib import Path
from datetime import datetime, timezone
import numpy as np
import pandas as pd
from scipy import stats

def finite(x):
    return None if x is None or not np.isfinite(float(x)) else float(x)

def summarize(x):
    s=pd.to_numeric(pd.Series(x),errors="coerce").dropna().astype(float)
    if not len(s): return {"n":0,"missing":int(pd.Series(x).isna().sum())}
    return {"n":int(s.size),"missing":int(pd.Series(x).isna().sum()),
            "mean":finite(s.mean()),"sd":finite(s.std(ddof=1)) if len(s)>1 else None,
            "median":finite(s.median()),"q1":finite(s.quantile(.25)),
            "q3":finite(s.quantile(.75)),"min":finite(s.min()),"max":finite(s.max())}

def mean_ci(x, confidence=.95):
    s=pd.to_numeric(pd.Series(x),errors="coerce").dropna().astype(float)
    n=len(s)
    if n<2: return {"estimate":finite(s.mean()) if n else None,"lower":None,"upper":None,"n":n}
    se=stats.sem(s); q=stats.t.ppf((1+confidence)/2,n-1)
    return {"estimate":finite(s.mean()),"lower":finite(s.mean()-q*se),
            "upper":finite(s.mean()+q*se),"n":n}

def analyze(path:Path, outcome:str, group:str, reference:str, comparison:str,
            baseline:str|None, alpha:float=.05):
    df=pd.read_csv(path)
    required=[outcome,group]
    if baseline: required.append(baseline)
    missing_cols=[c for c in required if c not in df.columns]
    if missing_cols: raise ValueError(f"Missing required columns: {missing_cols}")
    df[group]=df[group].astype("string")
    raw=pd.to_numeric(df[outcome],errors="coerce")
    result={"metadata":{"input_file":path.name,"input_sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
        "rows":int(len(df)),"outcome":outcome,"group":group,"reference_group":reference,
        "comparison_group":comparison,"baseline":baseline,"alpha":alpha,
        "generated_utc":datetime.now(timezone.utc).isoformat()},
        "missingness":{},"overall":summarize(raw),"by_group":{},"tests":{},
        "effect_sizes":{},"categorical":{},"correlations":{},"regression":{},
        "interpretation_guardrails":[
          "P-values do not measure clinical importance or the probability that the null hypothesis is true.",
          "A non-significant result is not evidence of equivalence.",
          "Check design, confounding, missing-data mechanism, outliers and model assumptions.",
          "Do not infer causality from an observational group comparison.",
          "Synthetic example data are not clinical evidence or real hospital outcomes."]}
    for col in df.columns:
        result["missingness"][col]={"missing_n":int(df[col].isna().sum()),
            "missing_pct":finite(df[col].isna().mean()*100)}
    for g in [reference,comparison]:
        vals=raw[df[group]==g].dropna()
        result["by_group"][g]=summarize(vals)
    a=raw[df[group]==reference].dropna().to_numpy(dtype=float)
    b=raw[df[group]==comparison].dropna().to_numpy(dtype=float)
    if len(a)<2 or len(b)<2: raise ValueError("Each group needs at least two non-missing outcome values.")
    result["tests"]["welch_t"]={"statistic":finite(stats.ttest_ind(a,b,equal_var=False).statistic),
        "p_value":finite(stats.ttest_ind(a,b,equal_var=False).pvalue),
        "method":"Welch independent-samples t-test","note":"Compares group means; independent observations and adequate distributional behaviour are required."}
    mw=stats.mannwhitneyu(a,b,alternative="two-sided",method="auto")
    result["tests"]["mann_whitney"]={"statistic":finite(mw.statistic),"p_value":finite(mw.pvalue),
        "method":"Mann–Whitney U test","note":"Tests distributional/rank differences; not automatically a test of medians."}
    diff=float(np.mean(a)-np.mean(b))
    pooled=math.sqrt(((len(a)-1)*np.var(a,ddof=1)+(len(b)-1)*np.var(b,ddof=1))/(len(a)+len(b)-2))
    result["effect_sizes"]["mean_difference_reference_minus_comparison"]={"estimate":finite(diff),
        "ci_95":None,"unit":outcome,"direction":"positive means higher in reference group"}
    # Welch CI for the unstandardized mean difference
    va=np.var(a,ddof=1)/len(a); vb=np.var(b,ddof=1)/len(b); se=math.sqrt(va+vb)
    dof=(va+vb)**2/(va**2/(len(a)-1)+vb**2/(len(b)-1))
    q=stats.t.ppf(.975,dof)
    result["effect_sizes"]["mean_difference_reference_minus_comparison"]["ci_95"]=[finite(diff-q*se),finite(diff+q*se)]
    result["effect_sizes"]["cohens_d"]={"estimate":finite(diff/pooled) if pooled else None,
        "note":"Small-sample correction is not applied; interpret with context."}
    result["normality"]={}
    for name,vals in [(reference,a),(comparison,b)]:
        if 3<=len(vals)<=5000:
            sw=stats.shapiro(vals)
            result["normality"][name]={"test":"Shapiro–Wilk","statistic":finite(sw.statistic),"p_value":finite(sw.pvalue),
                "caution":"Low power in small samples; combine with plots and subject-matter review."}
        else: result["normality"][name]={"not_run":"Shapiro–Wilk used only for n=3 to 5000."}
    if baseline:
        base=pd.to_numeric(df[baseline],errors="coerce")
        change=raw-base
        result["change_from_baseline"]={"overall":summarize(change)}
        for g in [reference,comparison]:
            result["change_from_baseline"][g]=summarize(change[df[group]==g])
        ca=change[df[group]==reference].dropna().to_numpy(float)
        cb=change[df[group]==comparison].dropna().to_numpy(float)
        if len(ca)>=2 and len(cb)>=2:
            t=stats.ttest_ind(ca,cb,equal_var=False)
            result["tests"]["welch_change"]={"statistic":finite(t.statistic),"p_value":finite(t.pvalue),
                "method":"Welch test on change scores","note":"Change-score analysis is not universally optimal; consider baseline-adjusted ANCOVA when appropriate."}
        # paired baseline-follow-up test across complete cases
        paired=pd.DataFrame({"base":base,"followup":raw}).dropna()
        if len(paired)>=2:
            t=stats.ttest_rel(paired["followup"],paired["base"])
            result["tests"]["paired_t_overall"]={"statistic":finite(t.statistic),"p_value":finite(t.pvalue),
                "n_pairs":int(len(paired)),"method":"Paired t-test","note":"Assumes independent pairs and approximately normal within-person differences."}
    # Categorical variables: Pearson chi-square, with expected-count warning
    for col in df.select_dtypes(include=["object","string","category"]).columns:
        if col in [group] or df[col].nunique(dropna=True)>12: continue
        tab=pd.crosstab(df[group],df[col])
        if tab.shape[0]>=2 and tab.shape[1]>=2:
            chi=stats.chi2_contingency(tab,correction=False)
            result["categorical"][col]={"levels":tab.columns.astype(str).tolist(),
                "table":tab.to_dict(orient="index"),"chi_square":finite(chi.statistic),
                "degrees_freedom":int(chi.dof),"p_value":finite(chi.pvalue),
                "min_expected_count":finite(np.min(chi.expected_freq)),
                "warning":"Use Fisher's exact test or an appropriate exact/Monte Carlo method when expected counts are sparse." if np.min(chi.expected_freq)<5 else None}
    # Pearson/Spearman for numeric pairs; simple unadjusted association only
    numeric=df.select_dtypes(include=[np.number]).columns.tolist()
    for col in numeric:
        if col==outcome: continue
        pair=pd.DataFrame({"x":pd.to_numeric(df[col],errors="coerce"),"y":raw}).dropna()
        if len(pair)>=3 and pair["x"].nunique()>1 and pair["y"].nunique()>1:
            p=stats.pearsonr(pair.x,pair.y); s=stats.spearmanr(pair.x,pair.y)
            result["correlations"][col]={"n":int(len(pair)),"pearson_r":finite(p.statistic),"pearson_p":finite(p.pvalue),
                "spearman_rho":finite(s.statistic),"spearman_p":finite(s.pvalue),
                "warning":"Unadjusted association; correlation does not establish causation."}
    # Unadjusted OLS with one predictor for transparent teaching
    if baseline:
        pair=pd.DataFrame({"x":pd.to_numeric(df[baseline],errors="coerce"),"y":raw}).dropna()
        if len(pair)>=3 and pair.x.nunique()>1:
            lr=stats.linregress(pair.x,pair.y)
            result["regression"]["simple_ols"]={"outcome":outcome,"predictor":baseline,"n":int(len(pair)),
                "intercept":finite(lr.intercept),"slope":finite(lr.slope),"r_squared":finite(lr.rvalue**2),
                "slope_p_value":finite(lr.pvalue),"slope_ci_95":[finite(lr.slope-stats.t.ppf(.975,len(pair)-2)*lr.stderr),
                finite(lr.slope+stats.t.ppf(.975,len(pair)-2)*lr.stderr)],
                "warning":"Unadjusted descriptive model; assess linearity, residuals, influential points and confounding."}
    return result

def write_outputs(result,outdir):
    outdir.mkdir(parents=True,exist_ok=True)
    (outdir/"analysis_report.json").write_text(json.dumps(result,indent=2,allow_nan=False),encoding="utf-8")
    rows=[]
    for col,v in result["missingness"].items(): rows.append({"section":"missingness","variable":col,"details":json.dumps(v)})
    for g,v in result["by_group"].items(): rows.append({"section":"descriptive_by_group","variable":g,"details":json.dumps(v)})
    for k,v in result["tests"].items(): rows.append({"section":"test","variable":k,"details":json.dumps(v)})
    pd.DataFrame(rows).to_csv(outdir/"analysis_summary.csv",index=False)
    html=["<!doctype html><meta charset='utf-8'><title>Statistical analysis report</title>",
          "<style>body{font:16px system-ui;max-width:1000px;margin:2rem auto;padding:0 1rem;color:#182230}pre{white-space:pre-wrap;background:#f3f5f7;padding:1rem;border-radius:8px}h1{color:#174a70}</style>",
          "<h1>Statistical analysis report</h1><p>Generated from a CSV input. Review the methods, assumptions and guardrails before interpretation.</p>",
          "<h2>Metadata and provenance</h2><pre>"+json.dumps(result["metadata"],indent=2)+"</pre>",
          "<h2>Descriptive results</h2><pre>"+json.dumps({"overall":result["overall"],"by_group":result["by_group"],"change":result.get("change_from_baseline")},indent=2)+"</pre>",
          "<h2>Inferential results</h2><pre>"+json.dumps({"tests":result["tests"],"effect_sizes":result["effect_sizes"],"normality":result["normality"]},indent=2)+"</pre>",
          "<h2>Interpretation guardrails</h2><ul>"+"".join("<li>"+x+"</li>" for x in result["interpretation_guardrails"])+"</ul>"]
    (outdir/"analysis_report.html").write_text("".join(html),encoding="utf-8")

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input",type=Path,required=True); p.add_argument("--outdir",type=Path,default=Path("outputs"))
    p.add_argument("--outcome",default="followup_sbp"); p.add_argument("--group",default="group")
    p.add_argument("--reference",default="intervention"); p.add_argument("--comparison",default="usual_care")
    p.add_argument("--baseline",default="baseline_sbp"); p.add_argument("--alpha",type=float,default=.05)
    a=p.parse_args()
    if not 0<a.alpha<1: p.error("--alpha must be between 0 and 1")
    result=analyze(a.input,a.outcome,a.group,a.reference,a.comparison,a.baseline,a.alpha)
    write_outputs(result,a.outdir)
    print(json.dumps({"rows":result["metadata"]["rows"],"input_sha256":result["metadata"]["input_sha256"],
        "outputs":[str(a.outdir/x) for x in ["analysis_report.json","analysis_summary.csv","analysis_report.html"]]},indent=2))
if __name__=="__main__": main()
