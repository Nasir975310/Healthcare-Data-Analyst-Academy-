import csv, json, unittest
from pathlib import Path
BASE=Path(__file__).resolve().parents[2]
DATA=BASE/"data"; OUT=BASE/"outputs"
def read_csv(p):
    with p.open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))
class ProjectDataTests(unittest.TestCase):
    def test_operations_key_unique(self):
        rows=read_csv(DATA/"operations_encounters.csv")
        keys=[r["encounter_id"] for r in rows]
        self.assertEqual(len(rows),1200)
        self.assertEqual(len(keys),len(set(keys)))
    def test_operations_chronology(self):
        rows=read_csv(DATA/"operations_encounters.csv")
        self.assertTrue(all(r["admission_date"]<=r["discharge_date"] for r in rows))
    def test_due_complete_and_plausible(self):
        rows=read_csv(DATA/"antihypertensive_due_cohort.csv")
        self.assertEqual(len(rows),500)
        self.assertTrue(all(18<=int(r["age_years"])<=110 for r in rows))
        self.assertTrue(all(60<=float(r["baseline_sbp_mmhg"])<=260 for r in rows))
    def test_pv_candidate_flags_not_dropped(self):
        rows=read_csv(DATA/"pharmacovigilance_cases.csv")
        self.assertEqual(len(rows),240)
        self.assertEqual(sum(int(r["duplicate_candidate_flag"]) for r in rows),3)
    def test_output_reconciliation(self):
        summary=json.loads((OUT/"operations_summary.json").read_text())
        self.assertEqual(summary["source_rows"],1200)
        self.assertEqual(summary["valid_encounters"],1200)
    def test_dashboard_files_exist(self):
        dash=BASE/"portfolio_publication"/"dashboards"
        for name in ["hospital_operations_dashboard.html","antihypertensive_due_dashboard.html","pharmacovigilance_quality_dashboard.html"]:
            self.assertTrue((dash/name).is_file())

    def test_workbench_fixtures_match_source_row_counts(self):
        wb=BASE/"interactive_workbench"/"data"
        expected={"operations_encounters.csv":1200,"antihypertensive_due_cohort.csv":500,"pharmacovigilance_cases.csv":240}
        for filename,count in expected.items():
            self.assertEqual(len(read_csv(wb/filename)),count)
    def test_workbench_metric_documentation_exists(self):
        self.assertTrue((BASE/"interactive_workbench"/"docs"/"metric_definitions.md").is_file())

if __name__=="__main__": unittest.main(verbosity=2)
