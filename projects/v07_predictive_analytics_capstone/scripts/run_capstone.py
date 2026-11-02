"""Synthetic, educational healthcare-risk modelling capstone.

This program creates synthetic patient-level records, compares a prevalence baseline
with logistic regression and a random forest, and writes validation outputs.
It is not a clinical decision-support tool.
"""
from pathlib import Path
import json
import platform
import sys

import numpy as np
import pandas as pd
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    roc_auc_score, average_precision_score, confusion_matrix,
    precision_score, recall_score, f1_score, brier_score_loss
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORTS = ROOT / "reports"
DATA.mkdir(exist_ok=True)
REPORTS.mkdir(exist_ok=True)
RANDOM_STATE = 2026

def make_synthetic_data(n=2400):
    rng = np.random.default_rng(RANDOM_STATE)
    age = rng.integers(18, 91, n)
    prior_admissions = rng.poisson(0.65, n)
    comorbidity_count = np.clip(rng.poisson(2.0, n), 0, 10)
    length_of_stay = np.clip(rng.gamma(2.0, 2.2, n), 0.5, 30)
    systolic_bp = np.clip(rng.normal(132, 19, n), 80, 220)
    department = rng.choice(["Medicine", "Surgery", "Cardiology", "Other"], n,
                            p=[0.42, 0.22, 0.18, 0.18])
    # Synthetic relationship only; no real clinical inference is intended.
    logit = (-3.15 + 0.018*(age-50) + 0.48*prior_admissions
             + 0.17*comorbidity_count + 0.045*(length_of_stay-4)
             + 0.006*(systolic_bp-130)
             + np.where(department=="Medicine",0.18,0))
    probability = 1/(1+np.exp(-logit))
    outcome = rng.binomial(1, probability)
    df = pd.DataFrame({
        "synthetic_patient_id": [f"SYN{i:05d}" for i in range(n)],
        "age": age, "prior_admissions_12m": prior_admissions,
        "comorbidity_count": comorbidity_count,
        "length_of_stay_days": length_of_stay.round(1),
        "systolic_bp": systolic_bp.round(1),
        "department": department,
        "readmitted_30d": outcome
    })
    # Introduce realistic missingness in predictors only.
    for col, rate in [("systolic_bp",0.08),("comorbidity_count",0.025)]:
        mask = rng.random(n) < rate
        df.loc[mask,col] = np.nan
    return df

def main():
    df = make_synthetic_data()
    data_path = DATA / "synthetic_patient_cohort.csv"
    df.to_csv(data_path,index=False)
    assert df["synthetic_patient_id"].is_unique, "Patient IDs must be unique."
    assert df["readmitted_30d"].isin([0,1]).all(), "Outcome must be binary."
    assert df["age"].between(18,90).all(), "Unexpected age range."

    target = "readmitted_30d"
    id_col = "synthetic_patient_id"
    features = [c for c in df.columns if c not in [target,id_col]]
    X, y = df[features], df[target]
    X_train, X_test, y_train, y_test = train_test_split(
        X,y,test_size=0.25,random_state=RANDOM_STATE,stratify=y
    )
    numeric = ["age","prior_admissions_12m","comorbidity_count",
               "length_of_stay_days","systolic_bp"]
    categorical = ["department"]
    preprocessor = ColumnTransformer([
        ("num",Pipeline([("impute",SimpleImputer(strategy="median")),
                         ("scale",StandardScaler())]),numeric),
        ("cat",Pipeline([("impute",SimpleImputer(strategy="most_frequent")),
                         ("encode",OneHotEncoder(handle_unknown="ignore"))]),categorical)
    ])
    models = {
        "logistic_regression": LogisticRegression(max_iter=1000,class_weight="balanced",
                                                   random_state=RANDOM_STATE),
        "random_forest": RandomForestClassifier(n_estimators=250,min_samples_leaf=8,
                                                class_weight="balanced_subsample",
                                                random_state=RANDOM_STATE,n_jobs=-1)
    }
    prevalence = float(y_train.mean())
    rows=[]
    for name, estimator in models.items():
        model=Pipeline([("preprocess",preprocessor),("model",estimator)])
        model.fit(X_train,y_train)
        probabilities=model.predict_proba(X_test)[:,1]
        # Illustrative 0.5 threshold only; a real threshold requires workflow analysis.
        predictions=(probabilities>=0.5).astype(int)
        tn,fp,fn,tp=confusion_matrix(y_test,predictions,labels=[0,1]).ravel()
        rows.append({
            "model":name,"test_n":len(y_test),"test_prevalence":float(y_test.mean()),
            "auroc":roc_auc_score(y_test,probabilities),
            "average_precision":average_precision_score(y_test,probabilities),
            "precision_at_0_5":precision_score(y_test,predictions,zero_division=0),
            "sensitivity_at_0_5":recall_score(y_test,predictions,zero_division=0),
            "specificity_at_0_5":float(tn/(tn+fp)) if tn+fp else None,
            "f1_at_0_5":f1_score(y_test,predictions,zero_division=0),
            "brier_score":brier_score_loss(y_test,probabilities),
            "tn":int(tn),"fp":int(fp),"fn":int(fn),"tp":int(tp)
        })
    metrics=pd.DataFrame(rows)
    metrics.to_csv(REPORTS/"model_metrics.csv",index=False)
    summary={
        "purpose":"Synthetic educational demonstration only; not for clinical use.",
        "python":sys.version.split()[0],"platform":platform.platform(),
        "pandas":pd.__version__,"scikit_learn":sklearn.__version__,
        "random_state":RANDOM_STATE,"n_patients":len(df),
        "train_n":len(X_train),"test_n":len(X_test),
        "training_prevalence_baseline":prevalence,
        "outcome_prevalence":float(y.mean()),
        "missing_predictors":df[features].isna().sum().to_dict(),
        "unique_patient_ids":bool(df[id_col].is_unique),
        "split":"Stratified patient-level holdout; one row per synthetic patient.",
        "caution":"The synthetic outcome mechanism is artificial. Metrics do not establish clinical validity."
    }
    (REPORTS/"run_summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    (REPORTS/"validation.txt").write_text(
        "PASS: unique synthetic patient IDs\n"
        "PASS: binary outcome domain\n"
        "PASS: age range\n"
        "PASS: preprocessing is fitted inside scikit-learn pipelines\n"
        "PASS: test partition held out from model fitting\n"
        "CAUTION: one-row-per-patient synthetic holdout is not external validation\n",
        encoding="utf-8"
    )
    print("Synthetic cohort:",data_path)
    print(metrics.to_string(index=False))
    print("Reports written to:",REPORTS)

if __name__=="__main__":
    main()
