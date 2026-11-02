#!/usr/bin/env python3
"""Statistical diagnostics, resampling and multiplicity correction for healthcare studies."""
from __future__ import annotations
import argparse, hashlib, json, math, platform
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.outliers_influence import variance_inflation_factor

VERSION="5.23.0"

def sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def finite(v):
    if v is None: return None
    try:
        x=float(v)
        return x if math.isfinite(x) else None
    except (TypeError,ValueError): return None

def load_data(path):
    p=Path(path)
    if p.suffix.lower()==".csv": df=pd.read_csv(p)
    elif p.suffix.lower() in {".xlsx",".xls"}: df=pd.read_excel(p)
    elif p.suffix.lower()==".parquet": df=pd.read_parquet(p)
    else: raise ValueError("Supported inputs: CSV, XLSX/XLS, Parquet")
    if df.empty: raise ValueError("Input dataset is empty")
    if df.columns.duplicated().any(): raise ValueError("Duplicate column names are not supported")
    return df

def bootstrap_mean_ci(x, reps=2000, confidence=.95, seed=2026):
    x=np.asarray(x,dtype=float); x=x[np.isfinite(x)]
    if len(x)<2: raise ValueError("Bootstrap mean CI requires at least two observations")
    if reps<200: raise ValueError("Use at least 200 bootstrap resamples")
    if not 0<confidence<1: raise ValueError("confidence must be between 0 and 1")
    rng=np.random.default_rng(seed)
    means=np.empty(reps)
    for i in range(reps): means[i]=rng.choice(x,size=len(x),replace=True).mean()
    alpha=1-confidence
    return {"n":len(x),"mean":float(x.mean()),"confidence":confidence,"method":"nonparametric percentile bootstrap",
            "replicates":reps,"seed":seed,"lower":float(np.quantile(means,alpha/2)),
            "upper":float(np.quantile(means,1-alpha/2))}

def normality_diagnostic(x):
    x=np.asarray(x,dtype=float); x=x[np.isfinite(x)]
    if len(x)<3: return {"test":"Shapiro-Wilk","n":len(x),"statistic":None,"p_value":None,"status":"not_run","reason":"At least 3 observations required"}
    # Shapiro-Wilk p-values are not reliable as a universal model-selection rule.
    sample=x if len(x)<=5000 else x[np.linspace(0,len(x)-1,5000,dtype=int)]
    r=stats.shapiro(sample)
    return {"test":"Shapiro-Wilk","n":len(x),"tested_n":len(sample),"statistic":finite(r.statistic),
            "p_value":finite(r.pvalue),"status":"completed",
            "interpretation":"Diagnostic only; combine with plots, design knowledge and robustness considerations."}

def group_diagnostics(df, outcome, group):
    if outcome not in df or group not in df: raise ValueError(f"Unknown columns: {outcome}, {group}")
    d=df[[outcome,group]].copy(); d[outcome]=pd.to_numeric(d[outcome],errors="coerce"); d=d.dropna()
    levels=list(d[group].unique())
    if len(levels)!=2: raise ValueError("Two-group diagnostics require exactly two observed groups")
    arrays=[d.loc[d[group]==v,outcome].to_numpy(dtype=float) for v in levels]
    if any(len(a)<2 for a in arrays): raise ValueError("Each group requires at least two observations")
    lev=stats.levene(*arrays,center="median")
    return {"outcome":outcome,"group":group,"levels":[str(x) for x in levels],
            "group_n":[len(x) for x in arrays],"normality":[normality_diagnostic(x) for x in arrays],
            "variance_homogeneity":{"test":"Levene median-centred","statistic":finite(lev.statistic),"p_value":finite(lev.pvalue),
             "interpretation":"A small p-value suggests unequal variances; Welch's test is generally preferable to pooled-variance t-test."},
            "recommended_comparison":"Welch independent-samples t-test if mean difference is the estimand; consider robust/nonparametric methods based on estimand and design."}

def regression_diagnostics(df, outcome, predictors, family="linear"):
    cols=[outcome]+predictors
    missing=[c for c in cols if c not in df]
    if missing: raise ValueError(f"Unknown regression columns: {missing}")
    d=df[cols].copy()
    for c in cols: d[c]=pd.to_numeric(d[c],errors="coerce")
    d=d.replace([np.inf,-np.inf],np.nan).dropna()
    if len(d)<=len(predictors)+2: raise ValueError("Insufficient complete cases for requested regression diagnostics")
    y=d[outcome].astype(float); X=sm.add_constant(d[predictors].astype(float),has_constant="add")
    if family=="linear":
        fit=sm.OLS(y,X).fit()
        robust=fit.get_robustcov_results(cov_type="HC3")
        resid=np.asarray(fit.resid); fitted=np.asarray(fit.fittedvalues)
        sh=normality_diagnostic(resid)
        bp=sm.stats.het_breuschpagan(resid,fit.model.exog)
        infl=fit.get_influence(); cooks=np.asarray(infl.cooks_distance[0])
        leverage=np.asarray(infl.hat_matrix_diag)
        threshold=4/len(d)
        # VIF excluding intercept; undefined in singular/constant designs.
        vif=[]
        for i,c in enumerate(predictors, start=1):
            try: v=variance_inflation_factor(X.to_numpy(),i)
            except Exception: v=float("nan")
            vif.append({"variable":c,"vif":finite(v)})
        return {"family":"linear_OLS","n_complete":len(d),"n_excluded":len(df)-len(d),
            "coefficients":[{"term":term,"estimate":finite(fit.params[term]),"conventional_se":finite(fit.bse[term]),
              "HC3_robust_se":finite(robust.bse[i]),"HC3_p_value":finite(robust.pvalues[i]),
              "HC3_ci_lower":finite(robust.conf_int()[i,0]),"HC3_ci_upper":finite(robust.conf_int()[i,1])}
              for i,term in enumerate(fit.params.index)],
            "residual_normality":sh,
            "heteroscedasticity":{"test":"Breusch-Pagan","LM_statistic":finite(bp[0]),"LM_p_value":finite(bp[1]),
                                  "F_statistic":finite(bp[2]),"F_p_value":finite(bp[3])},
            "influence":{"cooks_d_threshold_screen":threshold,"flagged_n":int((cooks>threshold).sum()),
                         "max_cooks_d":finite(np.max(cooks)),"max_leverage":finite(np.max(leverage)),
                         "note":"Screening thresholds are heuristics; inspect observations and verify data rather than deleting automatically."},
            "multicollinearity":{"vif":vif,"note":"VIF can be undefined or unstable with small samples, constants or collinearity."},
            "fit_summary":{"r_squared":finite(fit.rsquared),"adjusted_r_squared":finite(fit.rsquared_adj),
                           "condition_number":finite(fit.condition_number)}}
    if family=="logistic":
        if not set(y.unique()).issubset({0,1}) or len(y.unique())!=2:
            raise ValueError("Logistic outcome must contain both binary classes coded 0 and 1")
        fit=sm.Logit(y,X).fit(disp=False,maxiter=200)
        robust=fit.get_robustcov_results(cov_type="HC3") if hasattr(fit,"get_robustcov_results") else None
        probs=np.asarray(fit.predict(X))
        return {"family":"binary_logistic","n_complete":len(d),"n_excluded":len(df)-len(d),
          "converged":bool(fit.mle_retvals.get("converged",False)),
          "coefficients":[{"term":term,"estimate_log_odds":finite(fit.params[term]),
             "odds_ratio":finite(np.exp(fit.params[term])),"conventional_p_value":finite(fit.pvalues[term]),
             "ci_lower_log_odds":finite(fit.conf_int().loc[term,0]),"ci_upper_log_odds":finite(fit.conf_int().loc[term,1])}
             for term in fit.params.index],
          "apparent_classification":{"mean_predicted_probability":finite(probs.mean()),
            "note":"Descriptive in-sample predictions only; no discrimination or calibration validation."},
          "warnings":["Check sparse cells, separation, influential observations and event-per-parameter adequacy.",
                      "No Firth/penalized correction, bootstrap validation or external validation is implemented."]}
    raise ValueError("family must be linear or logistic")

def adjust_pvalues(items, method="holm"):
    if method not in {"holm","fdr_bh","bonferroni"}: raise ValueError("Supported corrections: holm, fdr_bh, bonferroni")
    vals=[float(x["p_value"]) for x in items]
    if any(not 0<=p<=1 for p in vals): raise ValueError("p-values must be between 0 and 1")
    if not vals: return []
    reject,adjusted,_,_=multipletests(vals,method=method)
    return [{**item,"adjusted_p_value":float(adjusted[i]),"reject_after_adjustment":bool(reject[i]),"correction":method}
            for i,item in enumerate(items)]

def run(input_path, config_path, output):
    cfg=json.loads(Path(config_path).read_text(encoding="utf-8"))
    df=load_data(input_path); out=Path(output); out.mkdir(parents=True,exist_ok=True)
    result={"version":VERSION,"generated_utc":datetime.now(timezone.utc).isoformat(),
            "input_sha256":sha256(input_path),"n_rows":len(df),"n_columns":len(df.columns),
            "assumption_diagnostics":[],"bootstrap":[],"regressions":[],"multiplicity":[],"warnings":[]}
    for spec in cfg.get("group_diagnostics",[]):
        result["assumption_diagnostics"].append(group_diagnostics(df,spec["outcome"],spec["group"]))
    for spec in cfg.get("bootstrap_means",[]):
        if spec["column"] not in df: raise ValueError(f"Unknown bootstrap column: {spec['column']}")
        x=pd.to_numeric(df[spec["column"]],errors="coerce").dropna()
        result["bootstrap"].append({"column":spec["column"],**bootstrap_mean_ci(x,spec.get("replicates",2000),
            spec.get("confidence",.95),spec.get("seed",2026))})
    for spec in cfg.get("regressions",[]):
        result["regressions"].append(regression_diagnostics(df,spec["outcome"],spec["predictors"],spec.get("family","linear")))
    for spec in cfg.get("multiplicity",[]):
        result["multiplicity"].append({"family":spec["name"],"results":adjust_pvalues(spec["tests"],spec.get("method","holm"))})
    if not any([result["assumption_diagnostics"],result["bootstrap"],result["regressions"],result["multiplicity"]]):
        raise ValueError("Configuration contains no analyses")
    if any(r.get("converged") is False for r in result["regressions"]): result["warnings"].append("At least one logistic model did not converge.")
    result["warnings"] += ["Diagnostics inform judgement; they do not automatically select or certify a statistical test.",
        "Bootstrap percentile intervals may perform poorly with very small, skewed or dependent samples.",
        "Complete-case regression can be biased when missingness is informative.",
        "Multiplicity correction applies only to the explicitly supplied test family; define families before inspecting results."]
    (out/"validation_results.json").write_text(json.dumps(result,indent=2,allow_nan=False),encoding="utf-8")
    (out/"validation_report.md").write_text(to_markdown(result),encoding="utf-8")
    manifest={"version":VERSION,"input_sha256":result["input_sha256"],"outputs":{
      "validation_results.json":sha256(out/"validation_results.json"),"validation_report.md":sha256(out/"validation_report.md")},
      "n_rows":len(df),"warnings":len(result["warnings"])}
    (out/"validation_manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
    return result

def to_markdown(r):
    lines=["# Statistical validation report","",f"- Dataset rows: {r['n_rows']}",f"- Dataset columns: {r['n_columns']}",
      f"- Input SHA-256: `{r['input_sha256']}`","", "## Group diagnostics"]
    if not r["assumption_diagnostics"]: lines.append("No group diagnostics configured.")
    for x in r["assumption_diagnostics"]:
        lines += [f"### {x['outcome']} by {x['group']}",f"- Groups: {x['levels']} (n={x['group_n']})",
          f"- Levene p-value: {x['variance_homogeneity']['p_value']}",
          f"- Recommendation: {x['recommended_comparison']}"]
        for n in x["normality"]: lines.append(f"- Shapiro-Wilk ({n['n']} observations): p={n['p_value']}")
    lines += ["","## Bootstrap intervals"]
    for x in r["bootstrap"]: lines.append(f"- {x['column']}: mean {x['mean']:.3f}; {x['confidence']:.0%} percentile CI [{x['lower']:.3f}, {x['upper']:.3f}] (B={x['replicates']}, seed={x['seed']})")
    lines += ["","## Regression diagnostics"]
    for x in r["regressions"]:
        lines.append(f"- {x['family']}: complete-case n={x['n_complete']}; excluded={x['n_excluded']}")
        if "residual_normality" in x: lines.append(f"  - Residual Shapiro-Wilk p={x['residual_normality']['p_value']}; Breusch-Pagan p={x['heteroscedasticity']['LM_p_value']}")
        if "converged" in x: lines.append(f"  - Converged: {x['converged']}")
    lines += ["","## Multiplicity correction"]
    for fam in r["multiplicity"]:
        lines.append(f"- {fam['family']} ({fam['results'][0]['correction'] if fam['results'] else 'no tests'}): "+", ".join(f"{x['name']} adjusted p={x['adjusted_p_value']:.4g}" for x in fam["results"]))
    lines += ["","## Warnings and interpretation limits"]
    lines += [f"- {x}" for x in r["warnings"]]
    return "\n".join(lines)+"\n"

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input",required=True); ap.add_argument("--config",required=True); ap.add_argument("--output",required=True)
    a=ap.parse_args(); r=run(a.input,a.config,a.output)
    print(json.dumps({"status":"success","rows":r["n_rows"],"diagnostic_groups":len(r["assumption_diagnostics"]),
      "bootstrap_intervals":len(r["bootstrap"]),"regressions":len(r["regressions"]),"multiplicity_families":len(r["multiplicity"])}))
if __name__=="__main__": main()
