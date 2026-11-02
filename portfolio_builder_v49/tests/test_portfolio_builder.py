import csv, json, subprocess, sys, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PROJECT=ROOT.parent/"project_execution_v48"
sys.path.insert(0,str(ROOT/"scripts"))
from build_portfolio_pack import build
class PortfolioBuilderTests(unittest.TestCase):
 def test_generates_portfolio_artifacts(self):
  with tempfile.TemporaryDirectory() as d:
   out=Path(d)/"pack"
   manifest=build(PROJECT,out)
   self.assertTrue(manifest["synthetic_data"])
   for name in ["README_draft.md","data_dictionary.csv","metric_contract.csv","qa_reproducibility.md","portfolio_evidence_inventory.csv","evidence_manifest.json","publication_quality_gate.md"]:
    self.assertTrue((out/name).exists(),name)
 def test_dictionary_and_metrics_have_expected_rows(self):
  with tempfile.TemporaryDirectory() as d:
   out=Path(d);build(PROJECT,out)
   with (out/"data_dictionary.csv").open() as f: self.assertEqual(len(list(csv.DictReader(f))),7)
   with (out/"metric_contract.csv").open() as f: self.assertEqual(len(list(csv.DictReader(f))),3)
 def test_refuses_non_synthetic_input(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"project";(p/"data/processed").mkdir(parents=True)
   (p/"data/processed/quality_report.json").write_text(json.dumps({"synthetic_data":False}))
   with self.assertRaises(ValueError): build(p,Path(d)/"out")
if __name__=="__main__":unittest.main()
