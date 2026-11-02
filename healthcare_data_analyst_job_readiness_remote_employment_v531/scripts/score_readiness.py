"""Score a candidate's self-assessment against the v5.31 rubric."""
from pathlib import Path
import argparse, json
ROOT=Path(__file__).resolve().parents[1]
RUBRIC=json.loads((ROOT/"data/assessment_rubric.json").read_text(encoding="utf-8"))
ACTIONS={
"excel":"Practice cleaning, pivots, lookups and reconciliation on a fresh workbook.",
"sql":"Write joins, CTEs, window functions and orphan/duplicate checks; explain table grain.",
"python":"Build a pandas ingestion-to-validation script with logged exceptions and reproducible outputs.",
"bi":"Model a star schema, write explicit DAX measures, test filter context and document RLS.",
"clinical":"Review clinical data grain, units, provenance, privacy and limits of interpretation.",
"statistics":"Practice test selection, assumptions, effect sizes, confidence intervals and confounding.",
"communication":"Write a one-page executive summary and a concise stakeholder status update.",
"professional":"Practice scoped delivery, version control, secure handling and asynchronous updates."
}
def score(payload):
    scores=payload.get("scores",{})
    missing=[s["id"] for s in RUBRIC["sections"] if s["id"] not in scores]
    unknown=sorted(set(scores)-{s["id"] for s in RUBRIC["sections"]})
    if missing or unknown: raise ValueError(f"Missing sections: {missing}; unknown sections: {unknown}")
    total=0.0; details=[]
    for section in RUBRIC["sections"]:
        value=scores[section["id"]]
        if isinstance(value,bool) or not isinstance(value,(int,float)) or not 0<=value<=section["max_score"]:
            raise ValueError(f"{section['id']} must be a number from 0 to {section['max_score']}")
        weighted=value*section["weight"]/100
        total+=weighted
        details.append({"id":section["id"],"name":section["name"],"raw_score":value,
                        "weight":section["weight"],"weighted_points":round(weighted,2),
                        "action":ACTIONS[section["id"]] if value<75 else "Maintain proficiency with a timed practical task."})
    privacy=bool(payload.get("privacy_or_integrity_breach",False))
    if total>=85: band="Strong portfolio readiness"
    elif total>=70: band="Developing job readiness"
    elif total>=55: band="Foundational; targeted practice required"
    else: band="Early-stage; build core evidence first"
    if privacy: band="Not ready for client data access — resolve privacy/integrity failure"
    return {"assessment":"v5.31.0","weighted_score":round(total,2),"band":band,
            "privacy_or_integrity_breach":privacy,"section_results":details,
            "priority_gaps":[d for d in details if d["raw_score"]<70],
            "interpretation":"Self-assessment only; not a hiring prediction, credential or proof of independent competence."}
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("input",help="JSON file with scores keyed by rubric section id")
    ap.add_argument("--output",default=str(ROOT/"reports/readiness_result.json"))
    args=ap.parse_args()
    payload=json.loads(Path(args.input).read_text(encoding="utf-8"))
    result=score(payload)
    Path(args.output).parent.mkdir(parents=True,exist_ok=True)
    Path(args.output).write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps(result,indent=2))
if __name__=="__main__": main()
