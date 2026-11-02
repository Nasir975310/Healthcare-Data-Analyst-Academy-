import importlib.util, json, sqlite3, tempfile, unittest, csv
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
def load(name):
    spec=importlib.util.spec_from_file_location(name,BASE/'scripts'/f'{name}.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

class ExecutionLabTests(unittest.TestCase):
    def test_sql_assessment_real_fixture(self):
        m=load('run_sql_assessment')
        with tempfile.TemporaryDirectory() as td:
            db=Path(td)/'fixture.sqlite'
            result=m.run(db,Path(td)/'out')
            self.assertEqual(result['source_and_distinct_ids'][0]['source_rows'],16)
            self.assertEqual(result['source_and_distinct_ids'][0]['distinct_encounter_ids'],15)
            self.assertEqual(result['duplicate_ids'][0]['encounter_id'],'E015')
            self.assertTrue((Path(td)/'out'/'assessment_results.json').exists())

    def test_role_fit_is_bounded_and_discloses_limit(self):
        m=load('role_fit')
        ev=json.loads((BASE/'examples'/'candidate_evidence.json').read_text())
        result=m.evaluate((BASE/'examples'/'junior_healthcare_analyst_job.txt').read_text(),ev)
        self.assertGreaterEqual(result['evidence_fit_percent'],0)
        self.assertLessEqual(result['evidence_fit_percent'],100)
        self.assertIn('not an ATS score',result['interpretation'])

    def test_application_metrics_empty(self):
        m=load('application_metrics')
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'empty.csv';p.write_text('date,employer,role,status' + chr(10))
            result=m.summarize(p)
            self.assertEqual(result['tracked_rows'],0)
            self.assertIsNone(result['response_per_submitted_percent'])

    def test_application_metrics_counts_status_rows(self):
        m=load('application_metrics')
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'a.csv'
            with p.open('w', newline='') as f:
                writer=csv.writer(f)
                writer.writerow(['date','employer','role','status'])
                writer.writerow(['2026-01-01','A','Analyst','submitted'])
                writer.writerow(['2026-01-02','B','Analyst','interview'])
            result=m.summarize(p)
            self.assertEqual(result['tracked_rows'],2)
            self.assertEqual(result['interview_status_count'],1)

    def test_fixture_contains_no_real_patient_identifiers(self):
        with tempfile.TemporaryDirectory() as td:
            db=Path(td)/'fixture.sqlite'
            load('create_fixture').build(db)
            with sqlite3.connect(db) as con:
                ids=[r[0] for r in con.execute('select patient_id from encounters')]
        self.assertTrue(all(x.startswith('P') for x in ids))
        self.assertEqual(len(ids),16)

if __name__=='__main__': unittest.main()
