import json, tempfile, unittest, hashlib
from pathlib import Path
from src.release_gate import compare, sha256

class ReleaseGateTests(unittest.TestCase):
    def fixture(self,base):
        local=base/"local"; ref=base/"ref"; local.mkdir(); ref.mkdir()
        for name,content in (("quality_report.json",'{"counts":{"raw_rows":24}}'),("department_summary.csv","department,n\\nCardiology,7\\n"),("sha256_manifest.json","{}")):
            (local/name).write_text(content); (ref/name).write_text(content)
        captured=[{"file":n,"sha256":sha256(local/n),"bytes":(local/n).stat().st_size} for n in ("quality_report.json","department_summary.csv","sha256_manifest.json")]
        report={"commands":[{"exit_code":0},{"exit_code":0},{"exit_code":0}],"captured_outputs":captured,"platform":"Linux","python":"3.x","project_path":"/tmp/project"}
        (local/"local_run_report.json").write_text(json.dumps(report))
        return local,ref
    def test_missing_evidence_is_not_run(self):
        with tempfile.TemporaryDirectory() as td:
            base=Path(td); result=compare(base/"local",base/"ref")
            self.assertEqual(result["status"],"NOT_RUN")
    def test_matching_evidence_passes(self):
        with tempfile.TemporaryDirectory() as td:
            local,ref=self.fixture(Path(td)); result=compare(local,ref)
            self.assertEqual(result["status"],"PASS")
            self.assertTrue(all(x["passed"] for x in result["checks"]))
    def test_mismatch_requires_review(self):
        with tempfile.TemporaryDirectory() as td:
            local,ref=self.fixture(Path(td)); (local/"department_summary.csv").write_text("department,n\\nCardiology,99\\n")
            result=compare(local,ref)
            self.assertEqual(result["status"],"REVIEW_REQUIRED")
            self.assertTrue(any(x["check"]=="department_summary.csv_matches_reference" and not x["passed"] for x in result["checks"]))
    def test_nonzero_command_requires_review(self):
        with tempfile.TemporaryDirectory() as td:
            local,ref=self.fixture(Path(td)); data=json.loads((local/"local_run_report.json").read_text()); data["commands"][1]["exit_code"]=2
            (local/"local_run_report.json").write_text(json.dumps(data))
            self.assertEqual(compare(local,ref)["status"],"REVIEW_REQUIRED")
if __name__=="__main__": unittest.main()
