import unittest, json, pathlib, subprocess, sys
HERE=pathlib.Path(__file__).resolve().parents[1]
class ValidationTests(unittest.TestCase):
    def test_validator_passes(self):
        p=subprocess.run([sys.executable,str(HERE/"scripts/validate_practicum.py")],capture_output=True,text=True)
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)
        report=json.loads((HERE/"deliverables/validation_report.json").read_text())
        self.assertEqual(report["failed"],0)
    def test_postgres_ddl_has_fk_and_indexes(self):
        sql=(HERE/"sql/postgresql/001_schema.sql").read_text().lower()
        self.assertIn("references hda_curated.dim_patient",sql)
        self.assertIn("create index",sql)
    def test_dax_avoids_adherence_claim(self):
        dax=(HERE/"powerbi/MEASURES.dax").read_text().lower()
        self.assertIn("medication order count",dax)
        self.assertIn("do not call this adherence",dax)
    def test_rubric_has_hard_gate(self):
        rubric=(HERE/"assessment/PRACTICAL_RUBRIC.md").read_text()
        self.assertIn("Hard gate",rubric)
if __name__=="__main__": unittest.main()
