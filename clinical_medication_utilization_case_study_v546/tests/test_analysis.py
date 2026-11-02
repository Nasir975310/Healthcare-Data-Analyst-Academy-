import sys, unittest, json
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'src'))
from run_analysis import run
class AnalysisTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls): cls.metrics=run()
 def test_raw_rows_and_duplicate_handling(self): self.assertEqual(self.metrics['raw_rows'],301); self.assertEqual(self.metrics['unique_record_ids'],300)
 def test_quality_exclusions(self): self.assertGreaterEqual(self.metrics['quality_issue_count'],5); self.assertEqual(self.metrics['clean_rows'],299)
 def test_paired_rows_bounded(self): self.assertGreater(self.metrics['paired_sbp_rows'],250); self.assertLessEqual(self.metrics['paired_sbp_rows'],self.metrics['clean_rows'])
 def test_summary_exists_and_classes(self):
  data=json.loads((BASE/'outputs'/'quality_and_summary.json').read_text()); self.assertEqual(len(data['by_primary_drug_class']),5)
 def test_sqlite_created(self): self.assertTrue((BASE/'outputs'/'hypertension_analysis.sqlite').exists())
 def test_threshold_caveat(self):
  data=json.loads((BASE/'outputs'/'quality_and_summary.json').read_text()); self.assertIn('Individual targets vary',data['metrics']['interpretation_note'])
if __name__=='__main__': unittest.main()
