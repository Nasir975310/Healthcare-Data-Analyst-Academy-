"""Create a timestamped local evidence snapshot from user-supplied vacancy text."""
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--vacancy-id",required=True)
    p.add_argument("--source-url",required=True)
    p.add_argument("--source-name",required=True)
    p.add_argument("--excerpt-file",required=True,help="Text copied by the user from the vacancy source")
    p.add_argument("--out",default="evidence")
    a=p.parse_args()
    excerpt=Path(a.excerpt_file).read_text(encoding="utf-8")
    if not excerpt.strip(): raise SystemExit("Excerpt file is empty.")
    raw=excerpt.encode("utf-8")
    digest=hashlib.sha256(raw).hexdigest()
    out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    text_path=out/f"{a.vacancy_id}_source_excerpt.txt"
    manifest_path=out/f"{a.vacancy_id}_evidence.json"
    text_path.write_bytes(raw)
    manifest={
        "vacancy_id":a.vacancy_id,"source_name":a.source_name,"source_url":a.source_url,
        "captured_at":datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "excerpt_file":text_path.name,"sha256":digest,
        "capture_method":"user-supplied text excerpt; no network retrieval performed",
        "limitations":"A hash proves file integrity after capture, not source authenticity, completeness or continued availability."
    }
    manifest_path.write_text(json.dumps(manifest,indent=2),encoding="utf-8")
    print(f"Saved {text_path} and {manifest_path}; SHA-256 {digest}")
if __name__=="__main__":main()
