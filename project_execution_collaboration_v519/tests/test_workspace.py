import importlib.util, tempfile, unittest, json
from pathlib import Path
P=Path(__file__).resolve().parents[1]/"scripts"/"workspace.py"
s=importlib.util.spec_from_file_location("workspace",P); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
class WorkspaceTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(); self.path=Path(self.tmp.name)/"proj"; m.init_project(self.path,"Test project","Analyst")
 def tearDown(self): self.tmp.cleanup()
 def test_scaffold_and_validation(self):
  self.assertEqual(m.validate_project(self.path),[])
  self.assertTrue((self.path/"src/sql/analysis.sql").exists())
 def test_task_state_update(self):
  m.update_task(self.path,"T-001","done")
  t=json.loads((self.path/"governance/tasks.json").read_text())
  self.assertEqual(t[0]["status"],"done")
 def test_unknown_task_rejected(self):
  with self.assertRaises(KeyError): m.update_task(self.path,"T-999","done")
 def test_feedback_and_readiness(self):
  m.add_record(self.path,"review_feedback.json",{"reviewer":"Reviewer","item":"Report","status":"accepted","comment":"Reviewed"},"review_feedback_added")
  self.assertTrue(m.readiness(self.path)["checks"][5]["passed"])
 def test_high_impact_change_blocks_readiness(self):
  m.add_record(self.path,"change_requests.json",{"id":"CR-001","title":"Change cohort","impact":"high","status":"proposed","reason":"Scope change"},"change_request_added")
  self.assertFalse(m.readiness(self.path)["checks"][6]["passed"])
 def test_snapshot_hashes_files(self):
  rec=m.snapshot(self.path,"0.1.0","Initial baseline")
  self.assertGreater(rec["file_count"],0)
 def test_invalid_status_rejected(self):
  with self.assertRaises(ValueError): m.update_task(self.path,"T-001","finished")
if __name__=="__main__": unittest.main()
