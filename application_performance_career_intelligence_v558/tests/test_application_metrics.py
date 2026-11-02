import sys, tempfile, unittest, csv, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from application_metrics import read_tracker, summarise, build_html, REQUIRED

class MetricsTests(unittest.TestCase):
    def setUp(self):
        self.rows = [
            dict(zip(REQUIRED, ["A","Org","Analyst","2026-01-01","site","screening","","","A","remote","",""])),
            dict(zip(REQUIRED, ["B","Org","Analyst","2026-01-02","site","interview","","","B","remote","",""])),
            dict(zip(REQUIRED, ["C","Org","Analyst","2026-01-03","site","rejected","Rejected","Experience","A","hybrid","",""])),
            dict(zip(REQUIRED, ["D","Org","Analyst","2026-01-04","site","offer","Offer","","B","remote","",""])),
            dict(zip(REQUIRED, ["E","Org","Analyst","2026-01-05","site","saved","","","A","unknown","",""])),
        ]
    def test_denominators_exclude_saved(self):
        s=summarise(self.rows)
        self.assertEqual(s["submitted_count"],4)
        self.assertEqual(s["response_count"],4)
        self.assertEqual(s["interview_count"],2)
        self.assertEqual(s["offer_count"],1)
        self.assertEqual(s["response_rate_pct"],100.0)
        self.assertEqual(s["interview_rate_pct"],50.0)
        self.assertEqual(s["offer_rate_pct"],25.0)
    def test_empty_rates_are_null(self):
        s=summarise([])
        self.assertIsNone(s["response_rate_pct"])
        self.assertEqual(s["application_count"],0)
    def test_duplicate_ids_rejected(self):
        self.rows[1]["application_id"]="A"
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"x.csv"
            with p.open("w",newline="") as f:
                w=csv.DictWriter(f,fieldnames=REQUIRED);w.writeheader();w.writerows(self.rows)
            with self.assertRaises(ValueError): read_tracker(p)
    def test_invalid_date_rejected(self):
        self.rows[0]["applied_date"]="yesterday"
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"x.csv"
            with p.open("w",newline="") as f:
                w=csv.DictWriter(f,fieldnames=REQUIRED);w.writeheader();w.writerows(self.rows)
            with self.assertRaises(ValueError): read_tracker(p)
    def test_html_escapes_user_content(self):
        self.rows[0]["employer"]="<script>alert(1)</script>"
        s=summarise(self.rows); page=build_html(s)
        self.assertNotIn("<script>alert(1)</script>",page)
    def test_cv_counts(self):
        s=summarise(self.rows)
        self.assertEqual(s["cv_versions"]["B"]["offers"],1)

if __name__ == "__main__": unittest.main()
