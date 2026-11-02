import csv, json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
TECH=ROOT/"technical_environment_v47"
class TechnicalEnvironmentTests(unittest.TestCase):
 def test_synthetic_dataset(self):
  with (TECH/"starter_project/data/raw/synthetic_encounters.csv").open(newline="") as f: rows=list(csv.DictReader(f))
  self.assertEqual(len(rows),150)
  ids=[r["encounter_id"] for r in rows]
  self.assertEqual(len(ids),len(set(ids)))
 def test_cross_platform_guides(self):
  self.assertTrue((TECH/"guides/setup_linux.md").exists())
  self.assertTrue((TECH/"guides/setup_windows.md").exists())
 def test_database_and_project_scaffold(self):
  self.assertTrue((TECH/"starter_project/docker-compose.yml").exists())
  self.assertTrue((TECH/"starter_project/pyproject.toml").exists())
  self.assertTrue((TECH/"starter_project/scripts/load_sqlite.py").exists())
 def test_ui_integration(self):
  html=(ROOT/"index.html").read_text()
  self.assertIn('id="technicalV47App"',html)
  self.assertIn('assets/technical-environment-v47.js',html)
if __name__=="__main__":unittest.main()
