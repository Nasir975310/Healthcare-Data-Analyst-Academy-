import importlib.util, json
from pathlib import Path
import pandas as pd

HERE=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("reporting",HERE/"scripts"/"integrated_reporting.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def test_table1_continuous_and_categorical():
    df=pd.DataFrame({"age":[20,30,40,None],"sex":["F","M","F","M"],"arm":["A","A","B","B"]})
    cfg={"table1":{"group":"arm","variables":[{"column":"age","type":"continuous"},{"column":"sex","type":"categorical"}]}}
    result=m.table1(df,cfg)
    assert "Mean ± SD" in set(result.method)
    assert "n (%)" in set(result.method)
    assert result.loc[result.variable=="age","missing"].max()==1

def test_table1_missing_column_raises():
    import pytest
    with pytest.raises(KeyError):
        m.table1(pd.DataFrame({"x":[1]}),{"table1":{"variables":[{"column":"missing"}]}})

def test_end_to_end_demo(tmp_path):
    cfg_path=HERE/"templates"/"report_config.json"
    data=HERE/"data"/"synthetic_reporting_dataset.csv"
    result=m.run(data,cfg_path,tmp_path/"out")
    out=tmp_path/"out"
    assert result["validation"]["passed"]
    assert (out/"table1.csv").exists()
    assert (out/"executive_summary.md").exists()
    assert (out/"technical_report.md").exists()
    assert (out/"evidence_manifest.json").exists()
    assert (out/"roc_summary.json").exists()
    assert (out/"kaplan_meier_summary.json").exists()
    assert len(result["figures"])>=7

def test_roc_rejects_nonbinary_outcome(tmp_path):
    import pytest
    df=pd.DataFrame({"y":[0,0,0,0],"s":[.1,.2,.3,.4]})
    cfg={"plots":{"roc":{"outcome":"y","score":"s"}}}
    with pytest.raises(ValueError,match="both binary"):
        m.make_plots(df,cfg,tmp_path)

def test_km_rejects_invalid_event(tmp_path):
    import pytest
    df=pd.DataFrame({"t":[1,2,3],"e":[0,2,1]})
    with pytest.raises(ValueError,match="event coded"):
        m.make_plots(df,{"plots":{"kaplan_meier":{"time":"t","event":"e"}}},tmp_path)

def test_output_validation_detects_empty_file(tmp_path):
    (tmp_path/"empty.txt").write_text("")
    assert not m.validate_outputs(tmp_path)["passed"]
