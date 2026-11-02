import importlib.util, pathlib, unittest, sys
HERE=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('pgloader',HERE/'scripts/load_postgresql.py')
loader=importlib.util.module_from_spec(spec);spec.loader.exec_module(loader)
class LoaderTests(unittest.TestCase):
 def test_date_parser(self):
  self.assertEqual(loader.as_date('2026-11-02T10:30:00Z').isoformat(),'2026-11-02')
  self.assertIsNone(loader.as_date(''))
 def test_timestamp_parser(self):
  self.assertEqual(loader.as_ts('2026-11-02T10:30:00Z').utcoffset().total_seconds(),0)
 def test_row_hash_deterministic_and_sensitive_to_change(self):
  a=loader.row_hash('female','1980-01-01')
  self.assertEqual(a,loader.row_hash('female','1980-01-01'))
  self.assertNotEqual(a,loader.row_hash('male','1980-01-01'))
 def test_schema_contract(self):
  sql=(HERE/'sql/migrations/001_schema.sql').read_text()
  for term in ['dim_patient','is_current','row_hash','uq_dim_patient_current','fact_observation','fact_medication_request','mart_encounter_summary','mart_patient_cohort']:
   self.assertIn(term,sql)
 def test_scd2_and_idempotent_upsert_contract(self):
  code=(HERE/'scripts/load_postgresql.py').read_text()
  self.assertIn('valid_to=%s',code)
  self.assertIn('version',code)
  self.assertIn('ON CONFLICT(observation_id)',code)
  self.assertIn('ON CONFLICT(medication_request_id)',code)
 def test_security_template_has_no_password(self):
  sql=(HERE/'sql/security/roles_and_grants.sql').read_text().lower()
  self.assertNotIn('password ',sql)
  self.assertIn('hda_analyst',sql);self.assertIn('hda_loader',sql)
if __name__=='__main__':unittest.main()
