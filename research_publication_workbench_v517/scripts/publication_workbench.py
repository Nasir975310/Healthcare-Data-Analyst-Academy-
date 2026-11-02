#!/usr/bin/env python3
"""Generate research publication tables, participant-flow diagrams and reporting checklists.

Requires Python 3.10+, pandas and scipy. Outputs are drafts; verify all values and
reporting items against the approved protocol, source records and journal guidance.
"""
from __future__ import annotations
import argparse, csv, json, math, re, hashlib
from pathlib import Path
from datetime import datetime, timezone
import pandas as pd
from scipy import stats

def esc(s):
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def fmt_mean_sd(x):
    s=pd.to_numeric(pd.Series(x),errors="coerce").dropna()
    return f"{s.mean():.1f} ± {s.std(ddof=1):.1f}" if len(s)>1 else (f"{s.iloc[0]:.1f}" if len(s)==1 else "—")

def fmt_median_iqr(x):
    s=pd.to_numeric(pd.Series(x),errors="coerce").dropna()
    return f"{s.median():.1f} ({s.quantile(.25):.1f}–{s.quantile(.75):.1f})" if len(s) else "—"

def build_table1(df,group,continuous,categorical,continuous_summary="mean_sd"):
    if group not in df: raise ValueError(f"Group column '{group}' not found.")
    groups=list(df[group].dropna().astype(str).unique())
    if len(groups)<2: raise ValueError("Table 1 requires at least two non-missing groups.")
    rows=[]
    for col in continuous:
        if col not in df: raise ValueError(f"Variable '{col}' not found.")
        vals=[pd.to_numeric(df.loc[df[group].astype(str)==g,col],errors="coerce").dropna() for g in groups]
        formatter=fmt_mean_sd if continuous_summary=="mean_sd" else fmt_median_iqr
        rows.append({"variable":col,"level":"","type":continuous_summary,
            **{g:formatter(v) for g,v in zip(groups,vals)},
            "missing_n":int(pd.to_numeric(df[col],errors="coerce").isna().sum()),"p_value":""})
    for col in categorical:
        if col not in df: raise ValueError(f"Variable '{col}' not found.")
        tab=pd.crosstab(df[group].astype(str),df[col].fillna("Missing").astype(str))
        for level in sorted(df[col].fillna("Missing").astype(str).unique()):
            row={"variable":col,"level":level,"type":"n (%)",
                "missing_n":int(df[col].isna().sum()),"p_value":""}
            for g in groups:
                denom=int((df[group].astype(str)==g).sum())
                n=int(tab.loc[g,level]) if g in tab.index and level in tab.columns else 0
                row[g]=f"{n} ({100*n/denom:.1f}%)" if denom else "—"
            rows.append(row)
    out=pd.DataFrame(rows)
    return out,groups

def add_group_tests(df,table,group,continuous,categorical,continuous_tests=None,categorical_test="chi_square"):
    groups=list(df[group].dropna().astype(str).unique())
    if len(groups)!=2: return table
    for col in continuous:
        a=pd.to_numeric(df.loc[df[group].astype(str)==groups[0],col],errors="coerce").dropna()
        b=pd.to_numeric(df.loc[df[group].astype(str)==groups[1],col],errors="coerce").dropna()
        if len(a)>1 and len(b)>1:
            test=(continuous_tests or {}).get(col,"welch")
            if test=="welch": p=stats.ttest_ind(a,b,equal_var=False).pvalue
            elif test=="mann_whitney": p=stats.mannwhitneyu(a,b,alternative="two-sided").pvalue
            else: raise ValueError(f"Unsupported continuous test for {col}: {test}")
            table.loc[table.variable==col,"p_value"]=f"{p:.4f}"
    for col in categorical:
        tab=pd.crosstab(df[group].astype(str),df[col].fillna("Missing").astype(str))
        if tab.shape[0]>=2 and tab.shape[1]>=2:
            if categorical_test=="chi_square":
                p=stats.chi2_contingency(tab,correction=False).pvalue
            else: raise ValueError("Only chi_square is implemented; choose exact methods separately for sparse tables.")
            # Put the variable-level p-value on the first row only.
            ix=table.index[table.variable==col]
            if len(ix): table.loc[ix[0],"p_value"]=f"{p:.4f}"
    return table

def consort_svg(enrolled,allocated_i,allocated_c,received_i,received_c,completed_i,completed_c,analysed_i,analysed_c):
    vals=[enrolled,allocated_i,allocated_c,received_i,received_c,completed_i,completed_c,analysed_i,analysed_c]
    if any(x<0 for x in vals): raise ValueError("Flow counts cannot be negative.")
    if allocated_i+allocated_c>enrolled: raise ValueError("Allocated participants cannot exceed enrolled participants.")
    if received_i>allocated_i or received_c>allocated_c or completed_i>received_i or completed_c>received_c or analysed_i>allocated_i or analysed_c>allocated_c:
        raise ValueError("Flow counts must be logically nested (received ≤ allocated; completed ≤ received; analysed ≤ allocated).")
    boxes=[
      (30,20,520,64,f"Assessed for eligibility: {enrolled}"),
      (30,112,245,76,f"Allocated to intervention: {allocated_i}",f"Received: {received_i}"),
      (305,112,245,76,f"Allocated to control: {allocated_c}",f"Received: {received_c}"),
      (30,224,245,76,f"Completed follow-up: {completed_i}",f"Analysed: {analysed_i}"),
      (305,224,245,76,f"Completed follow-up: {completed_c}",f"Analysed: {analysed_c}")]
    svg=['<svg xmlns="http://www.w3.org/2000/svg" width="580" height="330" viewBox="0 0 580 330">',
         '<style>text{font:14px sans-serif;fill:#172b3a}.box{fill:#f4f7fa;stroke:#47647a;stroke-width:1.5}.line{stroke:#47647a;stroke-width:1.5;fill:none}</style>']
    for x,y,w,h,*lines in boxes:
        svg.append(f'<rect class="box" x="{x}" y="{y}" width="{w}" height="{h}" rx="8"/>')
        for i,line in enumerate(lines):
            svg.append(f'<text x="{x+w/2}" y="{y+28+i*24}" text-anchor="middle">{esc(line)}</text>')
    svg += ['<path class="line" d="M290 84 V98 H152 V112 M290 98 H427 V112"/>',
            '<path class="line" d="M152 188 V224 M427 188 V224"/>',
            '<text x="290" y="315" text-anchor="middle" font-size="11">Draft participant flow — complete exclusion and loss reasons before publication</text>',
            '</svg>']
    return "\\n".join(svg)

def prisma_svg(records,duplicates,screened,excluded,fulltext,fulltext_excluded,included):
    vals=[records,duplicates,screened,excluded,fulltext,fulltext_excluded,included]
    if any(x<0 for x in vals): raise ValueError("PRISMA counts cannot be negative.")
    if duplicates>records or screened>records-duplicates or excluded>screened or fulltext>screened-excluded or fulltext_excluded>fulltext or included>fulltext-fulltext_excluded:
        raise ValueError("PRISMA counts are inconsistent. Check each stage denominator.")
    stages=[("Records identified",records),("Duplicates removed",duplicates),("Records screened",screened),
            ("Records excluded",excluded),("Reports sought for retrieval",fulltext),
            ("Reports excluded after full-text review",fulltext_excluded),("Studies included",included)]
    svg=['<svg xmlns="http://www.w3.org/2000/svg" width="720" height="560" viewBox="0 0 720 560">',
         '<style>text{font:14px sans-serif;fill:#172b3a}.box{fill:#f4f7fa;stroke:#47647a;stroke-width:1.5}.line{stroke:#47647a;stroke-width:1.5;fill:none}</style>']
    y=15
    for label,n in stages:
        svg.append(f'<rect class="box" x="125" y="{y}" width="470" height="55" rx="8"/>')
        svg.append(f'<text x="360" y="{y+23}" text-anchor="middle">{esc(label)}</text>')
        svg.append(f'<text x="360" y="{y+43}" text-anchor="middle">n = {n}</text>')
        if y<430: svg.append(f'<path class="line" d="M360 {y+55} V{y+75}"/>')
        y+=75
    svg.append('</svg>')
    return "\\n".join(svg)

def parse_ris(path):
    records=[]; cur={}
    for line in path.read_text(encoding="utf-8",errors="replace").splitlines():
        if line.strip()=="ER  -":
            if cur: records.append(cur); cur={}
            continue
        m=re.match(r"^([A-Z0-9]{2})  - (.*)$",line)
        if m:
            key,val=m.groups(); cur.setdefault(key,[]).append(val)
    if cur: records.append(cur)
    return records

def write_bibliography(records,outdir):
    outdir.mkdir(parents=True,exist_ok=True)
    rows=[]
    for i,r in enumerate(records,1):
        rows.append({"id":i,"type":(r.get("TY",[""])[0]),"authors":"; ".join(r.get("AU",[])),
            "year":(r.get("PY",[""])[0]),"title":" ".join(r.get("TI",r.get("T1",[""]))),
            "journal":" ".join(r.get("JO",r.get("JF",[""]))),"doi":(r.get("DO",[""])[0]),
            "url":(r.get("UR",[""])[0])})
    pd.DataFrame(rows).to_csv(outdir/"references.csv",index=False)
    bib=[]
    for r in rows:
        key=re.sub(r"[^A-Za-z0-9]","",((r["authors"].split(";")[0] if r["authors"] else "ref").split(",")[0])+r["year"]+str(r["id"]))
        bib += [f"@article{{{key},",f"  author = {{{r['authors']}}},",f"  title = {{{r['title']}}},",
                f"  journal = {{{r['journal']}}},",f"  year = {{{r['year']}}},",f"  doi = {{{r['doi']}}}", "}", ""]
    (outdir/"references.bib").write_text("\\n".join(bib),encoding="utf-8")
    return rows

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input",type=Path,required=True); p.add_argument("--outdir",type=Path,default=Path("outputs"))
    p.add_argument("--group",default="arm"); p.add_argument("--continuous",default="age,bmi,baseline_sbp,followup_sbp")
    p.add_argument("--categorical",default="sex,diabetes,adherent"); p.add_argument("--summary",choices=["mean_sd","median_iqr"],default="mean_sd")
    p.add_argument("--consort-counts",type=int,nargs=9,metavar=("ASSESSED","ALLOC_I","ALLOC_C","RECEIVED_I","RECEIVED_C","COMPLETE_I","COMPLETE_C","ANALYSED_I","ANALYSED_C"))
    p.add_argument("--prisma-counts",type=int,nargs=7,metavar=("RECORDS","DUPLICATES","SCREENED","EXCLUDED","FULLTEXT","FULLTEXT_EXCLUDED","INCLUDED"))
    p.add_argument("--ris",type=Path)
    a=p.parse_args(); df=pd.read_csv(a.input); a.outdir.mkdir(parents=True,exist_ok=True)
    cont=[x.strip() for x in a.continuous.split(",") if x.strip()]
    cat=[x.strip() for x in a.categorical.split(",") if x.strip()]
    table,groups=build_table1(df,a.group,cont,cat,a.summary)
    table=add_group_tests(df,table,a.group,cont,cat)
    table.to_csv(a.outdir/"table1_baseline_characteristics.csv",index=False)
    table.to_html(a.outdir/"table1_baseline_characteristics.html",index=False,border=0)
    flow=[]
    if a.consort_counts:
        svg=consort_svg(*a.consort_counts); (a.outdir/"consort_flow.svg").write_text(svg,encoding="utf-8"); flow.append("consort_flow.svg")
    if a.prisma_counts:
        svg=prisma_svg(*a.prisma_counts); (a.outdir/"prisma_flow.svg").write_text(svg,encoding="utf-8"); flow.append("prisma_flow.svg")
    refs=write_bibliography(parse_ris(a.ris),a.outdir) if a.ris else []
    manifest={"source_file":a.input.name,"source_sha256":hashlib.sha256(a.input.read_bytes()).hexdigest(),
      "rows":len(df),"group_column":a.group,"groups":groups,"continuous_variables":cont,
      "categorical_variables":cat,"summary_method":a.summary,"generated_utc":datetime.now(timezone.utc).isoformat(),
      "outputs":["table1_baseline_characteristics.csv","table1_baseline_characteristics.html"]+flow+
        (["references.csv","references.bib"] if a.ris else []),
      "warnings":["P-values are exploratory unless analysis methods and comparisons were prespecified.",
       "Chi-square may be unsuitable with sparse expected cell counts; use an appropriate exact method after review.",
       "Table 1 conventions vary; many journals discourage baseline significance testing.",
       "Participant flow counts are user-entered and must be reconciled to source records.",
       "Bibliography parsing is basic RIS ingestion; verify author names, title, year, journal and DOI."]}
    (a.outdir/"publication_manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
    print(json.dumps({"rows":len(df),"groups":groups,"outputs":manifest["outputs"],"references_imported":len(refs)},indent=2))
if __name__=="__main__": main()
