import unittest,tempfile,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from build_portfolio import build
class PortfolioTests(unittest.TestCase):
 def test_metrics_and_integrity(self):
  root=Path(__file__).resolve().parents[1]
  with tempfile.TemporaryDirectory() as t:
   r=build(root/'data',Path(t));m=r['metrics']
   self.assertEqual(r['status'],'PASS');self.assertEqual(m['patients'],6);self.assertEqual(m['encounters'],12)
   self.assertEqual(m['observations'],24);self.assertEqual(m['medication_orders'],16)
   self.assertEqual(sum(m['encounters_by_month'].values()),12)
 def test_output_files(self):
  root=Path(__file__).resolve().parents[1]
  with tempfile.TemporaryDirectory() as t:
   build(root/'data',Path(t));self.assertTrue((Path(t)/'data_quality_report.json').exists())
if __name__=='__main__':unittest.main()
