from pathlib import Path
import gzip
import io
import json
import sys
import tarfile
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'evals'))
from native_credentials_check import scan


class ArchivedCredentials(unittest.TestCase):
    def test_scan_finds_synthetic_credentials_in_plain_and_compressed_evidence(self):
        token = b'synthetic-evaluation-credential-1234567890'
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'decision.md').write_bytes(b'clean decision')
            self.assertEqual(scan(root, {token})[1], [])
            (root / 'trace.json').write_bytes(b'{"token":"' + token + b'"}')
            (root / 'trace.json.gz').write_bytes(gzip.compress(token))
            with tarfile.open(root / 'inputs.tar.gz', 'w:gz') as archive:
                member = tarfile.TarInfo('retained/note.md')
                member.size = len(token)
                archive.addfile(member, io.BytesIO(token))
            _, hits = scan(root, {token})
            paths = {hit['artifact'] for hit in hits}
            self.assertIn('trace.json', paths)
            self.assertIn('trace.json.gz:decompressed', paths)
            self.assertIn('inputs.tar.gz:retained/note.md', paths)
            self.assertNotIn('decision.md', paths)
            self.assertNotIn(token.decode(), json.dumps(hits))


if __name__ == '__main__':
    unittest.main()
