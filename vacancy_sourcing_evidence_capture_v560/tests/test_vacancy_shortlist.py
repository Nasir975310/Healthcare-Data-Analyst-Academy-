import sys, tempfile, unittest, csv, json
from pathlib import Path
from datetime import date
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from vacancy_shortlist import canonical_url, duplicate_groups, load_rows, profile_match, build_report, FIELDS

class ShortlistTests(unittest.TestCase):
    def setUp(self):
        self.rows=[
            dict(zip(FIELDS,["A","Org","Junior Healthcare Data Analyst","","","https://x.test/job/1?utm_source=a","https://x.test","","2026-01-01","2026-02-01","India","Remote","Full-time","0","","SQL; Excel; Healthcare","Python","healthcare data quality","","","","shortlisted"])),
            dict(zip(FIELDS,["B","Org","Junior Healthcare Data Analyst","","","https://x.test/job/1","https://x.test","","2026-01-01","2026-02-01","India","Remote","Full-time","0","","SQL; Excel; Healthcare","","healthcare reporting","","","","new"]))
        ]
        self.profile={"skills":["Excel","Healthcare"],"domains":["Healthcare"],"years_experience":0}
    def test_url_tracking_removed(self):
        self.assertEqual(canonical_url("https://X.test/job/1?utm_source=a"),canonical_url("https://x.test/job/1"))
    def test_duplicates_detected(self):
        self.assertEqual(duplicate_groups(self.rows),[["A","B"]])
    def test_required_skill_gap_reported(self):
        m=profile_match(self.rows[0],self.profile)
        self.assertIn("SQL",m["required_skills_not_in_profile"])
        self.assertIn("Excel",m["profile_skill_matches"])
    def test_expired_deadline(self):
        r=build_report(self.rows,self.profile,date(2026,3,1))
        self.assertTrue(all(x["expired"] for x in r["items"]))
    def test_negative_experience_rejected(self):
        self.rows[0]["required_experience_years"]="-1"
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"x.csv"
            with p.open("w",newline="") as f:
                w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(self.rows)
            with self.assertRaises(ValueError):load_rows(p)
    def test_invalid_status_rejected(self):
        self.rows[0]["status"]="maybe"
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"x.csv"
            with p.open("w",newline="") as f:
                w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(self.rows)
            with self.assertRaises(ValueError):load_rows(p)
if __name__=="__main__":unittest.main()
