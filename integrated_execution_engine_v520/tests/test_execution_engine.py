import importlib.util, tempfile, unittest, json, csv
from pathlib import Path
P=Path(__file__).resolve().parents[1]/"scripts"/"execution_engine.py"
sp=importlib.util.spec_from_file_location("engine",P); m=importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
class EngineTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(); self.project=Path(self.tmp.name)/"proj"
  from importlib.util import spec_from_file_location
  wpath=P.parents[2]/"project_execution_collaboration_v519"/"scripts"/"workspace.py"
  ws=spec_from_file_location("ws",wpath); self.w=importlib.util.module_from_spec(ws); ws.loader.exec_module(self.w)
  self.w.init_project(self.project,"Synthetic test project","Tester")
  self.csv=self.project/"data"/"raw"/"sample.csv"; self.csv.parent.mkdir(parents=True,exist_ok=True)
  self.csv.write_text("id,group,value\n1,A,10\n2,B,20\n2,B,20\n3,A,30\n",encoding="utf-8")
 def tearDown(self): self.tmp.cleanup()
 def test_csv_load_and_readonly_query(self):
  r=m.load_csv_sqlite(self.project,"data/raw/sample.csv","encounters")
  self.assertEqual(r["rows_loaded"],4)
  q=m.read_only_query(self.project, 'SELECT "group", COUNT(*) AS n FROM encounters GROUP BY "group"', "summary.csv")
  self.assertEqual(q["rows"],2)
 def test_write_sql_rejected(self):
  m.load_csv_sqlite(self.project,"data/raw/sample.csv","encounters")
  with self.assertRaises(ValueError): m.read_only_query(self.project,"DELETE FROM encounters")
 def test_authorizer_blocks_mutating_cte(self):
  m.load_csv_sqlite(self.project,"data/raw/sample.csv","encounters")
  with self.assertRaises(Exception): m.read_only_query(self.project,"WITH x AS (SELECT 1) DELETE FROM encounters")
 def test_pipeline_operations(self):
  cfg={"input":"data/raw/sample.csv","output":"data/processed/out.csv","steps":[{"op":"drop_duplicates","key":"id"},{"op":"filter_equals","column":"group","value":"A"},{"op":"select_columns","columns":["id","value"]}]}
  c=self.project/"pipeline.json"; c.write_text(json.dumps(cfg))
  r=m.run_pipeline(self.project,"pipeline.json")
  self.assertEqual(r["rows_input"],4); self.assertEqual(r["rows_output"],2)
  with (self.project/"data/processed/out.csv").open() as f: self.assertEqual(len(list(csv.DictReader(f))),2)
 def test_python_run_and_log(self):
  script=self.project/"src/python/ok.py"; script.write_text("print('execution-ok')\n")
  r=m.run_python(self.project,"src/python/ok.py")
  self.assertEqual(r["status"],"succeeded")
  self.assertTrue((self.project/r["log"]).exists())
 def test_python_failure_captured(self):
  script=self.project/"src/python/fail.py"; script.write_text("raise RuntimeError('expected')\n")
  r=m.run_python(self.project,"src/python/fail.py")
  self.assertEqual(r["status"],"failed"); self.assertEqual(r["exit_code"],1)
 def test_identifier_validation(self):
  with self.assertRaises(ValueError): m.validate_identifier("table; DROP TABLE x")
 def test_pipeline_unknown_operation_rejected(self):
  cfg={"input":"data/raw/sample.csv","steps":[{"op":"run_shell"}]}
  c=self.project/"bad.json"; c.write_text(json.dumps(cfg))
  with self.assertRaises(ValueError): m.run_pipeline(self.project,"bad.json")
if __name__=="__main__": unittest.main()
