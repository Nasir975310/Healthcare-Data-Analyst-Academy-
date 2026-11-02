from pathlib import Path
import csv, json, html
BASE=Path(__file__).resolve().parent
OUT=BASE/"dashboards"; OUT.mkdir(exist_ok=True)
RESULTS=BASE.parent/"outputs"
def rows(path):
    with path.open(newline="",encoding="utf-8") as f: return list(csv.DictReader(f))
def card(label,value,sub=""):
    return f'<div class="kpi"><span>{html.escape(label)}</span><strong>{html.escape(str(value))}</strong><small>{html.escape(sub)}</small></div>'
def bar_chart(items,title,key="value"):
    maxv=max([float(x[key]) for x in items] or [1]) or 1
    bars="".join(f'<div class="barrow"><label>{html.escape(str(x["label"]))}</label><div class="track"><i style="width:{float(x[key])/maxv*100:.1f}%"></i></div><b>{float(x[key]):,.1f}</b></div>' for x in items)
    return f'<section><h2>{html.escape(title)}</h2>{bars}</section>'
def page(title,subtitle,kpis,sections,warning):
    css="""*{box-sizing:border-box}body{margin:0;background:#f3f6fa;color:#172b4d;font:15px/1.5 system-ui,sans-serif}main{max-width:1100px;margin:auto;padding:28px}header{background:#102a43;color:white;padding:28px;border-radius:16px}h1{margin:0 0 8px;font-size:30px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin:18px 0}.kpi,section,.warning{background:white;border:1px solid #d9e2ec;border-radius:12px;padding:18px;margin:14px 0}.kpi span,.kpi small{display:block;color:#627d98}.kpi strong{font-size:28px;display:block;margin:5px 0}h2{font-size:19px;margin:0 0 15px}.barrow{display:grid;grid-template-columns:150px 1fr 65px;gap:10px;align-items:center;margin:12px 0}.track{height:12px;background:#e6edf5;border-radius:10px;overflow:hidden}.track i{display:block;height:100%;background:#247ba0;border-radius:10px}.warning{border-left:5px solid #d97706;background:#fffaf0}footer{color:#627d98;font-size:12px;margin:24px 0}@media(max-width:600px){main{padding:14px}.barrow{grid-template-columns:105px 1fr 52px;font-size:12px}}"""
    return f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><style>{css}</style><main><header><h1>{html.escape(title)}</h1><div>{html.escape(subtitle)}</div></header><div class="grid">{"".join(kpis)}</div>{"".join(sections)}<div class="warning"><b>Interpretation and data boundary</b><p>{html.escape(warning)}</p></div><footer>Generated from deterministic synthetic training data. Not for clinical or operational decisions. Build script: scripts_dashboard_build.py</footer></main></html>'
ops=json.loads((RESULTS/"operations_summary.json").read_text())
dept=rows(RESULTS/"operations_department_kpis.csv")
ops_sections=[bar_chart([{"label":r["department"],"value":r["encounters"]} for r in dept],"Encounter volume by department"),bar_chart([{"label":r["department"],"value":r["mean_los_days"]} for r in dept],"Mean length of stay (days)")]
(OUT/"hospital_operations_dashboard.html").write_text(page("Hospital Operations Performance","Synthetic encounter-level performance view",[card("Source encounter rows",ops["source_rows"]),card("Unique patients",ops["unique_patients"],"Not encounter count"),card("Mean LOS",ops["mean_los_days"],"Days"),card("Supplied flag rate",str(ops["supplied_flag_rate_pct"])+"%","Unvalidated synthetic flag")],ops_sections,"All records are fabricated. The supplied readmission flag is not validated against a time-window and subsequent-encounter definition. Department means are descriptive; do not infer quality or efficiency without case-mix and operational context."))
due=rows(RESULTS/"due_group_summary.csv"); classes=rows(RESULTS/"due_class_counts.csv")
due_sections=[bar_chart([{"label":"Treated" if r["prescribed_any_antihypertensive"]=="1" else "Not treated","value":r["followup_mean_sbp"]} for r in due],"Mean follow-up systolic BP (mmHg)"),bar_chart([{"label":r["antihypertensive_class"],"value":r["patients"]} for r in classes],"Cohort records by recorded class")]
treated=next(r["n"] for r in due if r["prescribed_any_antihypertensive"]=="1"); untreated=next(r["n"] for r in due if r["prescribed_any_antihypertensive"]=="0")
(OUT/"antihypertensive_due_dashboard.html").write_text(page("Antihypertensive DUE Descriptive Dashboard","Synthetic observational cohort · prescribing and paired BP descriptions",[card("Cohort records",500),card("Treated group",treated),card("Untreated group",untreated),card("Paired BP records",500)],due_sections,"These are synthetic observational data. Group differences are unadjusted descriptive associations, not causal treatment effects. Prescription does not establish dispensing, administration, ingestion, persistence or adherence."))
pv=rows(RESULTS/"pv_descriptive_counts.csv"); agg={}
for r in pv: agg[r["suspect_drug"]]=agg.get(r["suspect_drug"],0)+int(r["case_records"])
pvq=rows(RESULTS/"pv_quality_log.csv")
pv_sections=[bar_chart([{"label":k,"value":v} for k,v in sorted(agg.items())],"Case records by suspect drug"),bar_chart([{"label":r["check"],"value":r["rows"]} for r in pvq],"Quality-review counts")]
(OUT/"pharmacovigilance_quality_dashboard.html").write_text(page("Pharmacovigilance Case Quality","Synthetic case register · completeness, chronology and review workload",[card("Case records",240),card("Duplicate candidates",3,"Manual review required"),card("Missing case IDs",0),card("Chronology exceptions",0)],pv_sections,"Case records do not estimate incidence or risk. Duplicate candidates are not confirmed duplicates. Seriousness is distinct from severity. No causality, expectedness, signal detection or regulatory assessment is performed."))
