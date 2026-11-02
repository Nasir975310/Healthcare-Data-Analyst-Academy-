import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from jobfit import assess, DEFAULT_PROFILE
class JobFitTests(unittest.TestCase):
 def test_relevant_entry_role(self):
  r=assess('Junior Healthcare Data Analyst. PharmD preferred. SQL, Excel, Python, Power BI and data quality. Remote.')
  self.assertIn('Healthcare Data Analyst',r['role_families_detected']); self.assertTrue(0<=r['score_out_of_100']<=100)
 def test_empty_jd_rejected(self):
  with self.assertRaises(ValueError): assess('  ')
 def test_senior_role_penalty(self):
  a=assess('Junior clinical analyst healthcare SQL Excel')
  b=assess('Senior Lead clinical analyst healthcare SQL Excel; 8 years experience required')
  self.assertLess(b['score_out_of_100'],a['score_out_of_100'])
 def test_red_flags_detected(self):
  r=assess('Remote data analyst. Pay registration fee and share OTP on WhatsApp.')
  self.assertIn('upfront_fee',r['risk_flags']); self.assertIn('sensitive_data_request',r['risk_flags'])
 def test_empty_profile_skills_not_crash(self):
  r=assess('Healthcare data analyst SQL Python',{'skills':[],'education':'Other','experience_years':0,'remote_preference':True})
  self.assertEqual(r['matched_skill_groups'],[])
 def test_score_is_not_probability(self):
  r=assess('Healthcare reporting analyst Excel SQL')
  self.assertTrue(r['not_a_hiring_probability'])
 def test_no_invented_experience(self):
  r=assess('Data analyst requires 5 years experience',DEFAULT_PROFILE)
  self.assertEqual(r['profile_experience_years'],0)
if __name__=='__main__': unittest.main()
