import json, unittest
from pathlib import Path
from validate_dashboard import filtered, metrics, comorbidity, valid_class
BASE=Path(__file__).resolve().parents[1]
ROWS=json.loads((BASE/'data/dashboard_data.json').read_text())
class DashboardValidationTests(unittest.TestCase):
 def test_all_rows_and_duplicates(self):
  m=metrics(ROWS); self.assertEqual(m['filtered_records'],301); self.assertEqual(m['unique_record_ids'],300); self.assertEqual(m['duplicate_excess'],1)
 def test_drug_class_filter(self):
  for d in {r['primary_drug_class'] for r in ROWS if valid_class(r.get('primary_drug_class'))}: self.assertTrue(all(r['primary_drug_class']==d for r in filtered(ROWS,drug=d)))
 def test_sex_filter(self):
  for x in ('Male','Female'): self.assertTrue(all(r['sex']==x for r in filtered(ROWS,sex=x)))
 def test_age_bands_are_disjoint(self):
  for a in ('18–39','40–59','60+'):
   from validate_dashboard import age_band
   self.assertTrue(all(age_band(r.get('age_years'))==a for r in filtered(ROWS,age=a)))
 def test_comorbidity_schema_and_tristate(self):
  self.assertTrue(any(comorbidity(r) is True for r in ROWS)); self.assertTrue(any(comorbidity(r) is False for r in ROWS))
  self.assertTrue(all(comorbidity(r) is True for r in filtered(ROWS,co='yes')))
  self.assertTrue(all(comorbidity(r) is False for r in filtered(ROWS,co='no')))
 def test_combined_filter(self):
  result=filtered(ROWS,drug='ARB',sex='Female',age='60+',co='yes')
  self.assertTrue(all(r['primary_drug_class']=='ARB' and r['sex']=='Female' and int(r['age_years'])>=60 and comorbidity(r) is True for r in result))
 def test_invalid_class_sentinel_excluded_from_pairs(self):
  self.assertFalse(valid_class('None')); self.assertEqual(metrics(ROWS)['paired_sbp_records'],sum(1 for r in ROWS if valid_class(r.get('primary_drug_class')) and r['baseline_sbp_mmhg'] is not None and r['followup_sbp_mmhg'] is not None and 70<=float(r['baseline_sbp_mmhg'])<=250 and 70<=float(r['followup_sbp_mmhg'])<=250))
 def test_export_csv_escaping_contract(self):
  import csv, io
  sample=[{'field':'comma, quote " and newline\n'}]; buf=io.StringIO(); w=csv.DictWriter(buf,fieldnames=['field']); w.writeheader(); w.writerows(sample); self.assertEqual(next(csv.DictReader(io.StringIO(buf.getvalue()))),sample[0])
if __name__=='__main__': unittest.main()
