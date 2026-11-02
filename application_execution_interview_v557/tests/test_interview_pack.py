import json, tempfile, unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from interview_pack import make_pack,write_outputs
P={'years_experience':0,'skills':['Excel','Healthcare','Research'],'evidence':{'Research':{'status':'DOCUMENTED','reference':'Thesis'}}}
class Tests(unittest.TestCase):
 def test_topics_and_gaps(self):
  x=make_pack('Junior role: SQL, Python, healthcare data quality and research.',P); self.assertIn('SQL',x['detected_topics']); self.assertIn('SQL',x['potential_skill_gaps'])
 def test_empty(self):
  with self.assertRaises(ValueError): make_pack(' ',P)
 def test_sensitive(self): self.assertTrue(any('SENSITIVE_REQUEST_RED_FLAG' in x for x in make_pack('Send OTP and Aadhaar before interview.',P)['risk_flags']))
 def test_experience(self): self.assertTrue(any('EXPERIENCE_GAP' in x for x in make_pack('Requires 5+ years experience.',P)['risk_flags']))
 def test_remote(self): self.assertTrue(any('REMOTE_CLAIM' in x for x in make_pack('Fully remote role.',P)['risk_flags']))
 def test_outputs(self):
  x=make_pack('SQL and Excel healthcare reporting.',P)
  with tempfile.TemporaryDirectory() as d:
   write_outputs(x,Path(d)); self.assertTrue((Path(d)/'interview_pack.md').exists()); self.assertEqual(json.loads((Path(d)/'interview_pack.json').read_text())['detected_topics'],x['detected_topics'])
if __name__=='__main__': unittest.main()
