import hashlib, json, tempfile, unittest, zipfile
from pathlib import Path
from portfolio_release_candidate_v544.src.release_candidate import manifest_check, scan, build

class ReleaseCandidateTests(unittest.TestCase):
    def fixture(self, root):
        p=root/'project'; p.mkdir(); (p/'src').mkdir(); (p/'src'/'a.py').write_text('print(1)\n')
        h=hashlib.sha256((p/'src'/'a.py').read_bytes()).hexdigest(); (p/'SOURCE_MANIFEST.json').write_text(json.dumps({'src/a.py':h}))
        (p/'tests').mkdir(); (p/'tests'/'test_a.py').write_text('import unittest\nclass T(unittest.TestCase):\n def test_ok(self): self.assertEqual(1,1)\n')
        # No project runner is needed for manifest/scan unit tests.
        return p
    def test_manifest_passes(self):
        with tempfile.TemporaryDirectory() as td: self.assertTrue(manifest_check(self.fixture(Path(td)))['ok'])
    def test_manifest_detects_modified_file(self):
        with tempfile.TemporaryDirectory() as td:
            p=self.fixture(Path(td)); (p/'src'/'a.py').write_text('changed')
            self.assertFalse(manifest_check(p)['ok'])
    def test_scan_detects_credential_marker(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td); (p/'x.txt').write_text('token ghp_abcdefghijklmnopqrstuvwxyz123456')
            self.assertTrue(any('credential' in x for x in scan(p)))
    def test_scan_detects_database_artifact(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td); (p/'tmp.db').write_bytes(b'x')
            self.assertTrue(any('forbidden file type' in x for x in scan(p)))
    def test_scan_clean_source(self):
        with tempfile.TemporaryDirectory() as td: self.assertEqual(scan(self.fixture(Path(td))),[])
    def test_manifest_missing_file(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td); (p/'SOURCE_MANIFEST.json').write_text('{"missing.csv":"'+'0'*64+'"}')
            self.assertFalse(manifest_check(p)['ok'])

if __name__=='__main__': unittest.main()
