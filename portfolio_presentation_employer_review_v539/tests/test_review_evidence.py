import tempfile, unittest
from pathlib import Path
from src.review_evidence import audit, EXPECTED

class ReviewEvidenceTests(unittest.TestCase):
    def test_missing_project_artifacts_fail(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            report = audit(base / "project", base / "evidence")
            self.assertEqual(report["artifact_gate"], "FAIL")
            self.assertEqual(len(report["missing_artifacts"]), len(EXPECTED))

    def test_artifact_gate_passes_when_expected_paths_exist(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td); project = base / "project"; evidence = base / "evidence"
            for rel in EXPECTED:
                p = project / rel
                p.mkdir(parents=True, exist_ok=True) if rel in ("tests", "sql", "data") else (p.parent.mkdir(parents=True, exist_ok=True), p.write_text("fixture", encoding="utf-8"))
            report = audit(project, evidence)
            self.assertEqual(report["artifact_gate"], "PASS")

    def test_user_evidence_remains_pending_when_absent(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            report = audit(base / "project", base / "evidence")
            self.assertEqual(report["user_evidence_gate"], "PENDING")

    def test_evidence_files_are_presence_not_certification(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td); evidence = base / "evidence"; evidence.mkdir()
            for name in ("case_study_completed.md", "reproduction_log.md", "employer_review_scorecard.md", "publication_gate_completed.md"):
                (evidence / name).write_text("record", encoding="utf-8")
            report = audit(base / "project", evidence)
            self.assertEqual(report["user_evidence_gate"], "EVIDENCE_FILES_PRESENT_REQUIRES_MANUAL_REVIEW")
            self.assertTrue(any("do not validate correctness" in x for x in report["limitations"]))

if __name__ == "__main__": unittest.main()
