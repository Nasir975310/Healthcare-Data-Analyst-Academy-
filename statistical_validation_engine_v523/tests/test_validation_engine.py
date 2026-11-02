import importlib.util
from pathlib import Path
import numpy as np, pandas as pd, pytest

HERE=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("validation",HERE/"scripts"/"validation_engine.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
DATA=HERE.parent/"advanced_statistics_execution_v521"/"data"/"synthetic_healthcare_dataset.csv"

def test_bootstrap_reproducible():
    x=[1,2,3,4,5,6]
    a=m.bootstrap_mean_ci(x,500,.95,17)
    b=m.bootstrap_mean_ci(x,500,.95,17)
    assert a==b and a["lower"]<=a["mean"]<=a["upper"]

def test_bootstrap_rejects_small_replicates():
    with pytest.raises(ValueError,match="at least 200"):
        m.bootstrap_mean_ci([1,2,3],100)

def test_group_diagnostics():
    df=pd.read_csv(DATA)
    result=m.group_diagnostics(df,"los_days","sex")
    assert result["variance_homogeneity"]["test"]=="Levene median-centred"
    assert len(result["normality"])==2

def test_regression_hc3_and_diagnostics():
    df=pd.read_csv(DATA)
    r=m.regression_diagnostics(df,"los_days",["age","systolic_bp"],"linear")
    assert r["family"]=="linear_OLS"
    assert all("HC3_robust_se" in x for x in r["coefficients"])
    assert "heteroscedasticity" in r and "influence" in r and "multicollinearity" in r

def test_multiplicity_holm():
    x=m.adjust_pvalues([{"name":"a","p_value":.01},{"name":"b","p_value":.04},{"name":"c","p_value":.2}],"holm")
    assert x[0]["adjusted_p_value"]==pytest.approx(.03)
    assert x[1]["adjusted_p_value"]==pytest.approx(.08)

def test_multiplicity_invalid_pvalue():
    with pytest.raises(ValueError,match="between 0 and 1"):
        m.adjust_pvalues([{"name":"bad","p_value":1.2}])

def test_end_to_end(tmp_path):
    r=m.run(DATA,HERE/"templates"/"validation_config.json",tmp_path/"out")
    assert len(r["assumption_diagnostics"])==1
    assert len(r["bootstrap"])==1
    assert len(r["regressions"])==1
    assert len(r["multiplicity"])==1
    assert (tmp_path/"out"/"validation_manifest.json").exists()
    assert (tmp_path/"out"/"validation_report.md").exists()

def test_logistic_requires_two_classes():
    df=pd.DataFrame({"y":[0,0,0,0,0],"x":[1,2,3,4,5]})
    with pytest.raises(ValueError,match="both binary classes"):
        m.regression_diagnostics(df,"y",["x"],"logistic")
