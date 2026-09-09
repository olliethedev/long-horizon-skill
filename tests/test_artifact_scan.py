from pathlib import Path
import gzip
import io
import json
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'evals'))
from native_credentials_check import main, retry_scan, scan


class ArchivedCredentials(unittest.TestCase):
    def test_scan_finds_synthetic_credentials_in_plain_and_compressed_evidence(self):
        token = b'synthetic-evaluation-credential-1234567890'
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'decision.md').write_bytes(b'clean decision')
            self.assertEqual(scan(root, {token})[1], [])
            (root / 'trace.json').write_bytes(b'{"token":"' + token + b'"}')
            (root / 'trace.json.gz').write_bytes(gzip.compress(token))
            (root / 'link').symlink_to('/nonexistent/' + token.decode())
            with tarfile.open(root / 'inputs.tar.gz', 'w:gz') as archive:
                member = tarfile.TarInfo('retained/note.md')
                member.size = len(token)
                archive.addfile(member, io.BytesIO(token))
                link = tarfile.TarInfo('retained/link')
                link.type = tarfile.SYMTYPE
                link.linkname = '/nonexistent/' + token.decode()
                archive.addfile(link)
            _, hits = scan(root, {token})
            paths = {hit['artifact'] for hit in hits}
            self.assertIn('trace.json', paths)
            self.assertIn('trace.json.gz:decompressed', paths)
            self.assertIn('inputs.tar.gz:retained/note.md', paths)
            self.assertIn('link:link-target', paths)
            self.assertIn('inputs.tar.gz:link-target', paths)
            self.assertNotIn('decision.md', paths)
            self.assertNotIn(token.decode(), json.dumps(hits))

    def test_retry_reads_completed_gzip_and_retains_observed_credentials(self):
        token = b'synthetic-refreshed-credential-1234567890'
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            trace = root / 'trace.gz'
            complete = gzip.compress(token)
            trace.write_bytes(complete[:-8])
            observed = set()
            # Complete the real file during the retry pause. The credential is
            # available only in the first sample, before the successful scan.
            with patch('native_credentials_check.collect', side_effect=[{token}, set()]), \
                 patch('native_credentials_check.time.sleep', side_effect=lambda _: trace.write_bytes(complete)) as pause:
                result, errors = retry_scan(root, observed, attempts=2, retry_delay_seconds=0.01)
            self.assertEqual(pause.call_count, 1)
            self.assertEqual(errors[0]['exception_type'], 'EOFError')
            self.assertIsNotNone(result)
            self.assertIn('trace.gz:decompressed', {hit['artifact'] for hit in result[1]})
            self.assertIn(token, observed)
            self.assertNotIn(token.decode(), json.dumps([errors, result]))

    def test_persistent_corruption_fails_visibly_without_a_clean_result(self):
        complete = gzip.compress(b'clean')
        # DEFLATE block type 3 is invalid; keep the gzip header and trailer.
        corrupt_body = complete[:10] + bytes([complete[10] | 6]) + complete[11:]
        for content, exception_type in ((complete[:-8], 'EOFError'), (corrupt_body, 'error')):
            with self.subTest(exception_type=exception_type), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                artifacts = root / 'artifacts'
                artifacts.mkdir()
                (artifacts / 'trace.gz').write_bytes(content)
                (root / 'manifest.json').write_text('{"finished_at":"synthetic"}')
                output = root / 'scan-result.json'
                # Exercise main's real bounded-retry failure path, removing only
                # the pauses and host credential reads from this deterministic test.
                with patch('sys.argv', ['scanner', '--matrix', str(root), '--artifacts', str(artifacts), '--output', str(output)]), \
                     patch('native_credentials_check.collect', return_value=set()), \
                     patch('native_credentials_check.time.sleep') as pause, \
                     patch('sys.stdout', new_callable=io.StringIO) as stdout:
                    self.assertEqual(main(), 2)
                report = json.loads(output.read_text())
                self.assertFalse(report['scan_complete'])
                self.assertEqual(len(report['scan_errors']), 60)
                self.assertEqual({error['exception_type'] for error in report['scan_errors']}, {exception_type})
                self.assertEqual(report['samples'], 61)
                self.assertEqual(pause.call_count, 59)
                self.assertNotIn('matches', report)
                self.assertNotIn('artifact_streams_scanned', report)
                self.assertIn('no clean result reported', stdout.getvalue())


if __name__ == '__main__':
    unittest.main()
