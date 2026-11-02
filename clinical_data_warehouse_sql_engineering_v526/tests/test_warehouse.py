import importlib.util,sys,tempfile,subprocess,json,sqlite3,unittest
from pathlib import Path
HERE=Path(__file__).resolve().parents[1]
ROOT=HERE.parent
SPEC=importlib.util.spec_from_file_location("warehouse",HERE/"scripts/build_warehouse.py")
warehouse=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(warehouse)
class WarehouseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=ROOT/"healthcare_data_engineering_interoperability_v525"/"outputs"/"demo"
        if not cls.source.exists():
            subprocess.run([sys.executable,str(ROOT/"healthcare_data_engineering_interoperability_v525/scripts/fhir_analytics_etl.py"),
             "--input",str(ROOT/"healthcare_data_engineering_interoperability_v525/data/synthetic_hospital_fhir_bundle.json"),
             "--config",str(ROOT/"healthcare_data_engineering_interoperability_v525/templates/pipeline_config.json"),
             "--output",str(cls.source)],check=True,capture_output=True)
    def test_star_schema_counts_and_integrity(self):
        with tempfile.TemporaryDirectory() as d:
            db=Path(d)/"warehouse.sqlite"; warehouse.run(self.source,db)
            con=sqlite3.connect(db)
            counts={t:con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in
             ["dim_patient","dim_encounter","fact_observation","fact_medication_request","mart_encounter_summary","mart_patient_cohort"]}
            self.assertEqual(counts,{"dim_patient":5,"dim_encounter":6,"fact_observation":12,"fact_medication_request":5,"mart_encounter_summary":6,"mart_patient_cohort":4})
            self.assertEqual(con.execute("PRAGMA integrity_check").fetchone()[0],"ok")
            self.assertEqual(con.execute("PRAGMA foreign_key_check").fetchall(),[])
            con.close()
    def test_fact_grain_and_no_fanout(self):
        with tempfile.TemporaryDirectory() as d:
            db=Path(d)/"w.sqlite"; warehouse.run(self.source,db)
            con=sqlite3.connect(db)
            self.assertEqual(con.execute("SELECT SUM(observation_count) FROM mart_encounter_summary").fetchone()[0],12)
            self.assertEqual(con.execute("SELECT SUM(medication_request_count) FROM mart_encounter_summary").fetchone()[0],5)
            self.assertEqual(con.execute("SELECT COUNT(*) FROM fact_observation").fetchone()[0],12)
            con.close()
    def test_window_query(self):
        with tempfile.TemporaryDirectory() as d:
            db=Path(d)/"w.sqlite"; warehouse.run(self.source,db)
            con=sqlite3.connect(db)
            q="""SELECT patient_id,ROW_NUMBER() OVER(PARTITION BY patient_id ORDER BY encounter_date) n FROM mart_encounter_summary"""
            self.assertEqual(con.execute(q).fetchall().__len__(),6)
            con.close()
    def test_manifest(self):
        with tempfile.TemporaryDirectory() as d:
            db=Path(d)/"w.sqlite"; warehouse.run(self.source,db)
            m=json.loads((Path(d)/"warehouse_manifest.json").read_text())
            self.assertEqual(m["integrity_check"],"ok")
            self.assertEqual(m["foreign_key_violations"],0)
            self.assertTrue(m["sha256"])
    def test_missing_staging_input_fails(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(FileNotFoundError): warehouse.run(Path(d),Path(d)/"w.sqlite")
if __name__=="__main__":
    import unittest
    unittest.main()
