import tempfile,unittest
from pathlib import Path
from src.build_public_repo import build
from src.publication_scan import scan

class PublicationTests(unittest.TestCase):
    def make_source(self,base):
        source=base/"source";source.mkdir()
        for rel in ("src/run_project.py","data/synthetic_outpatient_encounters.csv","docs/data_dictionary.md","docs/metric_contract.md","docs/reference_results.md","docs/reproduction_and_review.md","sql/analysis.sql","scripts/repository_preflight.py","tests/test_project.py",".gitignore","QA_REPORT.md"):
            p=source/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text("synthetic fixture\n")
        return source
    def test_export_builds_readme_manifest_and_ci(self):
        with tempfile.TemporaryDirectory() as td:
            base=Path(td);source=self.make_source(base);dest=base/"repo"
            result=build(source,dest)
            self.assertTrue((dest/"README.md").is_file())
            self.assertTrue((dest/".github/workflows/python-tests.yml").is_file())
            self.assertTrue((dest/"SOURCE_MANIFEST.json").is_file())
            self.assertGreater(result["files_copied"],0)
    def test_export_refuses_nonempty_destination(self):
        with tempfile.TemporaryDirectory() as td:
            base=Path(td);source=self.make_source(base);dest=base/"repo";dest.mkdir();(dest/"keep").write_text("x")
            with self.assertRaises(ValueError):build(source,dest)
    def test_clean_export_scan_has_no_findings(self):
        with tempfile.TemporaryDirectory() as td:
            base=Path(td);source=self.make_source(base);dest=base/"repo";build(source,dest)
            self.assertEqual(scan(dest)["finding_count"],0)
    def test_secret_pattern_is_detected(self):
        with tempfile.TemporaryDirectory() as td:
            base=Path(td);(base/"leak.txt").write_text('api_key = "this_is_a_fake_secret_value"')
            self.assertGreater(scan(base)["finding_count"],0)
if __name__=="__main__":unittest.main()
