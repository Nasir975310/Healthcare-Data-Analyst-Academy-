import csv
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class CareerKitTests(unittest.TestCase):
    def test_required_documents_exist(self):
        required = [
            "README.md", "docs/ROLE_TARGETING_MATRIX.md",
            "templates/MASTER_CV.md", "templates/LINKEDIN_PROFILE.md",
            "templates/COVER_LETTER.md", "templates/PORTFOLIO_PROJECT_SUMMARY.md",
            "guides/30_DAY_EXECUTION_PLAN.md", "guides/INTERVIEW_PREPARATION.md",
            "tracker/application_tracker.csv", "tracker/weekly_scorecard.csv",
            "tracker/skills_evidence_matrix.csv"
        ]
        for rel in required:
            with self.subTest(path=rel):
                self.assertTrue((ROOT / rel).is_file())

    def test_application_tracker_has_unique_headers(self):
        with (ROOT / "tracker/application_tracker.csv").open(encoding="utf-8") as f:
            headers = next(csv.reader(f))
        self.assertEqual(len(headers), len(set(headers)))
        self.assertIn("job_url", headers)
        self.assertIn("next_action", headers)

    def test_skills_matrix_separates_evidence_from_claims(self):
        with (ROOT / "tracker/skills_evidence_matrix.csv").open(encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertGreaterEqual(len(rows), 7)
        self.assertTrue(all(r["evidence_level"] for r in rows))
        self.assertTrue(any(r["skill"] == "Power BI" and "Not yet evidenced" in r["status"] for r in rows))

    def test_thesis_and_synthetic_projects_are_distinguished(self):
        cv = (ROOT / "templates/MASTER_CV.md").read_text(encoding="utf-8")
        summary = (ROOT / "templates/PORTFOLIO_PROJECT_SUMMARY.md").read_text(encoding="utf-8")
        self.assertIn("Final study sample: 153 patients", cv)
        self.assertIn("Synthetic Outpatient", summary)
        self.assertIn("separate from the user's Pharm.D thesis", summary)

    def test_no_fabricated_contact_details(self):
        cv = (ROOT / "templates/MASTER_CV.md").read_text(encoding="utf-8")
        self.assertIn("Email: To be added", cv)
        self.assertNotIn("@gmail.com", cv.lower())

if __name__ == "__main__":
    unittest.main()
