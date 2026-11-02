import argparse, csv, json
from collections import Counter
from pathlib import Path

def summarize(path):
    with Path(path).open(newline='',encoding='utf-8-sig') as f:
        rows=list(csv.DictReader(f))
    statuses=Counter((r.get('status') or '').strip().lower() for r in rows)
    submitted=sum(1 for r in rows if (r.get('status') or '').strip().lower() not in ('','planned','draft','withdrawn'))
    responses=sum(v for k,v in statuses.items() if k in ('screening','assessment','interview','offer','rejected'))
    interviews=statuses.get('interview',0)
    offers=statuses.get('offer',0)
    return {'tracked_rows':len(rows),'status_counts':dict(sorted(statuses.items())),
            'applications_submitted_estimate':submitted,'responses_status_count':responses,
            'interview_status_count':interviews,'offer_status_count':offers,
            'response_per_submitted_percent':round(responses/submitted*100,1) if submitted else None,
            'interview_per_submitted_percent':round(interviews/submitted*100,1) if submitted else None,
            'caveat':'Counts are based on one current status per row; statuses are not event history. For funnel conversion, store dated status events and use cohort-based denominators.'}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--input',required=True)
    a=p.parse_args()
    print(json.dumps(summarize(a.input),indent=2))
