import unittest,tempfile,shutil
from pathlib import Path
from scripts.validate_sources import validate
class SourceValidationTests(unittest.TestCase):
 def test_packaged_synthetic_data_passes(self):
  base=Path(__file__).resolve().parents[1]/'data';r=validate(base);self.assertEqual(r['status'],'PASS');self.assertEqual(r['counts']['patients.csv'],6);self.assertEqual(r['counts']['encounters.csv'],12);self.assertEqual(r['counts']['observations.csv'],24);self.assertEqual(r['counts']['medications.csv'],16)
 def test_detects_duplicate_identifier(self):
  base=Path(__file__).resolve().parents[1]/'data'
  with tempfile.TemporaryDirectory() as td:
   dst=Path(td)
   for f in base.glob('*.csv'):shutil.copy(f,dst/f.name)
   p=dst/'patients.csv';lines=p.read_text().splitlines();p.write_text('\n'.join(lines+[lines[1]])+'\n')
   self.assertEqual(validate(dst)['status'],'FAIL')
if __name__=='__main__':unittest.main()
