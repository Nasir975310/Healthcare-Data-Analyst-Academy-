import json, unittest
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
class DashboardAssetTests(unittest.TestCase):
 def test_html_and_data_exist(self):
  self.assertTrue((BASE/'dashboard/index.html').exists());self.assertTrue((BASE/'data/dashboard_data.json').exists())
 def test_data_row_count(self):
  x=json.loads((BASE/'data/dashboard_data.json').read_text());self.assertEqual(len(x),301)
 def test_filters_and_export_exist(self):
  h=(BASE/'dashboard/index.html').read_text();self.assertIn('addEventListener("change",render)',h);self.assertIn('exportCSV',h)
 def test_synthetic_warning_present(self):
  h=(BASE/'dashboard/index.html').read_text().lower();self.assertIn('synthetic-data warning',h);self.assertIn('not clinical evidence',h)
 def test_metric_contract_exists(self): self.assertTrue((BASE/'docs/METRIC_CONTRACT.md').exists())
if __name__=='__main__':unittest.main()
