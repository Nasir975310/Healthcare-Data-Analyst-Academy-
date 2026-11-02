import unittest
from portfolio_handoff_evidence_v543.src.handoff_gate import assess

class GateTests(unittest.TestCase):
 def complete(self):
  sha="a"*40
  return {"repository":{"url":"https://github.com/example/portfolio","default_branch":"main","commit_sha":sha,"visibility":"public"},
   "publication":{"published_at":"2026-11-02T10:00:00Z","release_tag":"v1.0.0","release_url":"https://github.com/example/portfolio/releases/tag/v1.0.0"},
   "clean_clone":{"clone_url":"https://github.com/example/portfolio.git","clone_commit_sha":sha,"clone_test_command":"python -m unittest discover","clone_test_exit_code":0,"clone_test_log_sha256":"b"*64},
   "ci":{"workflow_url":"https://github.com/example/portfolio/actions/workflows/ci.yml","run_id":"12345","conclusion":"success","run_commit_sha":sha},
   "review":{"reviewer":"Independent reviewer","reviewed_at":"2026-11-02","privacy_review":True,"provenance_review":True,"limitations_acknowledged":True}}
 def test_empty_is_not_run(self): self.assertEqual(assess({})["status"],"NOT_RUN")
 def test_partial_is_pending(self): self.assertEqual(assess({"repository":{"url":"https://github.com/x/y"}})["status"],"PENDING_EVIDENCE")
 def test_consistent_complete_evidence_passes(self): self.assertEqual(assess(self.complete())["status"],"PASS")
 def test_mismatched_commit_fails(self):
  d=self.complete();d["ci"]["run_commit_sha"]="c"*40
  self.assertEqual(assess(d)["status"],"REVIEW_REQUIRED")
 def test_failed_clone_fails(self):
  d=self.complete();d["clean_clone"]["clone_test_exit_code"]=1
  self.assertEqual(assess(d)["status"],"REVIEW_REQUIRED")
 def test_review_required(self):
  d=self.complete();d["review"]["privacy_review"]=False
  self.assertEqual(assess(d)["status"],"REVIEW_REQUIRED")
if __name__=="__main__":unittest.main()
