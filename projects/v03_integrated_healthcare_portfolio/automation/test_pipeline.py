"""Unit tests for the synthetic healthcare analytics pipeline."""
import unittest
import pandas as pd
from healthcare_pipeline import validate_encounters, filter_period, summarize

class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            "encounter_id": ["E1", "E2", "E3"],
            "patient_id": ["P1", "P1", "P2"],
            "department_id": ["D1", "D1", "D2"],
            "admission_date": ["2026-01-01", "2026-02-01", "2026-04-01"],
            "encounter_type": ["IPD", "OPD", "IPD"],
            "systolic_bp": ["120", "", "140"]
        })

    def test_unique_encounters(self):
        clean = validate_encounters(self.df)
        self.assertTrue(clean["encounter_id"].is_unique)

    def test_duplicate_encounter_rejected(self):
        bad = self.df.copy()
        bad.loc[1, "encounter_id"] = "E1"
        with self.assertRaisesRegex(ValueError, "unique"):
            validate_encounters(bad)

    def test_half_open_date_window(self):
        clean = validate_encounters(self.df)
        cohort = filter_period(clean, "2026-01-01", "2026-04-01")
        self.assertEqual(cohort["encounter_id"].tolist(), ["E1", "E2"])

    def test_invalid_date_range_rejected(self):
        clean = validate_encounters(self.df)
        with self.assertRaisesRegex(ValueError, "earlier"):
            filter_period(clean, "2026-04-01", "2026-01-01")

    def test_missing_sbp_preserved(self):
        clean = validate_encounters(self.df)
        self.assertEqual(int(clean["systolic_bp"].isna().sum()), 1)

    def test_department_summary_reconciles(self):
        clean = validate_encounters(self.df)
        cohort = filter_period(clean, "2026-01-01", "2026-04-01")
        dept = pd.DataFrame({"department_id":["D1","D2"],"department_name":["Cardiology","Medicine"]})
        summary, metrics = summarize(cohort, dept)
        self.assertEqual(metrics["cohort_encounters"], 2)
        self.assertEqual(metrics["department_encounter_sum"], 2)
        self.assertEqual(metrics["sbp_missing"], 1)

    def test_duplicate_department_lookup_rejected(self):
        clean = validate_encounters(self.df)
        dept = pd.DataFrame({"department_id":["D1","D1"],"department_name":["A","B"]})
        with self.assertRaisesRegex(ValueError, "unique"):
            summarize(clean, dept)

if __name__ == "__main__":
    unittest.main(verbosity=2)
