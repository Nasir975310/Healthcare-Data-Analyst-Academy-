"""Reproducible descriptive and inferential analysis of synthetic cohort data.
Run: python clinical_statistics_analysis.py --data ../data/synthetic_clinical_cohort.csv --out ../reports
Requires pandas, numpy, scipy, statsmodels, matplotlib, scikit-learn.
"""
from __future__ import annotations
import argparse, json, platform
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.metrics import roc_auc_score, confusion_matrix, brier_score_loss
from sklearn.calibration import calibration_curve
import matplotlib.pyplot as plt

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--data",default="../data/synthetic_clinical_cohort.csv")
    ap.add_argument("--out",default="../reports")
    args=ap.parse_args()
    data=Path(args.data); out=Path(args.out); out.mkdir(parents=True,exist_ok=True)
    df=pd.read_csv(data)
    required={"patient_id","age_years","diabetes","ckd","treatment_group","baseline_sbp_mmhg","followup_sbp_mmhg","event_time_days","event_observed","followup_days"}
    missing=required-set(df.columns)
    if missing: raise ValueError(f"Missing columns: {sorted(missing)}")
    if df.patient_id.duplicated().any(): raise ValueError("Duplicate patient_id values")
    if not df.event_observed.isin([0,1]).all(): raise ValueError("event_observed must be 0/1")
    if (df.event_time_days<=0).any() or (df.event_time_days>df.followup_days).any(): raise ValueError("Invalid event/censor time")
    # Cohort table
    cohort=df.groupby("treatment_group").agg(
        n=("patient_id","count"), age_mean=("age_years","mean"),
        baseline_sbp_mean=("baseline_sbp_mmhg","mean"),
        followup_sbp_mean=("followup_sbp_mmhg","mean"),
        followup_sbp_sd=("followup_sbp_mmhg","std"),
        event_n=("event_observed","sum")
    ).reset_index()
    cohort.to_csv(out/"cohort_summary.csv",index=False)
    # Welch test and bootstrap CI for mean difference: enhanced minus standard
    a=df.loc[df.treatment_group=="Enhanced follow-up","followup_sbp_mmhg"].to_numpy()
    b=df.loc[df.treatment_group=="Standard care","followup_sbp_mmhg"].to_numpy()
    diff=float(a.mean()-b.mean())
    test=stats.ttest_ind(a,b,equal_var=False)
    rng=np.random.default_rng(2606); boot=[]
    for _ in range(5000):
        boot.append(rng.choice(a,len(a),replace=True).mean()-rng.choice(b,len(b),replace=True).mean())
    ci=np.quantile(boot,[.025,.975]).tolist()
    pooled=np.sqrt(((len(a)-1)*a.var(ddof=1)+(len(b)-1)*b.var(ddof=1))/(len(a)+len(b)-2))
    d=float(diff/pooled)
    # OLS adjusted association
    ols=smf.ols("followup_sbp_mmhg ~ C(treatment_group) + baseline_sbp_mmhg + age_years + diabetes + ckd",data=df).fit()
    with open(out/"ols_summary.txt","w") as f: f.write(ols.summary().as_text())
    # Logistic model and simple holdout evaluation
    from sklearn.model_selection import train_test_split
    from sklearn.compose import ColumnTransformer
    from sklearn.preprocessing import OneHotEncoder, StandardScaler
    from sklearn.pipeline import Pipeline
    from sklearn.impute import SimpleImputer
    from sklearn.linear_model import LogisticRegression
    X=df[["age_years","diabetes","ckd","treatment_group"]]
    y=df.event_observed
    Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.25,random_state=2606,stratify=y)
    prep=ColumnTransformer([
      ("num",Pipeline([("impute",SimpleImputer(strategy="median")),("scale",StandardScaler())]),["age_years","diabetes","ckd"]),
      ("cat",OneHotEncoder(handle_unknown="ignore"),["treatment_group"])
    ])
    model=Pipeline([("prep",prep),("model",LogisticRegression(max_iter=2000,class_weight=None))])
    model.fit(Xtr,ytr); prob=model.predict_proba(Xte)[:,1]; pred=(prob>=.5).astype(int)
    auc=float(roc_auc_score(yte,prob)) if yte.nunique()==2 else None
    cm=confusion_matrix(yte,pred,labels=[0,1]).tolist()
    # Diagnostic example, deliberately hypothetical and independent of cohort
    tp,fp,fn,tn=82,18,28,872
    sens=tp/(tp+fn); spec=tn/(tn+fp); ppv=tp/(tp+fp); npv=tn/(tn+fn)
    results={
      "dataset":"synthetic_clinical_cohort.csv","n":int(len(df)),
      "event_count":int(y.sum()),"event_fraction":float(y.mean()),
      "followup_sbp_difference_enhanced_minus_standard_mmhg":diff,
      "welch_t_p_value":float(test.pvalue),"bootstrap_95pct_ci_mmhg":ci,
      "cohens_d":d,"ols_r_squared":float(ols.rsquared),
      "logistic_holdout_auc":auc,"logistic_holdout_brier":float(brier_score_loss(yte,prob)),
      "logistic_holdout_confusion_matrix_tn_fp_fn_tp":cm,
      "logistic_threshold":0.5,
      "logistic_threshold_note":"At this threshold the rare-event model may predict no positive cases; inspect sensitivity/precision-recall and calibration rather than treating accuracy as adequate.",
      "hypothetical_diagnostic_test":{"tp":tp,"fp":fp,"fn":fn,"tn":tn,"sensitivity":sens,"specificity":spec,"ppv":ppv,"npv":npv},
      "software":{"python":platform.python_version(),"pandas":pd.__version__,"numpy":np.__version__}
    }
    (out/"analysis_results.json").write_text(json.dumps(results,indent=2))
    # Figure
    fig,ax=plt.subplots(figsize=(7,4))
    df.boxplot(column="followup_sbp_mmhg",by="treatment_group",ax=ax)
    ax.set_title("Synthetic follow-up systolic blood pressure by group")
    ax.set_xlabel("Simulated group"); ax.set_ylabel("Follow-up SBP (mmHg)")
    fig.suptitle(""); fig.tight_layout(); fig.savefig(out/"followup_sbp_by_group.png",dpi=150); plt.close(fig)
    print(json.dumps(results,indent=2))
if __name__=="__main__": main()
