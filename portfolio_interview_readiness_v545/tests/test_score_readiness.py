import unittest
from portfolio_interview_readiness_v545.src.score_readiness import score_payload

def sample(score=2, evidence="test evidence"):
    return {"areas": [{"name": f"area {i}", "score": score, "evidence": evidence} for i in range(7)]}

class ScoreTests(unittest.TestCase):
    def test_complete_practice_ready(self):
        result = score_payload(sample(3))
        self.assertEqual(result["status"], "PRACTICE_READY")
        self.assertEqual(result["total"], 21)
    def test_low_score_development_needed(self):
        self.assertEqual(score_payload(sample(1))["status"], "DEVELOPMENT_NEEDED")
    def test_scored_area_without_evidence_flagged(self):
        self.assertEqual(score_payload(sample(2, ""))["status"], "EVIDENCE_INCOMPLETE")
    def test_rejects_wrong_area_count(self):
        with self.assertRaises(ValueError): score_payload({"areas": []})
    def test_rejects_out_of_range(self):
        with self.assertRaises(ValueError): score_payload(sample(4))
    def test_rejects_duplicate_names(self):
        p = sample(); p["areas"][1]["name"] = p["areas"][0]["name"]
        with self.assertRaises(ValueError): score_payload(p)

if __name__ == "__main__": unittest.main()
