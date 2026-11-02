import importlib.util
from pathlib import Path
import pandas as pd, numpy as np, pytest
HERE=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("clinical_methods",HERE/"scripts"/"clinical_methods.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
DATA=HERE/"data"/"synthetic_clinical_methods.csv"

def test_cliffs_delta_direction():
    assert m.cliffs_delta([5,6,7],[1,2,3])==1.0
    assert m.cliffs_delta([1,2,3],[5,6,7])==-1.0

def test_nonparametric_outputs_effect_size():
    df=pd.read_csv(DATA)
    r=m.independent_nonparametric(df,"followup_sbp","group",500,12)
    assert -1<=r["cliffs_delta"]<=1
    assert len(r["cliffs_delta_ci"])==2

def test_paired_method_and_estimand_note():
    df=pd.read_csv(DATA)
    r=m.paired_analysis(df,"biomarker_before","biomarker_after",500,12)
    assert r["n_pairs"]<len(df)
    assert "different estimand" in r["note"]

def test_friedman():
    df=pd.read_csv(DATA)
    r=m.repeated_measures_friedman(df,"study_id",["measurement_t0","measurement_t1","measurement_t2"])
    assert r["n_complete_subjects"]==len(df)
    assert 0<=r["kendall_w"]<=1

def test_cv_prediction_metrics():
    df=pd.read_csv(DATA)
    r=m.validated_roc(df,"cv_event",["age","baseline_sbp"],5,2,22)
    assert 0<=r["pooled_oof_auc"]<=1
    assert r["brier_score_oof"]>=0
    assert len(r["roc_points"])>1

def test_power_positive():
    r=m.power_two_sample_mean(.5)
    assert r["total_n"]==r["n_group_1"]+r["n_group_2"]
    assert r["total_n"]>0

def test_missingness_descriptive_only():
    df=pd.read_csv(DATA)
    r=m.missingness_assessment(df,["baseline_sbp","age"])
    assert r["variables"][0]["missing_n"]==5
    assert "cannot identify" in r["interpretation"]

def test_cv_rejects_rare_class_for_folds():
    df=pd.DataFrame({"y":[0]*9+[1],"x":range(10)})
    with pytest.raises(ValueError,match="folds must be"):
        m.validated_roc(df,"y",["x"],5,1,1)

def test_end_to_end(tmp_path):
    r=m.run(DATA,HERE/"templates"/"clinical_methods_config.json",tmp_path/"out")
    assert all(r[k] for k in ["nonparametric","paired","repeated_measures","prediction","power","missingness"])
    assert (tmp_path/"out"/"evidence_manifest.json").exists()
