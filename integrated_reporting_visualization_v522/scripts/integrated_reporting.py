#!/usr/bin/env python3
"""Integrated healthcare analytics reporting and visualization pipeline (v5.22.0)."""
from __future__ import annotations
import argparse, hashlib, json, math, platform, sys, warnings
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.metrics import roc_curve, roc_auc_score

VERSION = "5.22.0"

def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024), b""): h.update(chunk)
    return h.hexdigest()

def load_data(path: Path) -> pd.DataFrame:
    suffix=path.suffix.lower()
    if suffix==".csv": return pd.read_csv(path)
    if suffix in (".xlsx",".xls"): return pd.read_excel(path)
    if suffix==".parquet": return pd.read_parquet(path)
    raise ValueError(f"Unsupported input format: {suffix}")

def safe_name(value: str) -> str:
    return "".join(c.lower() if c.isalnum() else "_" for c in str(value)).strip("_") or "variable"

def save_fig(fig, path: Path):
    fig.tight_layout()
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)

def table1(df: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    group=cfg.get("table1",{}).get("group")
    variables=cfg.get("table1",{}).get("variables",[])
    rows=[]
    for item in variables:
        col=item["column"]; label=item.get("label",col); kind=item.get("type","continuous")
        if col not in df: raise KeyError(f"Table 1 column missing: {col}")
        if kind=="continuous":
            x=pd.to_numeric(df[col],errors="coerce").dropna()
            rows.append({"variable":label,"level":"","overall":f"{x.mean():.2f} ± {x.std(ddof=1):.2f}" if len(x)>1 else "Not estimable",
                         "n":int(x.size),"missing":int(df[col].isna().sum()),"method":"Mean ± SD"})
            if group:
                for g,val in df.groupby(group,dropna=False):
                    y=pd.to_numeric(val[col],errors="coerce").dropna()
                    rows.append({"variable":label,"level":str(g),"overall":f"{y.mean():.2f} ± {y.std(ddof=1):.2f}" if len(y)>1 else "Not estimable",
                                 "n":int(y.size),"missing":int(val[col].isna().sum()),"method":"Mean ± SD"})
        elif kind=="categorical":
            counts=df[col].astype("object").where(df[col].notna(),"Missing").value_counts(dropna=False)
            denom=len(df)
            for level,n in counts.items():
                rows.append({"variable":label,"level":str(level),"overall":f"{int(n)} ({(n/denom*100 if denom else 0):.1f}%)",
                             "n":int(n),"missing":int(df[col].isna().sum()),"method":"n (%)"})
                if group:
                    for g,val in df.groupby(group,dropna=False):
                        v=val[col].astype("object").where(val[col].notna(),"Missing")
                        count=int((v==level).sum())
                        rows.append({"variable":label,"level":f"{level} | {g}","overall":f"{count} ({(count/len(val)*100 if len(val) else 0):.1f}%)",
                                     "n":count,"missing":int(val[col].isna().sum()),"method":"n (%)"})
        else: raise ValueError(f"Unknown Table 1 type for {col}: {kind}")
    return pd.DataFrame(rows)

def make_plots(df: pd.DataFrame, cfg: dict, out: Path) -> list:
    pdir=out/"figures"; pdir.mkdir(exist_ok=True)
    produced=[]
    for col in cfg.get("plots",{}).get("histograms",[]):
        if col not in df: raise KeyError(f"Histogram column missing: {col}")
        x=pd.to_numeric(df[col],errors="coerce").dropna()
        if x.empty: continue
        fig,ax=plt.subplots(figsize=(7,4)); ax.hist(x,bins="auto",edgecolor="black")
        ax.set(title=f"Distribution of {col}",xlabel=col,ylabel="Frequency")
        path=pdir/f"histogram_{safe_name(col)}.png"; save_fig(fig,path); produced.append(path)
    for spec in cfg.get("plots",{}).get("boxplots",[]):
        y,g=spec["value"],spec["group"]
        if y not in df or g not in df: raise KeyError(f"Boxplot columns missing: {y}, {g}")
        tmp=df[[y,g]].copy(); tmp[y]=pd.to_numeric(tmp[y],errors="coerce"); tmp=tmp.dropna()
        groups=list(tmp[g].drop_duplicates())
        if not groups: continue
        fig,ax=plt.subplots(figsize=(7,4))
        ax.boxplot([tmp.loc[tmp[g]==v,y] for v in groups],tick_labels=[str(v) for v in groups])
        ax.set(title=f"{y} by {g}",xlabel=g,ylabel=y)
        path=pdir/f"boxplot_{safe_name(y)}_by_{safe_name(g)}.png"; save_fig(fig,path); produced.append(path)
    forest=cfg.get("plots",{}).get("forest_plot")
    if forest:
        effects=pd.read_csv(Path(cfg["_base"])/forest["file"])
        needed=["label","estimate","lower","upper"]
        if not set(needed).issubset(effects): raise ValueError("Forest data requires label, estimate, lower, upper")
        if ((effects.lower>effects.estimate)|(effects.upper<effects.estimate)).any() or (effects.lower<=0).any():
            raise ValueError("Forest plot requires positive estimates and confidence limits containing estimate")
        fig,ax=plt.subplots(figsize=(8,max(3,len(effects)*.55)))
        y=np.arange(len(effects)); ax.errorbar(effects.estimate,y,xerr=[effects.estimate-effects.lower,effects.upper-effects.estimate],fmt="o",capsize=3)
        ax.axvline(1,linestyle="--"); ax.set_yticks(y, effects.label); ax.invert_yaxis(); ax.set_xlabel("Effect estimate (ratio scale)")
        ax.set_title("Forest plot (supplied estimates; no pooling performed)")
        path=pdir/"forest_plot.png"; save_fig(fig,path); produced.append(path)
    reg=cfg.get("plots",{}).get("regression_coefficients")
    if reg:
        data=pd.read_csv(Path(cfg["_base"])/reg["file"])
        needed=["term","estimate","lower","upper"]
        if not set(needed).issubset(data): raise ValueError("Coefficient data requires term, estimate, lower, upper")
        fig,ax=plt.subplots(figsize=(8,max(3,len(data)*.55))); y=np.arange(len(data))
        ax.errorbar(data.estimate,y,xerr=[data.estimate-data.lower,data.upper-data.estimate],fmt="o",capsize=3)
        ax.axvline(0,linestyle="--"); ax.set_yticks(y,data.term); ax.invert_yaxis()
        ax.set_xlabel("Coefficient (model scale)"); ax.set_title("Regression coefficient plot")
        path=pdir/"regression_coefficients.png"; save_fig(fig,path); produced.append(path)
    roc=cfg.get("plots",{}).get("roc")
    warnings_out=[]
    if roc:
        target,score=roc["outcome"],roc["score"]
        if target not in df or score not in df: raise KeyError("ROC outcome or score column missing")
        y=pd.to_numeric(df[target],errors="coerce"); s=pd.to_numeric(df[score],errors="coerce")
        valid=pd.DataFrame({"y":y,"s":s}).dropna()
        classes=set(valid.y.unique())
        if classes!={0,1}: raise ValueError("ROC outcome must contain both binary classes coded 0 and 1")
        if len(valid)<10: warnings_out.append("ROC based on fewer than 10 complete observations; highly unstable.")
        auc=float(roc_auc_score(valid.y,valid.s)); fpr,tpr,_=roc_curve(valid.y,valid.s)
        fig,ax=plt.subplots(figsize=(6,5)); ax.plot(fpr,tpr,label=f"Apparent AUC = {auc:.3f}"); ax.plot([0,1],[0,1],linestyle="--")
        ax.set(xlabel="1 − Specificity",ylabel="Sensitivity",title="ROC curve (apparent / resubstitution)")
        ax.legend(loc="lower right")
        path=pdir/"roc_curve_apparent.png"; save_fig(fig,path); produced.append(path)
        (out/"roc_summary.json").write_text(json.dumps({"n":len(valid),"auc_apparent":auc,"validation":"none; apparent performance only","warnings":warnings_out},indent=2))
        warnings_out.append("AUC is apparent (same sample used for score evaluation); do not interpret as validated predictive performance.")
    km=cfg.get("plots",{}).get("kaplan_meier")
    if km:
        time_col,event_col=km["time"],km["event"]
        if time_col not in df or event_col not in df: raise KeyError("KM time/event column missing")
        t=pd.to_numeric(df[time_col],errors="coerce"); e=pd.to_numeric(df[event_col],errors="coerce")
        valid=pd.DataFrame({"time":t,"event":e}).dropna()
        if (valid.time<0).any() or not set(valid.event.unique()).issubset({0,1}): raise ValueError("KM requires nonnegative follow-up and event coded 0/1")
        if valid.empty: raise ValueError("No complete observations for Kaplan–Meier")
        times=np.sort(valid.time.unique()); surv=1.0; xs=[0.0]; ys=[1.0]
        for tm in times:
            at_risk=int((valid.time>=tm).sum()); events=int(((valid.time==tm)&(valid.event==1)).sum())
            if at_risk: surv*=1-events/at_risk
            xs.extend([float(tm),float(tm)]); ys.extend([ys[-1],surv])
        fig,ax=plt.subplots(figsize=(7,4)); ax.step(xs,ys,where="post")
        ax.set(xlabel=time_col,ylabel="Estimated survival probability",ylim=(0,1.02),title="Kaplan–Meier estimate (descriptive)")
        path=pdir/"kaplan_meier.png"; save_fig(fig,path); produced.append(path)
        (out/"kaplan_meier_summary.json").write_text(json.dumps({"n":len(valid),"events":int(valid.event.sum()),"censored":int((valid.event==0).sum()),
            "median_followup":float(valid.time.median()),"method":"product-limit estimator","not_included":["confidence intervals","log-rank test","Cox model","competing risks"]},indent=2))
    return produced, warnings_out

def validate_outputs(out: Path) -> dict:
    files=[p for p in out.rglob("*") if p.is_file()]
    issues=[]
    for p in files:
        if p.stat().st_size==0: issues.append(f"Empty output: {p.relative_to(out)}")
        if p.suffix==".png":
            try:
                import matplotlib.image as mpimg
                arr=mpimg.imread(p)
                if arr.size==0: issues.append(f"Unreadable image: {p.relative_to(out)}")
            except Exception as exc: issues.append(f"Image validation failed: {p.name}: {exc}")
    return {"file_count":len(files),"issues":issues,"passed":not issues,
            "files":[{"path":str(p.relative_to(out)),"bytes":p.stat().st_size,"sha256":sha256_file(p)} for p in files]}

def build_reports(df, t1, figs, warnings_out, input_path, cfg, out):
    n=len(df); missing=int(df.isna().sum().sum()); cells=max(1,df.shape[0]*df.shape[1])
    technical=[
        "# Technical analysis report", "", f"- Input: `{input_path.name}`",
        f"- Rows × columns: {df.shape[0]} × {df.shape[1]}",
        f"- Overall missing cells: {missing}/{cells} ({missing/cells*100:.1f}%)",
        f"- Input SHA-256: `{sha256_file(input_path)}`",
        f"- Generated (UTC): {datetime.now(timezone.utc).isoformat()}",
        f"- Figures generated: {len(figs)}", "", "## Table 1", "",
        t1.to_markdown(index=False) if not t1.empty else "No Table 1 variables configured.", "",
        "## Warnings and interpretation limits", ""
    ]
    technical += [f"- {w}" for w in warnings_out] if warnings_out else ["- No pipeline warnings recorded; this does not establish absence of bias or model-assumption violations."]
    technical += ["", "## Reproducibility", "", f"- Pipeline version: {VERSION}",
                  f"- Python: {platform.python_version()}", f"- pandas: {pd.__version__}",
                  "- Configuration: `report_config.json`", "- Figures: `figures/`"]
    (out/"technical_report.md").write_text("\n".join(technical),encoding="utf-8")
    executive=["# Executive summary","",f"This run processed **{n:,} records** and **{df.shape[1]} variables**.",
               f"Overall cell missingness was **{missing/cells*100:.1f}%**. The pipeline generated **{len(figs)} figures**.",
               "", "## Key caveats",""]
    executive += [f"- {w}" for w in warnings_out] if warnings_out else ["- Descriptive outputs do not establish causality or clinical effectiveness."]
    executive += ["","This report describes the supplied dataset and configured analyses. It is not a clinical recommendation or proof of generalizability."]
    (out/"executive_summary.md").write_text("\n".join(executive),encoding="utf-8")

def run(input_path: Path, config_path: Path, output: Path) -> dict:
    cfg=json.loads(config_path.read_text(encoding="utf-8"))
    cfg["_base"]=str(config_path.parent)
    df=load_data(input_path)
    output.mkdir(parents=True,exist_ok=True)
    t1=table1(df,cfg); t1.to_csv(output/"table1.csv",index=False)
    figs,warns=make_plots(df,cfg,output)
    build_reports(df,t1,figs,warns,input_path,cfg,output)
    (output/"report_config.json").write_text(json.dumps({k:v for k,v in cfg.items() if k!="_base"},indent=2),encoding="utf-8")
    manifest={"version":VERSION,"generated_utc":datetime.now(timezone.utc).isoformat(),"input":str(input_path),
              "input_sha256":sha256_file(input_path),"rows":len(df),"columns":len(df.columns),
              "figures":[str(p.relative_to(output)) for p in figs],"warnings":warns,
              "validation":validate_outputs(output)}
    (output/"evidence_manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
    if not manifest["validation"]["passed"]: raise RuntimeError("Output validation failed; see evidence_manifest.json")
    return manifest

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input",required=True); ap.add_argument("--config",required=True); ap.add_argument("--output",required=True)
    args=ap.parse_args()
    result=run(Path(args.input),Path(args.config),Path(args.output))
    print(json.dumps({"status":"success","output":args.output,"rows":result["rows"],"figures":len(result["figures"]),"validation":result["validation"]["passed"]},indent=2))
if __name__=="__main__": main()
