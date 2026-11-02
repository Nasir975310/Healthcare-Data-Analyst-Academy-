import json, tempfile, unittest
from pathlib import Path
from src.capture_local_evidence import sha256

class CaptureEvidenceTests(unittest.TestCase):
    def test_sha256_is_stable(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"x.txt"; p.write_text("healthcare analytics")
            self.assertEqual(sha256(p),sha256(p))
            self.assertEqual(len(sha256(p)),64)

    def test_hash_changes_when_content_changes(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"x.txt"; p.write_text("first")
            a=sha256(p); p.write_text("second")
            self.assertNotEqual(a,sha256(p))

if __name__=="__main__": unittest.main()
