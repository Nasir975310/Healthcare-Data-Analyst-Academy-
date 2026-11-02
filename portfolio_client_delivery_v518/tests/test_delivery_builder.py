import importlib.util, json, tempfile, unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]/"scripts"/"delivery_builder.py"
spec=importlib.util.spec_from_file_location("delivery_builder",P); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
class DeliveryTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(); self.base=Path(self.tmp.name)
  self.src=self.base/"input.csv"; self.src.write_text("id,age,readmit\nA,30,false\nB,,true\n",encoding="utf-8")
 def tearDown(self): self.tmp.cleanup()
 def test_builds_complete_package(self):
  out=self.base/"package"; result=m.build(self.src,out,"Test","Client","Objective","Team")
  self.assertEqual(result["rows"],2); self.assertTrue((out/"project_manifest.json").exists())
  self.assertTrue((out/"reports"/"executive_summary.md").exists()); self.assertTrue(Path(result["archive"]).exists())
 def test_dictionary_missingness(self):
  out=self.base/"p"; m.build(self.src,out,"T","A","O","X")
  d=json.loads((out/"data_dictionary.json").read_text())
  age=next(x for x in d if x["field"]=="age"); self.assertEqual(age["missing"],1)
 def test_sensitive_column_flag(self):
  src=self.base/"s.csv"; src.write_text("patient_name,age\nJohn,30\n")
  r=m.build(src,self.base/"sout","T","A","O","X"); self.assertIn("patient_name",r["sensitive_name_flags"])
 def test_empty_header_rejected(self):
  src=self.base/"empty.csv"; src.write_text("")
  with self.assertRaises(ValueError): m.build(src,self.base/"emptyout","T","A","O","X")
 def test_sha256_is_stable(self):
  self.assertEqual(m.sha256(self.src),m.sha256(self.src))
if __name__=="__main__": unittest.main()
