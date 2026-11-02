import importlib.util
from pathlib import Path
import math
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("ec",ROOT/"scripts"/"evidence_calculator.py")
ec=importlib.util.module_from_spec(spec); spec.loader.exec_module(ec)

def test_effect_measures_known_values():
    r=ec.effect_measures(18,120,30,120)
    assert math.isclose(r["event_risk"]["intervention"],.15)
    assert math.isclose(r["event_risk"]["control"],.25)
    assert math.isclose(r["risk_difference_intervention_minus_control"]["estimate"],-.10)
    assert math.isclose(r["relative_risk"]["estimate"],.6)
    assert r["absolute_risk_reduction"]["nnt"]==10
    assert r["absolute_risk_increase"]["nnh"] is None

def test_harm_direction():
    r=ec.effect_measures(30,100,20,100)
    assert r["absolute_risk_increase"]["nnh"]==10
    assert r["absolute_risk_reduction"]["nnt"] is None

def test_zero_cell_requires_explicit_correction():
    uncorrected=ec.effect_measures(0,20,2,20)
    assert uncorrected["relative_risk"]["estimate"] is None
    assert uncorrected["odds_ratio"]["estimate"] is None
    r=ec.effect_measures(0,20,2,20,True)
    assert r["continuity_correction_applied"] is True

def test_diagnostic_metrics():
    r=ec.diagnostic(82,18,24,176,.10)
    assert math.isclose(r["sensitivity"]["estimate"],.82)
    assert math.isclose(r["specificity"]["estimate"],176/200)
    assert r["predictive_values_at_target_prevalence"]["prevalence"]==.10
    assert r["ppv"]["ci_95_wilson"] is not None

def test_invalid_denominators_rejected():
    for fn in [lambda:ec.effect_measures(5,4,1,10),lambda:ec.diagnostic(2,0,0,0)]:
        try: fn()
        except ValueError: pass
        else: raise AssertionError("Expected invalid input to fail")
