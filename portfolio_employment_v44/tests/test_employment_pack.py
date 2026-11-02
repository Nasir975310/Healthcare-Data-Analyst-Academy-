import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/"portfolio_employment_v44"
class EmploymentPackTests(unittest.TestCase):
 def test_five_role_tracks(self):
  data=json.loads((BASE/"role_profiles"/"role_tracks.json").read_text())
  self.assertEqual(len(data),5)
  self.assertTrue(all(x["skills"] and x["evidence"] for x in data))
 def test_templates_present(self):
  for name in ["REPOSITORY_README_TEMPLATE.md","CASE_STUDY_TEMPLATE.md","CV_EVIDENCE_BULLET_TEMPLATE.md","APPLICATION_SCORECARD.md","INTERVIEW_STORY_TEMPLATE.md"]:
   self.assertTrue((BASE/"templates"/name).exists())
 def test_app_module_and_mount(self):
  self.assertTrue((ROOT/"assets"/"employment-pipeline-v44.js").exists())
  page=(ROOT/"index.html").read_text()
  self.assertIn('id="employmentV44App"',page)
  self.assertIn('assets/employment-pipeline-v44.js',page)
 def test_no_external_service_in_module(self):
  src=(ROOT/"assets"/"employment-pipeline-v44.js").read_text()
  self.assertNotIn("fetch(",src)
  self.assertNotIn("XMLHttpRequest",src)
if __name__=="__main__": unittest.main()
