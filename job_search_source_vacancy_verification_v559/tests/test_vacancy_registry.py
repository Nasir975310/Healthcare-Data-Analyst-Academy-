import sys, tempfile, unittest, csv
from pathlib import Path
from datetime import date
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from vacancy_registry import canonical_url, read_registry, analyse, FIELDS

class RegistryTests(unittest.TestCase):
    def test_tracking_params_removed_and_host_normalised(self):
        self.assertEqual(canonical_url("HTTPS://Example.com/jobs/1?utm_source=x&b=2"),
                         canonical_url("https://example.com/jobs/1?b=2"))
    def test_duplicate_source_urls_detected(self):
        rows=[dict(zip(FIELDS, ["1","A","R","","","https://x.test/job/1?utm_source=a","https://x.test","2026-01-01","","","","","yes","yes","yes","yes","yes","","verified"])),
              dict(zip(FIELDS, ["2","A","R","","","https://x.test/job/1","https://x.test","2026-01-01","","","","yes","yes","yes","yes","yes","","verified"]))]
        report=analyse(rows,date(2026,1,2))
        self.assertEqual(report["duplicate_url_groups"], [["1","2"]])
    def test_deadline_expired(self):
        row=dict(zip(FIELDS, ["1","A","R","","","https://x.test/job","https://x.test","2026-01-01","2026-01-02","","","","yes","yes","yes","yes","yes","","verified"]))
        self.assertTrue(analyse([row],date(2026,1,3))["assessments"][0]["expired_as_of_review_date"])
    def test_unknown_checks_block_human_review_ready(self):
        row=dict(zip(FIELDS, ["1","A","R","","","https://x.test/job","https://x.test","2026-01-01","","","","unknown","yes","yes","yes","yes","","reviewing"]))
        self.assertFalse(analyse([row],date(2026,1,2))["assessments"][0]["eligible_for_human_final_review"])
    def test_invalid_stage_rejected(self):
        row={k:"" for k in FIELDS}; row.update({"vacancy_id":"1","employer":"A","role":"R","source_url":"https://x.test/job","employer_official_url":"https://x.test","date_found":"2026-01-01","employer_domain_checked":"yes","vacancy_on_official_site":"yes","recruiter_identity_checked":"yes","no_upfront_fee_confirmed":"yes","privacy_request_checked":"yes","status":"magic"})
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"x.csv"
            with p.open("w",newline="") as f:
                w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerow(row)
            with self.assertRaises(ValueError): read_registry(p)
    def test_unsafe_scheme_rejected(self):
        row=dict(zip(FIELDS, ["1","A","R","","","javascript:alert(1)","https://x.test","2026-01-01","","","","yes","yes","yes","yes","yes","","new"]))
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"x.csv"
            with p.open("w",newline="") as f:
                w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerow(row)
            with self.assertRaises(ValueError): read_registry(p)
if __name__=="__main__": unittest.main()
