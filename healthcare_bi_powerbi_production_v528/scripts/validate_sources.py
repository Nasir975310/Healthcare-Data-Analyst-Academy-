#!/usr/bin/env python3
"""Validate and summarize the synthetic Power BI source bundle."""
import csv,json,hashlib,argparse
from pathlib import Path
EXPECTED={'patients.csv':['PatientID','Gender','BirthDate','Residence','Region'],'encounters.csv':['EncounterID','PatientID','EncounterDate','EncounterType','Status'],'observations.csv':['ObservationID','EncounterID','Measure','Value','Unit'],'medications.csv':['MedicationID','EncounterID','Medication','DrugClass','IsActive']}
def read(p):
 with p.open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f))
def validate(folder):
 p=Path(folder);data={n:read(p/n) for n in EXPECTED};issues=[]
 for n,cols in EXPECTED.items():
  if not data[n] or list(data[n][0])!=cols:issues.append(f'{n}: missing rows or unexpected columns')
 for n,key in [('patients.csv','PatientID'),('encounters.csv','EncounterID'),('observations.csv','ObservationID'),('medications.csv','MedicationID')]:
  ids=[r[key] for r in data[n]]
  if len(ids)!=len(set(ids)):issues.append(f'{n}: duplicate {key}')
 pids={r['PatientID'] for r in data['patients.csv']};eids={r['EncounterID'] for r in data['encounters.csv']}
 for r in data['encounters.csv']:
  if r['PatientID'] not in pids:issues.append(f"Encounter {r['EncounterID']} has unknown patient")
 for n in ['observations.csv','medications.csv']:
  for r in data[n]:
   if r['EncounterID'] not in eids:issues.append(f"{n} row {next(iter(r.values()))} has unknown encounter")
 for r in data['observations.csv']:
  try:float(r['Value'])
  except:issues.append(f"Observation {r['ObservationID']} has nonnumeric Value")
 hashes={n:hashlib.sha256((p/n).read_bytes()).hexdigest() for n in EXPECTED}
 return {'status':'PASS' if not issues else 'FAIL','counts':{n:len(v) for n,v in data.items()},'issues':issues,'sha256':hashes,'synthetic_only':True}
def main():
 a=argparse.ArgumentParser();a.add_argument('--data-dir',default=str(Path(__file__).resolve().parents[1]/'data'));a.add_argument('--output',default='qa_report.json');x=a.parse_args();r=validate(x.data_dir);Path(x.output).write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2));raise SystemExit(0 if r['status']=='PASS' else 1)
if __name__=='__main__':main()
