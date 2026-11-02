import json, unittest
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
class ReportingPackTests(unittest.TestCase):
 def test_report_exists(self): self.assertTrue((BASE/'outputs/analytical_report.html').exists())
 def test_results_reconcile(self):
  x=json.loads((BASE/'outputs/analysis_results.json').read_text())
  self.assertEqual(x['quality']['raw_rows'],301)
  self.assertEqual(x['quality']['unique_ids'],300)
  self.assertEqual(x['quality']['paired_sbp_rows'],296)
 def test_class_summaries(self):
  x=json.loads((BASE/'outputs/analysis_results.json').read_text())
  self.assertEqual(len(x['by_primary_drug_class']),5)
  self.assertEqual(sum(y['n'] for y in x['by_primary_drug_class']),296)
 def test_powerbi_spec_and_dax(self):
  self.assertTrue((BASE/'powerbi/POWER_BI_MODEL_SPEC.md').exists())
  self.assertIn('Mean Paired SBP Change',(BASE/'powerbi/DAX_MEASURES.dax').read_text())
 def test_limitations_present(self):
  h=(BASE/'outputs/analytical_report.html').read_text()
  self.assertIn('synthetic',h.lower()); self.assertIn('confounding',h.lower())
if __name__=='__main__': unittest.main()
