"""Standardise synthetic hospital CSV extracts and produce quality/reconciliation outputs.
Run from the interoperability folder:
python scripts/standardise_clinical_data.py
"""
from pathlib import Path
import csv, json, hashlib
BASE=Path(__file__).resolve().parents[1]
DATA=BASE/"data"; OUT=BASE/"reports"; OUT.mkdir(exist_ok=True)
def load(name):
    with (DATA/name).open(newline="",encoding="utf-8") as f: return list(csv.DictReader(f))
def write(name, rows):
    if not rows: return
    with (OUT/name).open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
patients=load("patients.csv"); encounters=load("encounters.csv")
meds=load("medication_orders.csv"); labs=load("lab_observations.csv")
patient_ids={x["source_patient_id"] for x in patients}
encounter_ids={x["source_encounter_id"] for x in encounters}
issues=[]
def unique(rows,key,table):
    seen=set()
    for i,row in enumerate(rows,2):
        value=row.get(key,"")
        if not value or value in seen: issues.append({"table":table,"row":i,"issue":"missing_or_duplicate_key","field":key,"value":value})
        seen.add(value)
for name,rows,key in [("patients",patients,"source_patient_id"),("encounters",encounters,"source_encounter_id"),("medication_orders",meds,"source_order_id"),("lab_observations",labs,"source_observation_id")]:
    unique(rows,key,name)
for row in encounters:
    if row["source_patient_id"] not in patient_ids: issues.append({"table":"encounters","row":row["source_encounter_id"],"issue":"orphan_patient_reference","field":"source_patient_id","value":row["source_patient_id"]})
    if row["end_date"] < row["start_date"]: issues.append({"table":"encounters","row":row["source_encounter_id"],"issue":"invalid_chronology","field":"end_date","value":row["end_date"]})
for table,rows in [("medication_orders",meds),("lab_observations",labs)]:
    for row in rows:
        if row["source_encounter_id"] not in encounter_ids: issues.append({"table":table,"row":row.get("source_order_id",row.get("source_observation_id")),"issue":"orphan_encounter_reference","field":"source_encounter_id","value":row["source_encounter_id"]})
# Curated rows preserve source identifiers and original clinical terminology.
curated_enc=[{"encounter_id":r["source_encounter_id"],"patient_id":r["source_patient_id"],"encounter_class":r["class_code"],"status":r["status"],"start_date":r["start_date"],"end_date":r["end_date"],"department":r["department"],"source_system":"SYNTH_HOSPITAL"} for r in encounters]
curated_med=[{"medication_order_id":r["source_order_id"],"encounter_id":r["source_encounter_id"],"patient_id":r["source_patient_id"],"drug_display":r["drug_name"],"atc_code":r["atc_code"],"route":r["route"],"status":r["status"],"authored_on":r["authored_on"],"quantity":r["quantity"],"source_system":"SYNTH_PHARMACY"} for r in meds]
curated_lab=[{"observation_id":r["source_observation_id"],"encounter_id":r["source_encounter_id"],"patient_id":r["source_patient_id"],"test_display":r["test_name"],"loinc_code":r["loinc_code"],"value":r["value"],"unit":r["unit"],"effective_date":r["effective_date"],"status":r["status"],"source_system":"SYNTH_LAB"} for r in labs]
write("curated_encounters.csv",curated_enc);write("curated_medication_orders.csv",curated_med);write("curated_lab_observations.csv",curated_lab)
for row in patients:
    if row["administrative_sex"] not in {"F","M","U"}: issues.append({"table":"patients","row":row["source_patient_id"],"issue":"unexpected_administrative_sex_code","field":"administrative_sex","value":row["administrative_sex"]})
summary={"synthetic_only":True,"source_counts":{"patients":len(patients),"encounters":len(encounters),"medication_orders":len(meds),"lab_observations":len(labs)},"curated_counts":{"encounters":len(curated_enc),"medication_orders":len(curated_med),"lab_observations":len(curated_lab)},"quality_issue_count":len(issues),"quality_issues":issues,"reference_checks":{"encounter_patient_orphans":sum(1 for x in issues if x["issue"]=="orphan_patient_reference"),"child_encounter_orphans":sum(1 for x in issues if x["issue"]=="orphan_encounter_reference")},"source_sha256":{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(DATA.glob("*.csv"))}}
(OUT/"quality_reconciliation_report.json").write_text(json.dumps(summary,indent=2))
with (OUT/"quality_issues.csv").open("w",newline="",encoding="utf-8") as f:
    cols=["table","row","issue","field","value"];w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(issues)
print(json.dumps({k:v for k,v in summary.items() if k!="quality_issues"},indent=2))
