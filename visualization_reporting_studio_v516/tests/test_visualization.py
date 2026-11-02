import importlib.util
from pathlib import Path
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("viz",ROOT/"scripts"/"visualize_study.py")
viz=importlib.util.module_from_spec(spec); spec.loader.exec_module(viz)

def test_roc_auc_perfect_ordering():
    fpr,tpr,auc=viz.roc_points([0,0,1,1],[.1,.2,.8,.9])
    assert auc==1.0
    assert fpr[0]==0 and tpr[-1]==1

def test_roc_rejects_single_class():
    try: viz.roc_points([1,1],[.2,.8])
    except ValueError: pass
    else: raise AssertionError("ROC must reject a single reference class")

def test_kaplan_meier_product_limit():
    x,y,n,d=viz.km_curve([1,2,3],[1,0,1])
    assert list(x)==[0.0,1.0,3.0]
    assert np.isclose(y[-1],0.0)
    assert n==[3,1] and d==[1,1]

def test_forest_plot_and_validation(tmp_path):
    data=ROOT/"data"/"synthetic_forest_effects.csv"
    d=viz.forest_plot(data,tmp_path/"forest.png")
    assert len(d)==5 and (tmp_path/"forest.png").stat().st_size>0
    bad=tmp_path/"bad.csv"; bad.write_text("study,effect,lower,upper\\nX,0.8,0.9,1.1\\n")
    try: viz.forest_plot(bad,tmp_path/"bad.png")
    except ValueError: pass
    else: raise AssertionError("Invalid confidence interval must be rejected")

def test_end_to_end_figures_and_reports(tmp_path):
    df=pd.read_csv(ROOT/"data"/"synthetic_visualization_study.csv")
    figs=viz.make_figures(df,tmp_path,"group","followup_sbp","biomarker_score","followup_days","event")
    assert "group_boxplot.png" in figs
    assert "roc_curve.png" in figs
    assert "kaplan_meier.png" in figs
    viz.report(tmp_path,ROOT/"data"/"synthetic_visualization_study.csv",figs,"a"*64,len(df))
    assert (tmp_path/"visualization_report.html").exists()
    assert (tmp_path/"visualization_report.md").exists()
