import csv, json, unittest
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/"practicum_v43"/"data"
class PracticumFixtureTests(unittest.TestCase):
 def test_fixture_row_counts(self):
  expected={"hospital_encounters_raw.csv":1200,"antihypertensive_due_raw.csv":500,"pv_cases_raw.csv":240,"medication_orders_raw.csv":1800}
  for f,n in expected.items():
   self.assertEqual(len(pd.read_csv(DATA/f)),n)
 def test_primary_keys(self):
  for f,k in [("hospital_encounters_raw.csv","encounter_id"),("antihypertensive_due_raw.csv","patient_id"),("pv_cases_raw.csv","case_id"),("medication_orders_raw.csv","order_id")]:
   df=pd.read_csv(DATA/f); self.assertTrue(df[k].notna().all()); self.assertTrue(df[k].is_unique)
 def test_medication_order_quality_issues_are_preserved(self):
  o=pd.read_csv(DATA/"medication_orders_raw.csv")
  self.assertGreater((o.quantity<=0).sum(),0)
  self.assertGreater(o.unit_cost.isna().sum(),0)
  self.assertGreater((o.drug_class.fillna("").str.strip()=="").sum(),0)
  e=pd.read_csv(DATA/"hospital_encounters_raw.csv")
  self.assertGreater((~o.encounter_id.isin(e.encounter_id)).sum(),0)
 def test_all_engagement_briefs_and_rubric_exist(self):
  b=ROOT/"practicum_v43"/"briefs"
  self.assertEqual(len(list(b.glob("ENG-*.md"))),5)
  self.assertTrue((ROOT/"practicum_v43"/"REVIEW_RUBRIC.md").exists())
 def test_no_live_patient_claims_in_dataset_metadata(self):
  d=(ROOT/"practicum_v43"/"data"/"DATA_DICTIONARY.md").read_text().lower()
  self.assertIn("fabricated",d)
  self.assertIn("not patient data",d)
if __name__=="__main__": unittest.main()
