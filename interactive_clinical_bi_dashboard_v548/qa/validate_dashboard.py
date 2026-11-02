#!/usr/bin/env python3
"""Independent reference implementation for the v5.49 clinical BI dashboard."""
from __future__ import annotations
import argparse, csv, json, math
from pathlib import Path
FIELDS = ("diabetes", "ckd", "ischemic_heart_disease")
def valid_class(v): return v is not None and str(v).strip() != "" and str(v).lower() != "none"
def flag(v):
    if v is True or v == 1 or str(v).lower() == "yes": return True
    if v is False or v == 0 or str(v).lower() == "no": return False
    return None
def comorbidity(row):
    vals=[flag(row.get(k)) for k in FIELDS]
    if True in vals: return True
    if all(v is False for v in vals): return False
    return None
def age_band(v):
    try: n=float(v)
    except (TypeError, ValueError): return None
    if not math.isfinite(n): return None
    return "18–39" if n < 40 else "40–59" if n < 60 else "60+"
def plausible(v):
    try: n=float(v)
    except (TypeError, ValueError): return False
    return math.isfinite(n) and 70 <= n <= 250
def filtered(rows, drug="", sex="", age="", co=""):
    out=[]
    for r in rows:
        if drug and r.get("primary_drug_class") != drug: continue
        if sex and str(r.get("sex") or "") != sex: continue
        if age and age_band(r.get("age_years")) != age: continue
        c=comorbidity(r)
        if co == "yes" and c is not True: continue
        if co == "no" and c is not False: continue
        out.append(r)
    return out
def metrics(rows):
    pairs=[r for r in rows if valid_class(r.get("primary_drug_class")) and plausible(r.get("baseline_sbp_mmhg")) and plausible(r.get("followup_sbp_mmhg"))]
    base=[float(r["baseline_sbp_mmhg"]) for r in pairs]; follow=[float(r["followup_sbp_mmhg"]) for r in pairs]
    mean=lambda a: sum(a)/len(a) if a else None
    ids={r.get("record_id") for r in rows}
    return {"filtered_records":len(rows),"unique_record_ids":len(ids),"paired_sbp_records":len(pairs),"mean_baseline_sbp":mean(base),"mean_followup_sbp":mean(follow),"mean_paired_sbp_change":mean([b-f for b,f in zip(base,follow)]),"duplicate_excess":len(rows)-len(ids),"missing_followup_sbp":sum(r.get("followup_sbp_mmhg") in (None,"") for r in rows),"implausible_followup_sbp":sum(r.get("followup_sbp_mmhg") not in (None,"") and not plausible(r.get("followup_sbp_mmhg")) for r in rows),"missing_primary_class":sum(not valid_class(r.get("primary_drug_class")) for r in rows)}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--data',default='../data/dashboard_data.json'); ap.add_argument('--output',default='reconciliation.json'); args=ap.parse_args()
    here=Path(__file__).resolve().parent; rows=json.loads((here/args.data).resolve().read_text())
    drugs=sorted({r.get('primary_drug_class') for r in rows if valid_class(r.get('primary_drug_class'))})
    sexes=sorted({r.get('sex') for r in rows if r.get('sex')})
    combos=[({},'all')]
    combos += [({'drug':d},f'drug={d}') for d in drugs]
    combos += [({'sex':x},f'sex={x}') for x in sexes]
    combos += [({'age':a},f'age={a}') for a in ('18–39','40–59','60+')]
    combos += [({'co':c},f'comorbidity={c}') for c in ('yes','no')]
    combos += [({'drug':d,'sex':x,'age':a,'co':c},f'{d}|{x}|{a}|{c}') for d in drugs for x in sexes for a in ('18–39','40–59','60+') for c in ('yes','no')]
    cases=[{"label":label,"filters":f,"metrics":metrics(filtered(rows,**f))} for f,label in combos]
    out={"release":"5.49.0","dataset":"synthetic","source_rows":len(rows),"cases":cases}
    (here/args.output).write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
    print(f"Generated {len(cases)} filter reconciliation cases from {len(rows)} rows: {here/args.output}")
if __name__=='__main__': main()
