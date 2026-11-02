import importlib.util, json, tempfile, unittest, csv, sqlite3
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
PROJECT=load("project",BASE/"src"/"run_project.py")
PREFLIGHT=load("preflight",BASE/"scripts"/"repository_preflight.py")

class ProjectTests(unittest.TestCase):
    def test_source_counts_and_duplicate_rule(self):
        rows=PROJECT.load_rows(BASE/"data"/"synthetic_outpatient_encounters.csv")
        report,unique=PROJECT.analyse(rows)
        self.assertEqual(report["counts"]["raw_rows"],24)
        self.assertEqual(report["counts"]["duplicate_rows_removed"],1)
        self.assertEqual(report["counts"]["deduplicated_rows"],23)
        self.assertEqual(report["duplicate_encounter_ids"],["C023"])

    def test_missing_wait_is_not_zero_and_negative_is_excluded(self):
        rows=PROJECT.load_rows(BASE/"data"/"synthetic_outpatient_encounters.csv")
        report,_=PROJECT.analyse(rows)
        self.assertLess(report["counts"]["completed_encounters_with_valid_wait"],
                        report["counts"]["eligible_completed_encounters"])
        self.assertTrue(any("negative_wait" in x["issues"] for x in report["exceptions"]))

    def test_output_reproducibility_and_sqlite(self):
        with tempfile.TemporaryDirectory() as td:
            report=PROJECT.write_outputs(BASE/"data"/"synthetic_outpatient_encounters.csv",td)
            out=Path(td)
            self.assertTrue((out/"quality_report.json").exists())
            self.assertTrue((out/"department_summary.csv").exists())
            with sqlite3.connect(out/"analytics.sqlite") as con:
                n=con.execute("SELECT COUNT(*) FROM encounters_deduplicated").fetchone()[0]
                self.assertEqual(n,23)
            manifest=json.loads((out/"sha256_manifest.json").read_text())
            self.assertIn("quality_report.json",manifest)

    def test_missing_required_column_fails(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"bad.csv";p.write_text("encounter_id,status\\nX,completed\\n")
            with self.assertRaises(ValueError): PROJECT.load_rows(p)

    def test_preflight_ignores_generated_runtime_outputs(self):
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/"outputs";out.mkdir();(out/"analytics.sqlite").write_bytes(b"sqlite")
            result=PREFLIGHT.scan(td)
            self.assertEqual(result["finding_count"],0)

    def test_preflight_detects_test_secret_pattern(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"sample.py"
            p.write_text('api' + chr(95) + 'key = ' + chr(34) + 'ABCDEFGH' + 'IJKLMNOP' + 'QRSTUV' + chr(34) + chr(10))
            result=PREFLIGHT.scan(td)
            self.assertGreaterEqual(result["finding_count"],1)

if __name__=="__main__": unittest.main()
