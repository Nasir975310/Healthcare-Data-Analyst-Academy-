import argparse, json
from pathlib import Path

AREAS = 7
MAX_SCORE = 3

def score_payload(payload):
    areas = payload.get("areas")
    if not isinstance(areas, list) or len(areas) != AREAS:
        raise ValueError(f"Expected exactly {AREAS} assessment areas")
    names = set()
    total = 0
    missing = []
    results = []
    for item in areas:
        name = item.get("name")
        score = item.get("score")
        evidence = item.get("evidence", "")
        if not isinstance(name, str) or not name.strip() or name in names:
            raise ValueError("Area names must be non-empty and unique")
        names.add(name)
        if isinstance(score, bool) or not isinstance(score, int) or not 0 <= score <= MAX_SCORE:
            raise ValueError(f"Score for {name!r} must be an integer from 0 to {MAX_SCORE}")
        if not isinstance(evidence, str):
            raise ValueError(f"Evidence for {name!r} must be text")
        if score > 0 and not evidence.strip():
            missing.append(name)
        total += score
        results.append({"name": name, "score": score, "evidence_present": bool(evidence.strip())})
    maximum = AREAS * MAX_SCORE
    pct = round(total / maximum * 100, 1)
    state = "EVIDENCE_INCOMPLETE" if missing else ("PRACTICE_READY" if pct >= 75 else "DEVELOPMENT_NEEDED")
    return {"total": total, "maximum": maximum, "percentage": pct, "status": state,
            "areas": results, "missing_evidence_for_scored_areas": missing,
            "interpretation": "Practice aid only; not a validated hiring predictor or proof of employment readiness."}

def main():
    parser = argparse.ArgumentParser(description="Score the Academy interview-readiness self-assessment")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    report = score_payload(payload)
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("total", "maximum", "percentage", "status")}, indent=2))

if __name__ == "__main__":
    main()
