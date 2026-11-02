"""Create a small JSON summary from the synthetic encounters CSV."""
from pathlib import Path
import csv, json
from collections import Counter

base = Path(__file__).resolve().parents[3]
source = base / "datasets" / "v03_python" / "encounters.csv"
output = base / "projects" / "v03_python_foundations" / "encounter_summary.json"

with source.open("r", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

summary = {
    "record_count": len(rows),
    "unique_encounters": len({r["encounter_id"] for r in rows}),
    "encounter_type_counts": dict(Counter(r["encounter_type"] for r in rows)),
    "missing_sbp_count": sum(r["systolic_bp"] == "" for r in rows),
}
output.write_text(json.dumps(summary, indent=2), encoding="utf-8")
print(f"Wrote {output}")
