import pathlib, subprocess, sys, unittest
HERE=pathlib.Path(__file__).resolve().parents[1]
class EmployerEvalTests(unittest.TestCase):
    def test_assessment_script_compiles(self):
        p=subprocess.run([sys.executable,"-m","py_compile",str(HERE/"scripts/run_assessment.py")])
        self.assertEqual(p.returncode,0)
    def test_portfolio_audit_compiles(self):
        p=subprocess.run([sys.executable,"-m","py_compile",str(HERE/"scripts/portfolio_audit.py")])
        self.assertEqual(p.returncode,0)
    def test_hard_gates_present(self):
        rubric=(HERE/"assessments/SCORING_RUBRIC.md").read_text()
        self.assertIn("Hard gates",rubric)
        self.assertIn("fabricated experience",rubric.lower())
    def test_challenge_has_manual_sections(self):
        challenge=(HERE/"assessments/TECHNICAL_CHALLENGE.md").read_text()
        for part in ["Part A","Part B","Part C","Part D"]:
            self.assertIn(part,challenge)
    def test_tracker_has_application_fields(self):
        header=(HERE/"templates/JOB_APPLICATION_TRACKER.csv").read_text().splitlines()[0]
        for field in ["company","role","date_applied","stage","next_action"]:
            self.assertIn(field,header)
if __name__=="__main__": unittest.main()
