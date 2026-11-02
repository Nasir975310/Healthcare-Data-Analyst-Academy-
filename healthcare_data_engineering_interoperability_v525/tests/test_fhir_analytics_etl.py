import json, sys, tempfile, unittest
from pathlib import Path
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE/"scripts"))
import fhir_analytics_etl as etl

class FHIRPipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundle=json.loads((HERE/"data/synthetic_hospital_fhir_bundle.json").read_text())
        cls.cfg=json.loads((HERE/"templates/pipeline_config.json").read_text())
    def test_bundle_valid_and_counts(self):
        r=etl.validate_bundle(self.bundle)
        self.assertTrue(r["valid"],r["errors"])
        self.assertEqual(r["resource_counts"]["Patient"],5)
        self.assertEqual(r["resource_counts"]["Encounter"],6)
    def test_duplicate_id_rejected(self):
        b=json.loads(json.dumps(self.bundle))
        b["entry"].append(json.loads(json.dumps(b["entry"][0])))
        self.assertFalse(etl.validate_bundle(b)["valid"])
    def test_bad_date_rejected(self):
        b=json.loads(json.dumps(self.bundle))
        next(x["resource"] for x in b["entry"] if x["resource"].get("resourceType")=="Encounter")["period"]["start"]="2026-19-42"
        self.assertFalse(etl.validate_bundle(b)["valid"])
    def test_orphan_reference_rejected(self):
        b=json.loads(json.dumps(self.bundle))
        next(x["resource"] for x in b["entry"] if x["resource"].get("resourceType")=="Observation")["subject"]["reference"]="Patient/missing"
        self.assertFalse(etl.validate_bundle(b)["valid"])
    def test_flatten_and_mapping(self):
        t=etl.flatten(self.bundle,self.cfg)
        self.assertEqual(len(t["observations"]),12)
        self.assertTrue(all(x["mapped_concept"] for x in t["observations"]))
    def test_longitudinal_grain_no_cartesian_expansion(self):
        t=etl.flatten(self.bundle,self.cfg)
        rows=etl.longitudinal(t)
        self.assertEqual(len(rows),6)
        self.assertEqual(sum(x["observation_count"] for x in rows),12)
    def test_cohort_flow(self):
        t=etl.flatten(self.bundle,self.cfg)
        c=etl.build_cohort(t,self.cfg)
        self.assertEqual(c["eligible_encounters"],5)
        self.assertEqual(c["unique_patients"],4)
    def test_quality_reconciliation(self):
        t=etl.flatten(self.bundle,self.cfg)
        q=etl.quality(t)
        self.assertEqual(q["total_issues"],0)
    def test_end_to_end_cli(self):
        import subprocess
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)/"out"
            cmd=[sys.executable,str(HERE/"scripts/fhir_analytics_etl.py"),"--input",str(HERE/"data/synthetic_hospital_fhir_bundle.json"),
                 "--config",str(HERE/"templates/pipeline_config.json"),"--output",str(out)]
            subprocess.run(cmd,check=True,capture_output=True,text=True)
            for f in ["patients.csv","encounters.csv","observations.csv","medications.csv",
                      "patient_encounter_longitudinal.csv","hospital_analytics.sqlite","validation_report.json",
                      "data_quality_report.json","cohort_definition_and_flow.json","sha256_manifest.json"]:
                self.assertTrue((out/f).exists(),f)
if __name__=="__main__": unittest.main()
