import json, pathlib, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
class TestUATAssets(unittest.TestCase):
 def test_manifest_starts_pending(self):
  d=json.loads((ROOT/'evidence/uat_result.json').read_text())
  self.assertIn(d['status'], {'PENDING_USER_RUN','REVIEW_REQUIRED','PASS','FAIL'})
  self.assertIn('scope', d)
 def test_playwright_suite_exists(self):
  self.assertTrue((ROOT/'tests/test_dashboard_browser.py').is_file())
 def test_checklist_has_acceptance_items(self):
  s=(ROOT/'docs/UAT_CHECKLIST.md').read_text()
  for x in ['Page loads','Selecting a drug class','CSV export']:
   self.assertIn(x,s)
if __name__=='__main__': unittest.main()
