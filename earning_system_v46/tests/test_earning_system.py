import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/"earning_system_v46"
class EarningTests(unittest.TestCase):
 def test_service_catalogue_and_templates(self):
  self.assertTrue((BASE/"service_catalog"/"starter_services.md").exists())
  self.assertTrue((BASE/"service_catalog"/"service_scope_template.md").exists())
  self.assertTrue((BASE/"templates"/"first_client_checklist.md").exists())
 def test_six_sprint_system(self):
  s=(ROOT/"assets"/"earning-system-v46.js").read_text()
  for x in ["Week 1","Market testing and applications","Export weekly execution report","Import backup"]:
   self.assertIn(x,s)
 def test_module_integrated(self):
  s=(ROOT/"index.html").read_text()
  self.assertIn('id="earningV46App"',s)
  self.assertIn('assets/earning-system-v46.js',s)
if __name__=="__main__":unittest.main()
