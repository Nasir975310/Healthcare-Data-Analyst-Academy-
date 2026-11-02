#!/usr/bin/env python3
"""Generate publication-oriented figures and summaries from a CSV study dataset.

Requires Python 3.10+, pandas, numpy, matplotlib. No seaborn.
Figures are descriptive; inspect study design and assumptions before interpretation.
"""
from __future__ import annotations
import argparse, hashlib, json, math
from pathlib import Path
from datetime import datetime, timezone
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def savefig(fig,path):
    fig.tight_layout()
    fig.savefig(path,dpi=220,bbox_inches="tight")
    plt.close(fig)

def roc_points(y,score):
    y=np.asarray(y,dtype=int); score=np.asarray(score,dtype=float)
    if set(np.unique(y))- {0,1}: raise ValueError("ROC outcome must contain only 0 and 1.")
    pos=int((y==1).sum()); neg=int((y==0).sum())
    if pos==0 or neg==0: raise ValueError("ROC requires at least one positive and one negative reference outcome.")
    thresholds=np.r_[np.inf,np.sort(np.unique(score))[::-1],-np.inf]
    pts=[]
    for t in thresholds:
        pred=score>=t
        tp=int(((pred)&(y==1)).sum()); fp=int(((pred)&(y==0)).sum())
        pts.append((fp/neg,tp/pos))
    pts=sorted(set(pts))
    fpr=np.array([p[0] for p in pts]); tpr=np.array([p[1] for p in pts])
    auc=float(np.trapezoid(tpr,fpr))
    return fpr,tpr,auc

def km_curve(time,event):
    t=np.asarray(time,dtype=float); e=np.asarray(event,dtype=int)
    if len(t)==0 or len(t)!=len(e) or np.any(~np.isfinite(t)) or np.any(t<0):
        raise ValueError("Survival times must be finite, non-negative and paired with event indicators.")
    if set(np.unique(e))- {0,1}: raise ValueError("Event indicator must be 0=censored or 1=event.")
    surv=1.0; xs=[0.0]; ys=[1.0]; at_risk=[]; event_counts=[]
    for tm in sorted(np.unique(t[e==1])):
        n=int((t>=tm).sum()); d=int(((t==tm)&(e==1)).sum())
        at_risk.append(n); event_counts.append(d)
        surv*=1-d/n
        xs.append(float(tm)); ys.append(float(surv))
    return np.array(xs),np.array(ys),at_risk,event_counts

def make_figures(df,outdir,group_col,outcome_col,score_col,time_col,event_col):
    outdir.mkdir(parents=True,exist_ok=True); figures=[]
    numeric=df.select_dtypes(include=[np.number])
    for col in numeric.columns:
        vals=pd.to_numeric(df[col],errors="coerce").dropna()
        if len(vals)<2: continue
        fig,ax=plt.subplots(figsize=(7,4.4)); ax.hist(vals,bins="auto",edgecolor="black")
        ax.set(title=f"Distribution of {col}",xlabel=col,ylabel="Frequency")
        p=outdir/f"histogram_{col}.png"; savefig(fig,p); figures.append(p.name)
    if group_col in df and outcome_col in df:
        groups=[g for g in df[group_col].dropna().unique()]
        data=[pd.to_numeric(df.loc[df[group_col]==g,outcome_col],errors="coerce").dropna().values for g in groups]
        data=[x for x in data if len(x)>0]
        if len(data)>=2:
            fig,ax=plt.subplots(figsize=(7,4.4)); ax.boxplot(data,tick_labels=groups,showmeans=True)
            ax.set(title=f"{outcome_col} by {group_col}",xlabel=group_col,ylabel=outcome_col)
            p=outdir/"group_boxplot.png"; savefig(fig,p); figures.append(p.name)
    if outcome_col in df and group_col in df:
        tab=df.groupby(group_col,dropna=False)[outcome_col].agg(["count","mean","std","median"]).reset_index()
        tab.to_csv(outdir/"group_descriptive_summary.csv",index=False)
    if score_col in df and event_col in df:
        pair=df[[score_col,event_col]].apply(pd.to_numeric,errors="coerce").dropna()
        if len(pair)>2 and pair[event_col].nunique()==2:
            fpr,tpr,auc=roc_points(pair[event_col],pair[score_col])
            fig,ax=plt.subplots(figsize=(5.8,5.2)); ax.plot(fpr,tpr,marker="o",label=f"AUC = {auc:.3f}")
            ax.plot([0,1],[0,1],linestyle="--",label="Chance reference")
            ax.set(xlim=(0,1),ylim=(0,1),xlabel="1 − Specificity (FPR)",ylabel="Sensitivity (TPR)",title="ROC curve")
            ax.legend(loc="lower right")
            p=outdir/"roc_curve.png"; savefig(fig,p); figures.append(p.name)
            (outdir/"roc_summary.json").write_text(json.dumps({"n":len(pair),"auc":auc,
                "note":"Apparent AUC on this dataset; no validation or optimism correction."},indent=2),encoding="utf-8")
    if time_col in df and event_col in df and group_col in df:
        fig,ax=plt.subplots(figsize=(7,4.6)); summaries={}
        for g,sub in df.groupby(group_col):
            pair=sub[[time_col,event_col]].apply(pd.to_numeric,errors="coerce").dropna()
            if len(pair)==0: continue
            x,y,nrisk,nevents=km_curve(pair[time_col],pair[event_col])
            ax.step(x,y,where="post",label=str(g))
            summaries[str(g)]={"n":len(pair),"events":int(pair[event_col].sum()),
                "curve_time":x.tolist(),"survival":y.tolist(),"at_risk_at_event_times":nrisk,"events_at_times":nevents}
        ax.set(xlabel="Follow-up time",ylabel="Estimated event-free probability",ylim=(0,1.03),title="Kaplan–Meier learning curve")
        ax.legend()
        p=outdir/"kaplan_meier.png"; savefig(fig,p); figures.append(p.name)
        (outdir/"kaplan_meier_summary.json").write_text(json.dumps(summaries,indent=2),encoding="utf-8")
    return figures

def forest_plot(csv_path,outpath):
    d=pd.read_csv(csv_path)
    req={"study","effect","lower","upper"}
    if not req.issubset(d.columns): raise ValueError(f"Forest CSV needs columns: {sorted(req)}")
    for c in ["effect","lower","upper"]: d[c]=pd.to_numeric(d[c],errors="raise")
    if (d[["effect","lower","upper"]]<=0).any().any() or (d.lower>d.effect).any() or (d.effect>d.upper).any():
        raise ValueError("Forest plot requires positive estimates with lower <= effect <= upper.")
    y=np.arange(len(d))[::-1]
    fig,ax=plt.subplots(figsize=(8,max(3.5,.55*len(d)+1)))
    ax.errorbar(d.effect,y,xerr=[d.effect-d.lower,d.upper-d.effect],fmt="o",capsize=3)
    ax.axvline(1,linestyle="--")
    ax.set_yticks(y,labels=d.study.astype(str)); ax.set_xscale("log")
    ax.set_xlabel("Effect measure (log scale)"); ax.set_title("Study estimates and 95% confidence intervals")
    savefig(fig,outpath)
    return d

def report(outdir,source,figures,sha,n):
    lines=["# Statistical visualization report","",f"- Input file: `{source.name}`",f"- SHA-256: `{sha}`",f"- Rows: {n}",
           "- Generated UTC: "+datetime.now(timezone.utc).isoformat(),"",
           "## Figures",""]
    for f in figures: lines += [f"### {f}","",f"![{f}]({f})",""]
    lines += ["## Interpretation safeguards","",
      "- Histograms and box plots describe observed data; they do not establish distributional assumptions or causal effects.",
      "- ROC AUC is apparent performance on the supplied data unless external or resampling validation is performed.",
      "- The Kaplan–Meier plot is a descriptive product-limit curve; no log-rank test, confidence bands, competing-risk model or adjusted Cox model is included.",
      "- A forest plot visualizes supplied effect estimates and confidence intervals; it does not calculate a pooled meta-analysis.",
      "- Check missingness, data quality, independence, clustering, prespecification and multiplicity before publication."]
    (outdir/"visualization_report.md").write_text("\\n".join(lines),encoding="utf-8")
    html=["<!doctype html><meta charset='utf-8'><title>Visualization report</title>",
          "<style>body{font:16px system-ui;max-width:1050px;margin:2rem auto;padding:0 1rem;color:#182230}img{max-width:100%;height:auto}section{margin:2rem 0}code{overflow-wrap:anywhere}</style>",
          "<h1>Statistical visualization report</h1>",
          f"<p>Input: <code>{source.name}</code> · rows: {n} · SHA-256: <code>{sha}</code></p>"]
    for f in figures: html.append(f"<section><h2>{f}</h2><img src='{f}' alt='{f}'></section>")
    html.append("<h2>Interpretation safeguards</h2><ul>"+"".join(f"<li>{x}</li>" for x in lines[-6:])+"</ul>")
    (outdir/"visualization_report.html").write_text("".join(html),encoding="utf-8")

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input",type=Path,required=True); p.add_argument("--outdir",type=Path,default=Path("outputs"))
    p.add_argument("--group",default="group"); p.add_argument("--outcome",default="followup_sbp")
    p.add_argument("--score",default="biomarker_score"); p.add_argument("--time",default="followup_days")
    p.add_argument("--event",default="event"); p.add_argument("--forest-csv",type=Path)
    a=p.parse_args()
    df=pd.read_csv(a.input)
    if df.empty: p.error("Input dataset has no rows.")
    sha=hashlib.sha256(a.input.read_bytes()).hexdigest()
    figures=make_figures(df,a.outdir,a.group,a.outcome,a.score,a.time,a.event)
    if a.forest_csv:
        forest_plot(a.forest_csv,a.outdir/"forest_plot.png"); figures.append("forest_plot.png")
    report(a.outdir,a.input,figures,sha,len(df))
    print(json.dumps({"rows":len(df),"sha256":sha,"figures":figures,
        "reports":["visualization_report.md","visualization_report.html"]},indent=2))
if __name__=="__main__": main()
