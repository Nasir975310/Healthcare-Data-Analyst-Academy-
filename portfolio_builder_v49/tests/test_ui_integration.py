import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
class UIIntegrationTests(unittest.TestCase):
 def test_nav_and_view(self):
  html=(ROOT/"index.html").read_text()
  self.assertIn('data-view="portfolio-v49"',html)
  self.assertIn('id="portfolioV49App"',html)
  self.assertIn('assets/portfolio-builder-v49.js',html)
 def test_generated_outputs(self):
  out=ROOT/"portfolio_builder_v49/output"
  for name in ["README_draft.md","data_dictionary.csv","metric_contract.csv","qa_reproducibility.md","portfolio_evidence_inventory.csv","evidence_manifest.json","publication_quality_gate.md"]:
   self.assertTrue((out/name).exists())
if __name__=="__main__":unittest.main()
