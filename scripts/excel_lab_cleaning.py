from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assignments" / "data"
encounters = pd.read_csv(DATA / "excel_encounters.csv", dtype={"encounter_id": "string"})
orders = pd.read_csv(DATA / "excel_raw_medication_orders.csv", dtype={"order_id":"string","encounter_id":"string"})
formulary = pd.read_csv(DATA / "synthetic_formulary_reference.csv")

# Preserve raw data; transform a copy.
clean = orders.copy()
for col in ["drug_name", "therapeutic_class", "order_status", "encounter_id"]:
    clean[col] = clean[col].astype("string").str.strip()
clean["drug_name"] = clean["drug_name"].str.replace(r"\\s+", " ", regex=True)
clean["order_status"] = clean["order_status"].str.upper()
clean["missing_class_flag"] = clean["therapeutic_class"].isna() | clean["therapeutic_class"].eq("")
clean["missing_cost_flag"] = clean["unit_cost_inr"].isna()
clean["orphan_encounter_flag"] = ~clean["encounter_id"].isin(encounters["encounter_id"])

# Candidate duplicate review: do not auto-delete. Keep a review report.
business_key = ["encounter_id", "order_date", "drug_name", "route", "quantity"]
clean["duplicate_candidate_flag"] = clean.duplicated(subset=business_key, keep=False)

OUT = ROOT / "assignments" / "outputs"
OUT.mkdir(exist_ok=True)
clean.to_csv(OUT / "medication_orders_quality_review.csv", index=False)
clean.loc[clean["duplicate_candidate_flag"]].to_csv(OUT / "duplicate_candidates_for_review.csv", index=False)
print("Encounter rows:", len(encounters))
print("Raw order rows:", len(orders))
print("Missing class:", int(clean["missing_class_flag"].sum()))
print("Missing cost:", int(clean["missing_cost_flag"].sum()))
print("Orphan encounter refs:", int(clean["orphan_encounter_flag"].sum()))
print("Duplicate candidate rows:", int(clean["duplicate_candidate_flag"].sum()))
print("Wrote review files to:", OUT)
