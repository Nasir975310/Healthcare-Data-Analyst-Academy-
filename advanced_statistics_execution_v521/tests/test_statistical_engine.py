import importlib.util, tempfile, unittest, json
from pathlib import Path
P=Path(__file__).resolve().parents[1]/"scripts"/"statistical_engine.py"
sp=importlib.util.spec_from_file_location("se",P); m=importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
class StatisticalEngineTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(); self.base=Path(self.tmp.name)
  self.data=self.base/"data.csv"
  self.data.write_text("id,group,value,outcome,age\n1,A,10,0,30\n2,A,12,1,40\n3,A,11,0,35\n4,B,20,1,50\n5,B,22,0,60\n6,B,21,1,55\n",encoding="utf-8")
 def tearDown(self): self.tmp.cleanup()
 def test_profile_and_missingness(self):
  d=m.load_data(self.data); p=m.profile(d); self.assertEqual(p[0]["n"],6)
  self.assertEqual(m.missing_report(d)[0]["missing_n"],0)
 def test_outlier_report(self):
  d=m.load_data(self.data); r=m.outlier_report(d,["value"]); self.assertEqual(r[0]["method"],"1.5xIQR exploratory flag")
 def test_welch_comparison(self):
  d=m.load_data(self.data); r=m.compare_groups(d,{"outcome":"value","group":"group","test":"welch"})
  self.assertEqual(r["n"],[3,3]); self.assertGreater(r["p_value"],0)
 def test_chi_square(self):
  d=m.load_data(self.data); r=m.categorical_test(d,{"row":"group","column":"outcome"})
  self.assertEqual(r["degrees_freedom"],1)
 def test_linear_regression(self):
  d=m.load_data(self.data); r=m.regression(d,{"outcome":"value","predictors":["age"],"family":"linear"})
  self.assertEqual(r["family"],"linear")
 def test_logistic_regression(self):
  d=m.load_data(self.data); r=m.regression(d,{"outcome":"outcome","predictors":["age"],"family":"logistic"})
  self.assertEqual(r["family"],"logistic")
 def test_complete_report_outputs(self):
  cfg={"outlier_columns":["value"],"group_comparison":{"outcome":"value","group":"group"}}
  c=self.base/"config.json"; c.write_text(json.dumps(cfg)); out=self.base/"out"
  r=m.run_analysis(self.data,c,out)
  self.assertTrue((out/"analysis_results.json").exists())
  self.assertTrue((out/"descriptive_profile.csv").exists())
  self.assertTrue((out/"statistical_report.md").exists())
 def test_invalid_group_count(self):
  d=m.load_data(self.data)
  with self.assertRaises(ValueError): m.compare_groups(d,{"outcome":"value","group":"id"})
if __name__=="__main__": unittest.main()
