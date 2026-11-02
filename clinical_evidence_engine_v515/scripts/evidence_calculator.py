#!/usr/bin/env python3
"""Clinical evidence calculators: 2x2 effect measures and diagnostic accuracy.

Requires Python 3.10+ and pandas. Educational calculations only. Interpret
confidence intervals and study validity in context; do not use as prescribing advice.
"""
from __future__ import annotations
import argparse, csv, json, math, hashlib
from pathlib import Path
from datetime import datetime, timezone

def wilson(k:int,n:int,z:float=1.959963984540054):
    if n<=0 or k<0 or k>n: raise ValueError("Require 0 <= events <= denominator and denominator > 0.")
    p=k/n; den=1+z*z/n
    center=(p+z*z/(2*n))/den
    half=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return [center-half,center+half]

def validate_counts(a,b,c,d):
    vals=[a,b,c,d]
    if any(not isinstance(x,int) or x<0 for x in vals):
        raise ValueError("All cell counts must be non-negative integers.")
    if a+b==0 or c+d==0: raise ValueError("Each study arm needs a positive denominator.")
    if a+b < a or c+d < c: raise ValueError("Invalid event counts.")

def effect_measures(event_t,total_t,event_c,total_c,continuity_correction=False):
    validate_counts(event_t,total_t-event_t,event_c,total_c-event_c)
    rt=event_t/total_t; rc=event_c/total_c
    rd=rt-rc
    # Wald CI for risk difference; Wilson intervals are also provided per arm.
    se_rd=math.sqrt(rt*(1-rt)/total_t+rc*(1-rc)/total_c)
    rd_ci=[rd-1.959963984540054*se_rd,rd+1.959963984540054*se_rd]
    # Ratio measures: log scale. If any cell is zero, optional Haldane-Anscombe correction.
    et,nt,ec,nc=event_t,total_t-event_t,event_c,total_c-event_c
    corrected=False
    if min(et,nt,ec,nc)==0:
        if not continuity_correction:
            rr=orr=None; rr_ci=orr_ci=None
        else:
            et+=.5; nt+=.5; ec+=.5; nc+=.5; corrected=True
            rr=(et/(et+nt))/(ec/(ec+nc))
            orr=(et*nc)/(nt*ec)
            se_log_rr=math.sqrt(1/et-1/(et+nt)+1/ec-1/(ec+nc))
            se_log_or=math.sqrt(1/et+1/nt+1/ec+1/nc)
            rr_ci=[math.exp(math.log(rr)-1.959963984540054*se_log_rr),math.exp(math.log(rr)+1.959963984540054*se_log_rr)]
            orr_ci=[math.exp(math.log(orr)-1.959963984540054*se_log_or),math.exp(math.log(orr)+1.959963984540054*se_log_or)]
    else:
        rr=rt/rc
        orr=(et*nc)/(nt*ec)
        se_log_rr=math.sqrt(1/et-1/(et+nt)+1/ec-1/(ec+nc))
        se_log_or=math.sqrt(1/et+1/nt+1/ec+1/nc)
        rr_ci=[math.exp(math.log(rr)-1.959963984540054*se_log_rr),math.exp(math.log(rr)+1.959963984540054*se_log_rr)]
        orr_ci=[math.exp(math.log(orr)-1.959963984540054*se_log_or),math.exp(math.log(orr)+1.959963984540054*se_log_or)]
    arr=-rd
    nnt=None
    if arr>0: nnt=math.ceil(1/arr-1e-12)
    nnh=None
    if rd>0: nnh=math.ceil(1/rd-1e-12)
    return {
      "event_risk":{"intervention":rt,"control":rc},
      "risk_difference_intervention_minus_control":{"estimate":rd,"ci_95_wald":rd_ci,
        "interpretation":"Negative means fewer events in intervention arm; positive means more events."},
      "relative_risk":{"estimate":rr,"ci_95_log_wald":rr_ci},
      "odds_ratio":{"estimate":orr,"ci_95_log_wald":orr_ci},
      "absolute_risk_reduction":{"estimate":arr if arr>0 else None,
        "nnt":nnt,"note":"NNT shown only when intervention event risk is lower; calculated by ceiling of reciprocal ARR."},
      "absolute_risk_increase":{"estimate":rd if rd>0 else None,
        "nnh":nnh,"note":"NNH shown only when intervention event risk is higher; calculated by ceiling of reciprocal absolute risk increase."},
      "risk_ci_wilson":{"intervention":wilson(event_t,total_t),"control":wilson(event_c,total_c)},
      "continuity_correction_applied":corrected,
      "cautions":["Risk difference CI uses a simple Wald approximation; small samples or extreme risks need more robust methods.",
       "RR and OR intervals use log-Wald approximations; zero cells require an explicitly selected correction or an exact method.",
       "NNT/NNH is time-horizon- and outcome-specific; include the follow-up period and confidence interval for ARR.",
       "Odds ratios are not risk ratios and can exaggerate relative effect when outcomes are common."]}

def diagnostic(tp,fn,fp,tn,prevalence=None):
    vals=[tp,fn,fp,tn]
    if any(not isinstance(x,int) or x<0 for x in vals): raise ValueError("Counts must be non-negative integers.")
    diseased=tp+fn; nondiseased=fp+tn
    if diseased==0 or nondiseased==0: raise ValueError("Need at least one diseased and one non-diseased participant.")
    sens=tp/diseased; spec=tn/nondiseased
    ppv=tp/(tp+fp) if tp+fp else None
    npv=tn/(tn+fn) if tn+fn else None
    lr_pos=sens/(1-spec) if spec<1 else None
    lr_neg=(1-sens)/spec if spec>0 else None
    out={"counts":{"true_positive":tp,"false_negative":fn,"false_positive":fp,"true_negative":tn},
      "sensitivity":{"estimate":sens,"ci_95_wilson":wilson(tp,diseased)},
      "specificity":{"estimate":spec,"ci_95_wilson":wilson(tn,nondiseased)},
      "ppv":{"estimate":ppv,"ci_95_wilson":wilson(tp,tp+fp) if tp+fp else None},
      "npv":{"estimate":npv,"ci_95_wilson":wilson(tn,tn+fn) if tn+fn else None},
      "likelihood_ratios":{"positive":lr_pos,"negative":lr_neg},
      "accuracy":(tp+tn)/(tp+fn+fp+tn),
      "prevalence_in_sample":diseased/(diseased+nondiseased),
      "cautions":["PPV and NPV depend on prevalence and may not transport to another setting.",
       "Sensitivity and specificity can vary with threshold, spectrum and reference-standard quality.",
       "AUC requires patient-level test scores and cannot be calculated from one 2x2 table.",
       "Diagnostic accuracy does not alone establish clinical utility or patient benefit."]}
    if prevalence is not None:
        if not 0<prevalence<1: raise ValueError("Target prevalence must be between 0 and 1.")
        denom_ppv=sens*prevalence+(1-spec)*(1-prevalence)
        denom_npv=spec*(1-prevalence)+(1-sens)*prevalence
        out["predictive_values_at_target_prevalence"]={"prevalence":prevalence,
          "ppv":sens*prevalence/denom_ppv if denom_ppv else None,
          "npv":spec*(1-prevalence)/denom_npv if denom_npv else None,
          "note":"Bayes-derived estimates assuming sensitivity and specificity transport unchanged to target setting."}
    return out

def main():
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest="mode",required=True)
    e=sub.add_parser("effects"); e.add_argument("--event-intervention",type=int,required=True); e.add_argument("--total-intervention",type=int,required=True); e.add_argument("--event-control",type=int,required=True); e.add_argument("--total-control",type=int,required=True); e.add_argument("--continuity-correction",action="store_true")
    d=sub.add_parser("diagnostic"); d.add_argument("--tp",type=int,required=True); d.add_argument("--fn",type=int,required=True); d.add_argument("--fp",type=int,required=True); d.add_argument("--tn",type=int,required=True); d.add_argument("--prevalence",type=float)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    result=effect_measures(a.event_intervention,a.total_intervention,a.event_control,a.total_control,a.continuity_correction) if a.mode=="effects" else diagnostic(a.tp,a.fn,a.fp,a.tn,a.prevalence)
    result["metadata"]={"analysis_type":a.mode,"generated_utc":datetime.now(timezone.utc).isoformat()}
    raw=json.dumps(result,indent=2,allow_nan=False)
    if a.output: a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(raw,encoding="utf-8")
    print(raw)
if __name__=="__main__": main()
