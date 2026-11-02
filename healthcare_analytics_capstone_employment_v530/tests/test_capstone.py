import sys, unittest, json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
import run_capstone
class CapstoneTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.result=run_capstone.main()
    def test_synthetic_flag(self): self.assertTrue(self.result["synthetic_data"])
    def test_expected_counts(self):
        k=self.result["kpis"]
        self.assertEqual(k["patient_count"],8)
        self.assertEqual(k["encounter_count"],13)
        self.assertEqual(k["medication_orders"],16)
    def test_orphan_detected(self):
        self.assertEqual(self.result["quality"]["encounters_with_unknown_patient"],["EN013"])
    def test_observation_counts(self): self.assertEqual(len(run_capstone.load("observations.csv")),24)
    def test_sqlite_integrity(self):
        self.assertEqual(self.result["sqlite"]["integrity_check"],"ok")
        self.assertEqual(self.result["sqlite"]["foreign_key_violations"],0)
if __name__=="__main__": unittest.main()
