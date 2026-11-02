import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/"hiring_assessment_v45"
class HiringTests(unittest.TestCase):
 def test_seven_assessment_briefs(self):
  self.assertEqual(len(list((BASE/"assessments").glob("*.md"))),7)
 def test_fixtures_present(self):
  self.assertTrue((BASE/"fixtures"/"synthetic_encounters.csv").exists())
  self.assertTrue((BASE/"fixtures"/"synthetic_orders.csv").exists())
 def test_rubric_present(self):
  self.assertTrue((BASE/"rubrics"/"scoring_rubric.md").exists())
 def test_module_integrated(self):
  s=(ROOT/"index.html").read_text()
  self.assertIn('id="hiringV45App"',s)
  self.assertIn('assets/hiring-assessment-v45.js',s)
if __name__=="__main__": unittest.main()
