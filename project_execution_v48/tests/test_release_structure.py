import unittest, csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class ProjectReleaseTests(unittest.TestCase):
 def test_dataset_has_planted_quality_issues(self):
  with (ROOT/"data/raw/synthetic_hospital_encounters.csv").open(newline="") as f: rows=list(csv.DictReader(f))
  self.assertEqual(len(rows),241)
  self.assertEqual(rows[5]["encounter_id"],rows[-1]["encounter_id"])
 def test_instructions_and_sql_exist(self):
  for p in ["README.md","guides/project_workflow.md","sql/analysis_queries.sql","templates/case_study_template.md","run_project.py"]:
   self.assertTrue((ROOT/p).exists())
 def test_pipeline_outputs_exist_after_run(self):
  for p in ["data/processed/quality_report.json","data/processed/clean_encounters.csv","data/quarantine/quarantined_encounters.csv","reports/project_report.md","reports/department_encounters.png"]:
   self.assertTrue((ROOT/p).exists())
if __name__=="__main__":unittest.main()
