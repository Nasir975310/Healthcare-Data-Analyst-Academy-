import importlib.util
from pathlib import Path
import math
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("analysis",ROOT/"scripts"/"analyze_study.py")
analysis=importlib.util.module_from_spec(spec); spec.loader.exec_module(analysis)
DATA=ROOT/"data"/"synthetic_bp_study.csv"

def test_analysis_structure_and_provenance():
    r=analysis.analyze(DATA,"followup_sbp","group","intervention","usual_care","baseline_sbp")
    assert r["metadata"]["rows"]==18
    assert len(r["metadata"]["input_sha256"])==64
    assert r["by_group"]["intervention"]["n"]==9
    assert r["by_group"]["usual_care"]["n"]==9
    assert "welch_t" in r["tests"] and "mann_whitney" in r["tests"]
    assert "paired_t_overall" in r["tests"]
    assert "cohens_d" in r["effect_sizes"]
    assert "sex" in r["categorical"]

def test_missingness_and_ci():
    assert analysis.summarize([1,2,None])["missing"]==1
    ci=analysis.mean_ci([1,2,3,4])
    assert ci["lower"] < ci["estimate"] < ci["upper"]

def test_outputs_are_written(tmp_path):
    r=analysis.analyze(DATA,"followup_sbp","group","intervention","usual_care","baseline_sbp")
    analysis.write_outputs(r,tmp_path)
    for name in ["analysis_report.json","analysis_summary.csv","analysis_report.html"]:
        assert (tmp_path/name).is_file() and (tmp_path/name).stat().st_size>0

def test_missing_group_is_rejected():
    try:
        analysis.analyze(DATA,"followup_sbp","group","missing","usual_care","baseline_sbp")
    except ValueError as e:
        assert "two non-missing" in str(e)
    else: raise AssertionError("Expected insufficient group data to fail")
