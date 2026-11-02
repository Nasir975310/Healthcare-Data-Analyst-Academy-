#!/usr/bin/env python3
"""Clinical research methods: nonparametric, paired, repeated-measures, validated prediction, power and missing data."""
from __future__ import annotations
import argparse, hashlib, json, math
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.power import TTestIndPower
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, roc_curve, brier_score_loss
from sklearn.calibration import calibration_curve
import statsmodels.api as sm

VERSION="5.24.0"

def sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def numeric(df,col):
    if col not in df: raise ValueError(f"Unknown column: {col}")
    return pd.to_numeric(df[col],errors="coerce")

def bootstrap_ci(values, statistic=np.mean, reps=3000, confidence=.95, seed=524):
    x=np.asarray(values,dtype=float); x=x[np.isfinite(x)]
    if len(x)<2: raise ValueError("At least two finite observations are required")
    if reps<200: raise ValueError("At least 200 bootstrap replicates are required")
    rng=np.random.default_rng(seed)
    vals=np.array([statistic(rng.choice(x,size=len(x),replace=True)) for _ in range(reps)],dtype=float)
    a=(1-confidence)/2
    return {"estimate":float(statistic(x)),"lower":float(np.quantile(vals,a)),"upper":float(np.quantile(vals,1-a)),
            "confidence":confidence,"replicates":reps,"seed":seed,"method":"nonparametric percentile bootstrap"}

def cliffs_delta(a,b):
    a=np.asarray(a); b=np.asarray(b)
    # Pairwise comparison; chunking avoids allocating a huge matrix.
    greater=less=0
    for start in range(0,len(a),512):
        d=a[start:start+512,None]-b[None,:]
        greater+=int((d>0).sum()); less+=int((d<0).sum())
    return (greater-less)/(len(a)*len(b))

def independent_nonparametric(df,outcome,group,reps=3000,seed=524):
    y=numeric(df,outcome); g=df[group] if group in df else None
    if g is None: raise ValueError(f"Unknown group column: {group}")
    d=pd.DataFrame({"y":y,"g":g}).dropna(); levels=list(d.g.unique())
    if len(levels)!=2: raise ValueError("Exactly two observed groups are required")
    a=d.loc[d.g==levels[0],"y"].to_numpy(); b=d.loc[d.g==levels[1],"y"].to_numpy()
    if min(len(a),len(b))<2: raise ValueError("Each group requires at least two observations")
    u=stats.mannwhitneyu(a,b,alternative="two-sided",method="auto")
    delta=cliffs_delta(a,b)
    # Bootstrap independent groups separately, preserving group sizes.
    rng=np.random.default_rng(seed); boot=np.empty(reps)
    for i in range(reps):
        aa=rng.choice(a,len(a),replace=True); bb=rng.choice(b,len(b),replace=True)
        boot[i]=cliffs_delta(aa,bb)
    alpha=.05
    return {"outcome":outcome,"group":group,"levels":[str(levels[0]),str(levels[1])],"n":[len(a),len(b)],
      "mann_whitney_u":float(u.statistic),"p_value":float(u.pvalue),"cliffs_delta":float(delta),
      "cliffs_delta_ci":[float(np.quantile(boot,alpha/2)),float(np.quantile(boot,1-alpha/2))],
      "bootstrap":{"replicates":reps,"seed":seed,"method":"independent-group percentile bootstrap"},
      "interpretation":"Cliff's delta ranges from -1 to +1; positive values indicate values in group 1 tend to exceed group 2. Magnitude thresholds are context-dependent."}

def paired_analysis(df,before,after,reps=3000,seed=524):
    x=numeric(df,before); y=numeric(df,after); d=pd.DataFrame({"before":x,"after":y}).dropna()
    diff=(d.after-d.before).to_numpy()
    if len(diff)<2: raise ValueError("At least two complete pairs are required")
    test=stats.wilcoxon(diff,alternative="two-sided",zero_method="wilcox",method="auto")
    ci=bootstrap_ci(diff,np.mean,reps,.95,seed)
    return {"before":before,"after":after,"n_pairs":len(diff),"mean_change_after_minus_before":float(diff.mean()),
      "median_change":float(np.median(diff)),"wilcoxon_statistic":float(test.statistic),"p_value":float(test.pvalue),
      "mean_change_bootstrap_ci":ci,"note":"Wilcoxon signed-rank targets a rank-based paired location effect; the bootstrap interval is for the arithmetic mean change, a different estimand."}

def repeated_measures_friedman(df,subject,conditions):
    cols=[subject]+conditions
    if any(c not in df for c in cols): raise ValueError("Unknown subject or condition column")
    wide=df[cols].copy()
    for c in conditions: wide[c]=pd.to_numeric(wide[c],errors="coerce")
    wide=wide.dropna()
    if wide[subject].duplicated().any(): raise ValueError("Expected one row per subject with repeated measures in separate columns")
    if len(conditions)<3: raise ValueError("Friedman test requires at least three repeated conditions")
    if len(wide)<2: raise ValueError("At least two complete subjects are required")
    arrays=[wide[c].to_numpy() for c in conditions]
    test=stats.friedmanchisquare(*arrays)
    n=len(wide); k=len(conditions)
    kendall_w=float(test.statistic/(n*(k-1))) if n*(k-1)>0 else None
    return {"subject":subject,"conditions":conditions,"n_complete_subjects":n,"n_excluded":len(df)-n,
      "friedman_chi_square":float(test.statistic),"df":k-1,"p_value":float(test.pvalue),"kendall_w":kendall_w,
      "note":"Complete-case Friedman test; no post-hoc pairwise tests or multiplicity correction are automatically performed."}

def validated_roc(df,outcome,predictors,folds=5,repeats=1,seed=524):
    cols=[outcome]+predictors
    if any(c not in df for c in cols): raise ValueError("Unknown outcome or predictor column")
    d=df[cols].copy()
    y=pd.to_numeric(d.pop(outcome),errors="coerce")
    for c in predictors: d[c]=pd.to_numeric(d[c],errors="coerce")
    valid=y.notna(); d=d.loc[valid]; y=y.loc[valid].astype(int)
    d=d.replace([np.inf,-np.inf],np.nan)
    if set(y.unique())!={0,1}: raise ValueError("Outcome must contain both classes coded 0 and 1")
    min_class=int(y.value_counts().min())
    if folds<2 or folds>min_class: raise ValueError(f"folds must be 2..{min_class} (smallest class count)")
    if repeats<1: raise ValueError("repeats must be >=1")
    aucs=[]; all_predictions=[]; all_labels=[]
    for r in range(repeats):
        cv=StratifiedKFold(n_splits=folds,shuffle=True,random_state=seed+r)
        model=make_pipeline(SimpleImputer(strategy="median",add_indicator=True),StandardScaler(),LogisticRegression(max_iter=2000))
        probs=cross_val_predict(model,d,y,cv=cv,method="predict_proba")[:,1]
        aucs.append(float(roc_auc_score(y,probs)))
        all_predictions.extend(probs.tolist()); all_labels.extend(y.tolist())
    # Out-of-fold probabilities are averaged across repeated CV runs per subject.
    pred=np.asarray(all_predictions).reshape(repeats,len(y)).mean(axis=0)
    auc=float(roc_auc_score(y,pred))
    fpr,tpr,_=roc_curve(y,pred)
    brier=float(brier_score_loss(y,pred))
    # Calibration slope/intercept on out-of-fold predictions; clip to avoid infinite logits.
    clipped=np.clip(pred,1e-6,1-1e-6)
    logits=np.log(clipped/(1-clipped))
    cal=sm.Logit(y.to_numpy(),sm.add_constant(logits)).fit(disp=False)
    return {"outcome":outcome,"predictors":predictors,"n":len(y),"class_counts":{str(k):int(v) for k,v in y.value_counts().items()},
      "folds":folds,"repeats":repeats,"seed":seed,"cv_auc_by_repeat":aucs,"pooled_oof_auc":auc,
      "brier_score_oof":brier,"calibration_intercept_oof":float(np.asarray(cal.params)[0]),
      "calibration_slope_oof":float(np.asarray(cal.params)[1]),
      "roc_points":[{"fpr":float(x),"tpr":float(z)} for x,z in zip(fpr,tpr)],
      "warnings":["Small datasets produce unstable cross-validation estimates.",
       "The reported pooled out-of-fold AUC uses predictions from repeated stratified CV; fold-level uncertainty is not a confidence interval.",
       "No nested CV or external validation; any feature selection or hyperparameter tuning must occur inside each training fold.",
       "Calibration slope/intercept are estimated on out-of-fold predictions from this dataset and are not external calibration validation."]}

def power_two_sample_mean(effect_size,alpha=.05,power=.8,ratio=1.0):
    if effect_size<=0 or not 0<alpha<1 or not 0<power<1 or ratio<=0: raise ValueError("effect_size, alpha, power and ratio are outside valid ranges")
    n1=TTestIndPower().solve_power(effect_size=effect_size,alpha=alpha,power=power,ratio=ratio,alternative="two-sided")
    return {"standardized_mean_difference":effect_size,"alpha":alpha,"power":power,"allocation_ratio_n2_over_n1":ratio,
      "n_group_1":math.ceil(n1),"n_group_2":math.ceil(n1*ratio),"total_n":math.ceil(n1)+math.ceil(n1*ratio),
      "method":"two independent groups, two-sided t-test, normal-theory approximation via statsmodels",
      "warning":"Planning estimate only; inflate for attrition, clustering, unequal variances, multiplicity and design-specific requirements."}

def missingness_assessment(df,columns):
    selected=columns or list(df.columns)
    out=[]
    for c in selected:
        if c not in df: raise ValueError(f"Unknown missingness column: {c}")
        mask=df[c].isna()
        out.append({"variable":c,"missing_n":int(mask.sum()),"missing_percent":float(mask.mean()*100),
          "complete_n":int((~mask).sum()),"missingness_indicator_varies":bool(mask.any() and (~mask).any())})
    patterns=df[selected].isna().astype(int).astype(str).agg("".join,axis=1).value_counts()
    return {"variables":out,"pattern_count":int(len(patterns)),
      "most_common_patterns":[{"pattern_1_missing_0_observed":k,"n":int(v)} for k,v in patterns.head(10).items()],
      "interpretation":"Descriptive missingness patterns cannot identify MCAR, MAR or MNAR by themselves. Use study knowledge and sensitivity analysis; do not infer mechanism from percentages alone."}

def run(input_path,config_path,output):
    cfg=json.loads(Path(config_path).read_text()); df=pd.read_csv(input_path) if str(input_path).endswith(".csv") else pd.read_excel(input_path)
    out=Path(output); out.mkdir(parents=True,exist_ok=True)
    result={"version":VERSION,"generated_utc":datetime.now(timezone.utc).isoformat(),"input_sha256":sha256(input_path),
      "n_rows":len(df),"nonparametric":[],"paired":[],"repeated_measures":[],"prediction":[],"power":[],"missingness":[]}
    for s in cfg.get("nonparametric",[]): result["nonparametric"].append(independent_nonparametric(df,s["outcome"],s["group"],s.get("bootstrap_replicates",3000),s.get("seed",524)))
    for s in cfg.get("paired",[]): result["paired"].append(paired_analysis(df,s["before"],s["after"],s.get("bootstrap_replicates",3000),s.get("seed",524)))
    for s in cfg.get("repeated_measures",[]): result["repeated_measures"].append(repeated_measures_friedman(df,s["subject"],s["conditions"]))
    for s in cfg.get("prediction",[]): result["prediction"].append(validated_roc(df,s["outcome"],s["predictors"],s.get("folds",5),s.get("repeats",3),s.get("seed",524)))
    for s in cfg.get("power",[]): result["power"].append(power_two_sample_mean(s["effect_size"],s.get("alpha",.05),s.get("power",.8),s.get("allocation_ratio",1)))
    for s in cfg.get("missingness",[]): result["missingness"].append(missingness_assessment(df,s.get("columns",[])))
    if not any(result[k] for k in ["nonparametric","paired","repeated_measures","prediction","power","missingness"]): raise ValueError("No analyses configured")
    result["warnings"]=["No multiple imputation is implemented in this release; do not treat median imputation in the predictive pipeline as inferential missing-data handling.",
      "All methods require a design-appropriate analysis plan and review. The synthetic dataset is not clinical evidence."]
    (out/"clinical_methods_results.json").write_text(json.dumps(result,indent=2,allow_nan=False))
    lines=["# Clinical research methods report","",f"- Dataset rows: {len(df)}",f"- Input SHA-256: `{result['input_sha256']}`",""]
    for key in ["nonparametric","paired","repeated_measures","prediction","power","missingness"]:
        lines += [f"## {key.replace('_',' ').title()}",""]
        lines += [f"- {json.dumps(x,ensure_ascii=False)}" for x in result[key]] or ["- No analyses configured."]
        lines.append("")
    lines += ["## Warnings"]+[f"- {w}" for w in result["warnings"]]
    (out/"clinical_methods_report.md").write_text("\n".join(lines)+"\n")
    manifest={"version":VERSION,"input_sha256":result["input_sha256"],"outputs":{
      "clinical_methods_results.json":sha256(out/"clinical_methods_results.json"),
      "clinical_methods_report.md":sha256(out/"clinical_methods_report.md")}}
    (out/"evidence_manifest.json").write_text(json.dumps(manifest,indent=2))
    return result

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input",required=True); ap.add_argument("--config",required=True); ap.add_argument("--output",required=True)
    a=ap.parse_args(); r=run(a.input,a.config,a.output)
    print(json.dumps({"status":"success","n_rows":r["n_rows"],"nonparametric":len(r["nonparametric"]),
      "paired":len(r["paired"]),"repeated_measures":len(r["repeated_measures"]),
      "prediction":len(r["prediction"]),"power":len(r["power"]),"missingness":len(r["missingness"])}))
if __name__=="__main__": main()
