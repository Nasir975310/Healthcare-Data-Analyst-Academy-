import sys, unittest, json, sqlite3
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
import run_project
class PracticumTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.result=run_project.main()
    def test_source_counts(self):
        q=self.result["quality"]["source_rows"]
        self.assertEqual(q,{"patients":30,"encounters":91,"observations":170,"medications":129})
    def test_orphan_detected(self):
        self.assertEqual(self.result["quality"]["encounters_with_unknown_patient"],["E0091"])
    def test_orphan_rejected_from_curated(self):
        c=self.result["quality"]["curation"]
        self.assertEqual(c["rejected_encounters"],1)
        self.assertEqual(c["accepted_encounters"],90)
    def test_warehouse_integrity(self):
        w=self.result["quality"]["warehouse"]
        self.assertEqual(w["integrity_check"],"ok")
        self.assertEqual(w["foreign_key_violations"],0)
    def test_kpis_consistent(self):
        k=self.result["kpis"]
        self.assertEqual(k["source_encounters"],91)
        self.assertEqual(k["curated_encounters"],90)
        self.assertEqual(k["completed_encounters"]+k["cancelled_encounters"]+k["scheduled_encounters"],90)
    def test_outputs_exist(self):
        out=Path(run_project.OUT)
        for f in ["data_quality_report.json","kpi_summary.json","monthly_encounters.csv","medication_class_utilization.csv","source_manifest.json","hospital_analytics.sqlite"]:
            self.assertTrue((out/f).exists(),f)
if __name__=="__main__": unittest.main()
