import gzip
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'evals'))
from recall import dump
from workflow_publish import archive, publication_scan, recover_gzip
from workflow_summary import summarize


class WorkflowPublication(unittest.TestCase):
    def test_a_compressed_credential_stops_publication(self):
        with tempfile.TemporaryDirectory() as temporary, patch('workflow_publish.collect', return_value=set()):
            root = Path(temporary)
            (root / 'trace.jsonl.gz').write_bytes(gzip.compress(('sk-' + 'A' * 48).encode()))
            with self.assertRaises(ValueError):
                publication_scan(root)

    def test_interrupted_gzip_is_labeled_partial_and_its_recovered_content_is_scanned(self):
        with tempfile.TemporaryDirectory() as temporary, patch('workflow_publish.collect', return_value=set()):
            root = Path(temporary)
            payload = ('sk-' + 'A' * 48).encode()
            raw = gzip.compress(payload)[:-5]
            self.assertEqual(recover_gzip(raw), (payload, False))
            (root / 'trace.jsonl.gz').write_bytes(raw)
            with self.assertRaises(ValueError):
                publication_scan(root)

    def test_archive_preserves_evidence_and_symlinks_without_rewriting_sources(self):
        with tempfile.TemporaryDirectory() as temporary, patch('workflow_publish.collect', return_value=set()):
            root = Path(temporary)
            source, output = root / 'original', root / 'publication'
            (source / 'sources').mkdir(parents=True)
            output.mkdir()
            dump(source / 'manifest.json', {'finished_at': 'test', 'source_hashes': {}, 'live': True})
            (source / 'evidence.md').write_text('Original observation')
            (source / 'memory.md').symlink_to('evidence.md')
            result = archive(source, output)
            self.assertEqual(result['artifact_hashes']['memory.md'], 'symlink:evidence.md')
            self.assertEqual(result['artifact_hashes']['evidence.md'], hashlib.sha256(b'Original observation').hexdigest())
            self.assertTrue(result['publication_scan']['complete'])
            with self.assertRaises(FileExistsError):
                archive(source, output)

    def fixture(self, root):
        original, continuation = root / 'original', root / 'continuation'
        case = {'harness': 'codex', 'domain': 'weekly-product', 'arm': 'skill'}
        dump(original / 'manifest.json', {'live': True, 'finished_at': 'test', 'schedule': [case],
                                         'skill_tree': 'test', 'harnesses': []})
        dump(continuation / 'manifest.json', {'live': True, 'finished_at': 'test',
            'source_manifest_sha256': hashlib.sha256((original / 'manifest.json').read_bytes()).hexdigest(),
            'maximum_total_launch_attempts': 50, 'reserved_launch_slots': 1})
        for index, batch in enumerate((original, continuation)):
            folder = batch / 'trajectories/codex/weekly-product/skill'
            (folder / 'product').mkdir(parents=True)
            session = folder / 'sessions' / f'{index:02d}'
            (session / 'product-before').mkdir(parents=True)
            (session / 'product-after').mkdir()
            dump(session / 'manifest.json', {'index': index, 'finished_at': 'test', 'model_launch_attempted': True,
                'credential_scan': {'complete': True, 'matches': []}, 'product_before': {}, 'product_after': {},
                'day': index * 7, 'exit_code': 0, 'elapsed_seconds': 2, 'temporary_auth_home_removed': True,
                'isolation_probe': {'isolated': True}, 'fresh_session': True, 'model_or_effort_override': False})
            dump(session / 'trace-summary.json', {})
            (session / 'trace.jsonl.gz').write_bytes(gzip.compress(b''))
            dump(folder / 'trajectory.json', {'actual_sessions': 1, 'previous_sessions': index,
                'stop_reason': 'owner_session_budget_exhausted',
                'state': {'events': [], 'scheduler': {'day': 14}, 'revision': 1, 'config': {}}})
        return original, continuation

    def test_continuation_counts_unique_sessions_and_keeps_censoring_visible(self):
        with tempfile.TemporaryDirectory() as temporary, patch('workflow_summary.usage_totals', return_value={}), \
                patch('workflow_summary.session_tools', return_value=([], {})):
            original, continuation = self.fixture(Path(temporary))
            result = summarize(original, continuation)
            self.assertEqual(result['total_native_sessions'], 2)
            self.assertEqual(result['coverage'], {'resource_censored': 1})
            self.assertEqual(result['trajectories'][0]['days'], [0, 7])
            self.assertEqual(result['usage_by_trajectory']['codex/weekly-product/skill']['totals']['elapsed_seconds'], 4)
            path = continuation / 'trajectories/codex/weekly-product/skill/sessions/01/manifest.json'
            data = json.loads(path.read_text())
            data['index'] = 0
            dump(path, data)
            with self.assertRaises(ValueError):
                summarize(original, continuation)


if __name__ == '__main__':
    unittest.main()
