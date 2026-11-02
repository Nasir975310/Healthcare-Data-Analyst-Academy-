import json, pathlib, subprocess, sys, unittest
HERE=pathlib.Path(__file__).resolve().parents[1]
class DeploymentTests(unittest.TestCase):
    def test_compose_is_loopback_bound(self):
        s=(HERE/"docker-compose.yml").read_text()
        self.assertIn('127.0.0.1:55432:5432',s)
    def test_raw_mount_is_read_only(self):
        s=(HERE/"docker-compose.yml").read_text()
        self.assertIn('data/raw:/seed:ro',s)
    def test_postgres_curates_orphans_as_exceptions(self):
        s=(HERE/"docker/postgres/init/002_load_and_curate.sh").read_text()
        self.assertIn("'UNKNOWN_PATIENT'",s)
        self.assertIn("LEFT JOIN curated.dim_patient",s)
    def test_release_gate_requires_external_evidence(self):
        gate=(HERE/"scripts/release_gate.py").read_text()
        self.assertIn('else "PENDING"',gate)
        self.assertIn('"PARTIALLY_VERIFIED"',gate)
    def test_evidence_templates_are_pending(self):
        for n in ["powerbi_validation.template.json","github_publication.template.json"]:
            obj=json.loads((HERE/"evidence/templates"/n).read_text())
            self.assertEqual(obj["status"],"PENDING")
if __name__=="__main__":unittest.main()
