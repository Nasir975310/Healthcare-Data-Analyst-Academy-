"""Summarise a job-application tracker and produce an offline HTML report."""
from __future__ import annotations
import argparse, csv, json, html
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

REQUIRED = ["application_id", "employer", "role", "applied_date", "source", "stage",
            "outcome", "rejection_reason", "cv_version", "remote_type", "follow_up_due", "notes"]
RESPONSE_STAGES = {"screening", "assessment", "interview", "offer", "rejected", "withdrawn"}
INTERVIEW_STAGES = {"interview", "offer"}
OFFER_STAGES = {"offer"}

def read_tracker(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        missing = [c for c in REQUIRED if c not in (reader.fieldnames or [])]
        if missing:
            raise ValueError("Tracker missing required columns: " + ", ".join(missing))
        rows = list(reader)
    seen = set()
    for i, r in enumerate(rows, 2):
        aid = (r.get("application_id") or "").strip()
        if not aid:
            raise ValueError(f"Row {i}: application_id is required.")
        if aid in seen:
            raise ValueError(f"Row {i}: duplicate application_id {aid!r}.")
        seen.add(aid)
        stage = (r.get("stage") or "").strip().lower()
        if stage not in {"saved", "applied", "screening", "assessment", "interview", "offer", "rejected", "withdrawn"}:
            raise ValueError(f"Row {i}: unsupported stage {stage!r}.")
        try:
            date.fromisoformat(r["applied_date"])
        except Exception as e:
            raise ValueError(f"Row {i}: applied_date must be YYYY-MM-DD.") from e
    return rows

def summarise(rows):
    n = len(rows)
    stages = Counter((r["stage"] or "").strip().lower() for r in rows)
    response_n = sum(1 for r in rows if r["stage"].strip().lower() in RESPONSE_STAGES)
    interview_n = sum(1 for r in rows if r["stage"].strip().lower() in INTERVIEW_STAGES)
    offer_n = sum(1 for r in rows if r["stage"].strip().lower() in OFFER_STAGES)
    applied_n = sum(1 for r in rows if r["stage"].strip().lower() != "saved")
    reason_counts = Counter((r["rejection_reason"] or "").strip() or "Not recorded"
                            for r in rows if r["stage"].strip().lower() == "rejected")
    cv_counts = defaultdict(lambda: {"applications": 0, "responses": 0, "interviews": 0, "offers": 0})
    for r in rows:
        cv = (r["cv_version"] or "").strip() or "Not recorded"
        s = r["stage"].strip().lower()
        cv_counts[cv]["applications"] += 1
        cv_counts[cv]["responses"] += s in RESPONSE_STAGES
        cv_counts[cv]["interviews"] += s in INTERVIEW_STAGES
        cv_counts[cv]["offers"] += s in OFFER_STAGES
    def rate(a, b):
        return round((a / b) * 100, 1) if b else None
    return {
        "application_count": n,
        "submitted_count": applied_n,
        "stage_counts": dict(sorted(stages.items())),
        "response_count": response_n,
        "interview_count": interview_n,
        "offer_count": offer_n,
        "response_rate_pct": rate(response_n, applied_n),
        "interview_rate_pct": rate(interview_n, applied_n),
        "offer_rate_pct": rate(offer_n, applied_n),
        "rejection_reasons": dict(reason_counts.most_common()),
        "cv_versions": {k: dict(v) for k, v in sorted(cv_counts.items())},
        "definitions": {
            "response_rate_pct": "Applications currently at screening, assessment, interview, offer, rejected or withdrawn divided by non-saved applications. This is a tracker-stage proxy, not an employer response-time metric.",
            "interview_rate_pct": "Applications currently at interview or offer divided by non-saved applications.",
            "offer_rate_pct": "Applications currently at offer divided by non-saved applications.",
            "cv_versions": "Descriptive counts only. CV groups are not randomized or adjusted for role mix, timing or applicant differences."
        },
        "limitations": [
            "Small, self-entered samples are unstable and may be incomplete.",
            "Current stage is a snapshot; stage history and time-to-response are not modelled.",
            "CV-version comparisons are observational and do not establish that a CV caused an outcome.",
            "No personal data, employer legitimacy or vacancy authenticity is verified."
        ]
    }

def build_html(summary, title="Application performance snapshot"):
    def pct(v):
        return "—" if v is None else f"{v:.1f}%"
    cards = [
        ("Applications", summary["application_count"]),
        ("Submitted", summary["submitted_count"]),
        ("Response-stage proxy", pct(summary["response_rate_pct"])),
        ("Interview rate", pct(summary["interview_rate_pct"])),
        ("Offer rate", pct(summary["offer_rate_pct"]))
    ]
    card_html = "".join(f'<article class="kpi"><span>{html.escape(str(k))}</span><strong>{html.escape(str(v))}</strong></article>' for k,v in cards)
    stages = "".join(f"<tr><td>{html.escape(k)}</td><td>{v}</td></tr>" for k,v in summary["stage_counts"].items()) or '<tr><td colspan="2">No records</td></tr>'
    reasons = "".join(f"<tr><td>{html.escape(k)}</td><td>{v}</td></tr>" for k,v in summary["rejection_reasons"].items()) or '<tr><td colspan="2">No recorded rejections</td></tr>'
    cvs = "".join(f"<tr><td>{html.escape(k)}</td><td>{v['applications']}</td><td>{v['responses']}</td><td>{v['interviews']}</td><td>{v['offers']}</td></tr>" for k,v in summary["cv_versions"].items()) or '<tr><td colspan="5">No records</td></tr>'
    limitations = "".join(f"<li>{html.escape(x)}</li>" for x in summary["limitations"])
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title>
    <style>body{{font:16px system-ui,sans-serif;max-width:1100px;margin:2rem auto;padding:0 1rem;color:#202938;background:#f7f8fa}}h1,h2{{line-height:1.2}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px}}.kpi,section{{background:white;border:1px solid #dce1e8;border-radius:12px;padding:16px}}.kpi span{{display:block;color:#586579;font-size:.9rem}}.kpi strong{{display:block;font-size:1.8rem;margin-top:8px}}section{{margin-top:18px;overflow:auto}}table{{border-collapse:collapse;width:100%}}td,th{{text-align:left;padding:9px;border-bottom:1px solid #e5e8ed}}.note{{color:#586579;font-size:.92rem}}@media(max-width:600px){{body{{margin:1rem auto}}}}</style></head><body>
    <h1>{html.escape(title)}</h1><p class="note">Generated from a user-maintained tracker. Metrics describe recorded stages, not hiring probability.</p>
    <div class="grid">{card_html}</div>
    <section><h2>Pipeline stages</h2><table><tr><th>Current stage</th><th>Applications</th></tr>{stages}</table></section>
    <section><h2>CV version comparison</h2><p class="note">Descriptive counts only; do not interpret differences as causal effects.</p><table><tr><th>Version</th><th>Applications</th><th>Response-stage</th><th>Interview/offer</th><th>Offers</th></tr>{cvs}</table></section>
    <section><h2>Recorded rejection reasons</h2><table><tr><th>Reason</th><th>Count</th></tr>{reasons}</table></section>
    <section><h2>Interpretation limits</h2><ul>{limitations}</ul></section></body></html>"""

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("tracker")
    p.add_argument("--out", default="application_report")
    p.add_argument("--title", default="Application performance snapshot")
    a = p.parse_args()
    rows = read_tracker(a.tracker)
    summary = summarise(rows)
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    (out/"summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (out/"dashboard.html").write_text(build_html(summary, a.title), encoding="utf-8")
    print(f"Processed {len(rows)} tracker rows. Outputs: {out/'summary.json'}, {out/'dashboard.html'}")

if __name__ == "__main__":
    main()
