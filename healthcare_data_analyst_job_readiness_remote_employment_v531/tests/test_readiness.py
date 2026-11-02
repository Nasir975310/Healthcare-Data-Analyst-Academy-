import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from score_readiness import score, RUBRIC
class ReadinessTests(unittest.TestCase):
    def setUp(self):
        self.payload={"scores":{s["id"]:80 for s in RUBRIC["sections"]}}
    def test_weighted_total(self): self.assertEqual(score(self.payload)["weighted_score"],80)
    def test_weights_sum_to_100(self): self.assertEqual(sum(s["weight"] for s in RUBRIC["sections"]),100)
    def test_privacy_gate(self):
        p=dict(self.payload,privacy_or_integrity_breach=True)
        self.assertIn("Not ready",score(p)["band"])
    def test_missing_score_rejected(self):
        with self.assertRaises(ValueError): score({"scores":{}})
    def test_out_of_range_rejected(self):
        p={"scores":dict(self.payload["scores"],sql=101)}
        with self.assertRaises(ValueError): score(p)
    def test_priority_gap(self):
        p={"scores":dict(self.payload["scores"],python=45)}
        self.assertEqual([x["id"] for x in score(p)["priority_gaps"]],["python"])
if __name__=="__main__": unittest.main()
