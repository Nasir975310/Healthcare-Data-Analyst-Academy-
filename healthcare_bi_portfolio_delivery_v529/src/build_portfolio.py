#!/usr/bin/env python3
"""Build deterministic synthetic hospital BI portfolio outputs using stdlib only."""
import csv,json,hashlib,argparse
from pathlib import Path
from collections import Counter,defaultdict

def rows(p):
    with p.open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f))
def build(data_dir,out_dir):
    d=Path(data_dir); o=Path(out_dir); o.mkdir(parents=True,exist_ok=True)
    patients=rows(d/'patients.csv'); encounters=rows(d/'encounters.csv'); obs=rows(d/'observations.csv'); meds=rows(d/'medications.csv')
    pids={r['PatientID'] for r in patients}; eids={r['EncounterID'] for r in encounters}
    issues=[]
    for file,key,rs in [('patients','PatientID',patients),('encounters','EncounterID',encounters),('observations','ObservationID',obs),('medications','MedicationID',meds)]:
        vals=[r[key] for r in rs]
        if len(vals)!=len(set(vals)):issues.append(f'duplicate {key}')
    for r in encounters:
        if r['PatientID'] not in pids:issues.append('encounter references unknown patient '+r['EncounterID'])
    for r in obs+meds:
        if r['EncounterID'] not in eids:issues.append('fact references unknown encounter '+r.get('ObservationID',r.get('MedicationID','?')))
    if issues: raise ValueError('; '.join(issues))
    by_month=Counter(r['EncounterDate'][:7] for r in encounters)
    by_type=Counter(r['EncounterType'] for r in encounters)
    by_class=Counter(r['DrugClass'] for r in meds)
    bp=defaultdict(list)
    for r in obs: bp[r['Measure']].append(float(r['Value']))
    metrics={'patients':len(patients),'encounters':len(encounters),'completed_encounters':sum(r['Status']=='Completed' for r in encounters),'observations':len(obs),'medication_orders':len(meds),'mean_systolic_bp':round(sum(bp['Systolic BP'])/len(bp['Systolic BP']),2),'mean_diastolic_bp':round(sum(bp['Diastolic BP'])/len(bp['Diastolic BP']),2),'encounters_by_month':dict(sorted(by_month.items())),'encounters_by_type':dict(sorted(by_type.items())),'medication_orders_by_class':dict(sorted(by_class.items())),'synthetic_only':True}
    hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(d.glob('*.csv'))}
    report={'status':'PASS','checks':{'unique_primary_keys':True,'encounter_patient_references':True,'fact_encounter_references':True,'synthetic_data_only':True},'metrics':metrics,'source_sha256':hashes}
    (o/'portfolio_metrics.json').write_text(json.dumps(metrics,indent=2)+'\n')
    (o/'data_quality_report.json').write_text(json.dumps(report,indent=2)+'\n')
    with (o/'monthly_encounters.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['Month','Encounters']);w.writerows(sorted(by_month.items()))
    with (o/'medication_class_mix.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['DrugClass','MedicationOrders']);w.writerows(sorted(by_class.items()))
    return report
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--data',default=str(Path(__file__).resolve().parents[1]/'data'));p.add_argument('--out',default=str(Path(__file__).resolve().parents[1]/'reports'));a=p.parse_args();r=build(a.data,a.out);print(json.dumps(r,indent=2))
