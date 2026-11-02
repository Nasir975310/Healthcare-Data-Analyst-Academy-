"""Offline vacancy source registry, duplicate detection and verification checklist."""
from __future__ import annotations
import argparse, csv, json, re, html
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

FIELDS = [
    "vacancy_id","employer","role","source_name","source_type","source_url",
    "employer_official_url","date_found","deadline","location","remote_type",
    "eligibility_notes","employer_domain_checked","vacancy_on_official_site",
    "recruiter_identity_checked","no_upfront_fee_confirmed","privacy_request_checked",
    "verification_notes","status"
]
BOOL_FIELDS = {
    "employer_domain_checked","vacancy_on_official_site","recruiter_identity_checked",
    "no_upfront_fee_confirmed","privacy_request_checked"
}
ALLOWED = {"yes","no","unknown","not_applicable"}
TRACKER_STAGES = {"new","reviewing","verified","not_verified","expired","applied","closed"}
TRACKING_PARAMS = {"utm_source","utm_medium","utm_campaign","utm_term","utm_content","gclid","fbclid"}

def canonical_url(url):
    """Normalise URL for duplicate comparison; do not claim URL ownership/authenticity."""
    raw = (url or "").strip()
    if not raw:
        return ""
    parts = urlsplit(raw)
    scheme = (parts.scheme or "https").lower()
    host = (parts.hostname or "").lower()
    if not host:
        return raw.lower().rstrip("/")
    port = parts.port
    netloc = host
    if port and not ((scheme == "https" and port == 443) or (scheme == "http" and port == 80)):
        netloc += f":{port}"
    path = re.sub(r"/+", "/", parts.path or "/").rstrip("/") or "/"
    query = [(k,v) for k,v in parse_qsl(parts.query, keep_blank_values=True)
             if k.lower() not in TRACKING_PARAMS]
    query.sort()
    return urlunsplit((scheme, netloc, path, urlencode(query), ""))

def read_registry(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        missing = [x for x in FIELDS if x not in (reader.fieldnames or [])]
        if missing:
            raise ValueError("Missing columns: " + ", ".join(missing))
        rows = list(reader)
    seen = set()
    for line, row in enumerate(rows, 2):
        vid = (row.get("vacancy_id") or "").strip()
        if not vid: raise ValueError(f"Row {line}: vacancy_id is required.")
        if vid in seen: raise ValueError(f"Row {line}: duplicate vacancy_id {vid!r}.")
        seen.add(vid)
        stage = (row.get("status") or "").strip().lower()
        if stage not in TRACKER_STAGES: raise ValueError(f"Row {line}: invalid status {stage!r}.")
        for field in BOOL_FIELDS:
            value = (row.get(field) or "unknown").strip().lower()
            if value not in ALLOWED: raise ValueError(f"Row {line}: {field} must be yes/no/unknown/not_applicable.")
        for field in ("date_found","deadline"):
            value = (row.get(field) or "").strip()
            if value:
                try: date.fromisoformat(value)
                except ValueError as e: raise ValueError(f"Row {line}: {field} must be YYYY-MM-DD.") from e
        url = (row.get("source_url") or "").strip()
        if url and urlsplit(url).scheme not in {"http","https"}:
            raise ValueError(f"Row {line}: source_url must use http or https.")
    return rows

def assess_row(row, as_of):
    checks = {f: (row.get(f) or "unknown").strip().lower() for f in BOOL_FIELDS}
    critical = [
        "employer_domain_checked","vacancy_on_official_site",
        "recruiter_identity_checked","no_upfront_fee_confirmed","privacy_request_checked"
    ]
    yes_count = sum(checks[f] == "yes" for f in critical)
    unknown = [f for f in critical if checks[f] in {"unknown","not_applicable"}]
    no = [f for f in critical if checks[f] == "no"]
    deadline = (row.get("deadline") or "").strip()
    expired = bool(deadline and date.fromisoformat(deadline) < as_of)
    warnings = []
    if not (row.get("source_url") or "").strip():
        warnings.append("No source URL recorded.")
    if not (row.get("employer_official_url") or "").strip():
        warnings.append("No independently located employer website recorded.")
    if expired: warnings.append("Deadline is before the selected review date.")
    if no: warnings.append("One or more verification checks are marked NO: " + ", ".join(no))
    if unknown: warnings.append("Verification remains incomplete: " + ", ".join(unknown))
    # Deliberately conservative: a vacancy is never auto-certified.
    ready = not expired and not no and not unknown and bool(row.get("employer_official_url"))
    return {
        "vacancy_id": row["vacancy_id"],
        "employer": row.get("employer",""),
        "role": row.get("role",""),
        "source_url": row.get("source_url",""),
        "canonical_source_url": canonical_url(row.get("source_url","")),
        "deadline": deadline,
        "expired_as_of_review_date": expired,
        "checks_yes": yes_count,
        "checks_total": len(critical),
        "checks_unknown_or_na": unknown,
        "checks_no": no,
        "manual_review_complete": not unknown and not no,
        "eligible_for_human_final_review": ready,
        "warnings": warnings,
        "disclaimer": "Checklist completion is not proof of legitimacy, employment eligibility or vacancy authenticity. Independently verify through official channels."
    }

def analyse(rows, as_of):
    assessments = [assess_row(r, as_of) for r in rows]
    urls = {}
    for item in assessments:
        key = item["canonical_source_url"]
        if key: urls.setdefault(key, []).append(item["vacancy_id"])
    duplicate_groups = [ids for ids in urls.values() if len(ids) > 1]
    return {
        "review_date": as_of.isoformat(),
        "vacancy_count": len(rows),
        "duplicate_url_groups": duplicate_groups,
        "expired_count": sum(x["expired_as_of_review_date"] for x in assessments),
        "manual_review_complete_count": sum(x["manual_review_complete"] for x in assessments),
        "eligible_for_human_final_review_count": sum(x["eligible_for_human_final_review"] for x in assessments),
        "assessments": assessments,
        "limitations": [
            "No network access is used; URLs, domains, employers and vacancies are not verified.",
            "Duplicate detection compares normalised source URLs only; same vacancy on different URLs may not be detected.",
            "A complete checklist is not a guarantee of legitimacy or safety.",
            "Review date is supplied by the user; deadline status depends on its accuracy.",
            "Do not submit credentials, OTPs, passwords, banking details or unnecessary identity documents."
        ]
    }

def render_html(report):
    rows = []
    for a in report["assessments"]:
        state = "Expired" if a["expired_as_of_review_date"] else ("Ready for human review" if a["eligible_for_human_final_review"] else "Needs verification")
        warnings = "<br>".join(html.escape(x) for x in a["warnings"]) or "No checklist warnings"
        url = html.escape(a["source_url"])
        link = f'<a href="{url}" rel="noopener noreferrer">{url}</a>' if url else "—"
        rows.append(f"<tr><td>{html.escape(a['vacancy_id'])}</td><td>{html.escape(a['employer'])}</td><td>{html.escape(a['role'])}</td><td>{state}</td><td>{a['checks_yes']}/{a['checks_total']}</td><td>{warnings}</td><td>{link}</td></tr>")
    duplicates = "".join("<li>"+html.escape(", ".join(group))+"</li>" for group in report["duplicate_url_groups"]) or "<li>None detected by source URL matching</li>"
    limits = "".join("<li>"+html.escape(x)+"</li>" for x in report["limitations"])
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Vacancy verification register</title>
    <style>body{{font:15px system-ui;max-width:1200px;margin:2rem auto;padding:0 1rem;color:#202938;background:#f7f8fa}}section{{background:white;border:1px solid #dce1e8;border-radius:12px;padding:16px;margin:14px 0;overflow:auto}}table{{border-collapse:collapse;width:100%;min-width:850px}}td,th{{padding:9px;text-align:left;vertical-align:top;border-bottom:1px solid #e5e8ed}}.note{{color:#586579}}</style></head><body><h1>Vacancy source & verification register</h1><p class="note">Review date: {report['review_date']} · {report['vacancy_count']} records. This is a local checklist, not an employer verification service.</p>
    <section><h2>Duplicate source URL groups</h2><ul>{duplicates}</ul></section>
    <section><h2>Vacancy review</h2><table><tr><th>ID</th><th>Employer</th><th>Role</th><th>Status</th><th>Checks</th><th>Warnings</th><th>Source</th></tr>{''.join(rows)}</table></section>
    <section><h2>Limitations and safety</h2><ul>{limits}</ul></section></body></html>"""

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("registry")
    p.add_argument("--as-of", required=True, help="Review date YYYY-MM-DD")
    p.add_argument("--out", default="vacancy_review")
    a=p.parse_args()
    review_date=date.fromisoformat(a.as_of)
    rows=read_registry(a.registry)
    report=analyse(rows, review_date)
    out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    (out/"vacancy_report.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    (out/"vacancy_report.html").write_text(render_html(report),encoding="utf-8")
    print(f"Reviewed {len(rows)} records; outputs: {out/'vacancy_report.json'}, {out/'vacancy_report.html'}")

if __name__=="__main__": main()
