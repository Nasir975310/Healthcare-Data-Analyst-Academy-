import importlib.util
import json
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("scorer", BASE / "scripts" / "score_submission.py")
scorer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scorer)

class ScorerTests(unittest.TestCase):
    def test_sample_submission_passes_all_checklist_items(self):
        payload = json.loads((BASE / "examples" / "sample_submission.json").read_text())
        result = scorer.score(payload)
        self.assertEqual(result["passed"], 10)
        self.assertEqual(result["total"], 10)

    def test_empty_submission_fails_all(self):
        result = scorer.score({})
        self.assertEqual(result["passed"], 0)
        self.assertEqual(result["total"], 10)

    def test_limitations_are_required(self):
        payload = json.loads((BASE / "examples" / "sample_submission.json").read_text())
        payload["limitations"] = []
        self.assertFalse(next(x for x in scorer.score(payload)["checks"] if x["id"] == "states_limitations")["passed"])

    def test_sql_duplicate_strategy_required(self):
        payload = json.loads((BASE / "examples" / "sample_submission.json").read_text())
        payload["sql"] = "SELECT COUNT(*) FROM encounters;"
        self.assertFalse(next(x for x in scorer.score(payload)["checks"] if x["id"] == "sql_uses_distinct_or_dedup")["passed"])

    def test_privacy_boundary_required(self):
        payload = json.loads((BASE / "examples" / "sample_submission.json").read_text())
        payload["data_privacy"] = "Data from client."
        self.assertFalse(next(x for x in scorer.score(payload)["checks"] if x["id"] == "privacy_statement")["passed"])

if __name__ == "__main__":
    unittest.main()
