import gzip
import io
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'evals'))
from native_harnesses import Harness
from workflow_runner import ROOT, SOURCES, STOP_BETWEEN_CASES, run_session
from workflow_world import initial


class WorkflowEvidence(unittest.TestCase):
    def test_generated_memory_survives_postprocessing_and_unsupported_nodes(self):
        for failure in ('fifo', 'parsing', 'partial-gzip'):
            with self.subTest(failure=failure), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                (root / 'evals/runs').mkdir(parents=True)
                for name in ('workflow_api.md', 'workflow_client.py'):
                    shutil.copyfile(ROOT / 'evals' / name, root / 'evals' / name)
                product = root / 'product'
                product.mkdir()
                output = root / 'session'

                def fake_capture(command, prompt, destination, timeout):
                    workspace = Path(command[1])
                    (workspace / 'product/memory.md').write_text('Original agent memory')
                    (workspace / 'product/link').symlink_to('/absent/synthetic-target')
                    if failure == 'fifo':
                        os.mkfifo(workspace / 'product/pipe')
                    if failure == 'partial-gzip':
                        (workspace / 'product/partial.gz').write_bytes(gzip.compress(b'evidence')[:-8])
                    (workspace / 'work/decision.md').write_text('Original decision')
                    (destination / 'trace.jsonl.gz').write_bytes(gzip.compress(b'original trace'))
                    return {'exit_code': 0}

                STOP_BETWEEN_CASES.clear()
                with patch('workflow_runner.setup_home', side_effect=lambda harness, home: home.mkdir()), \
                     patch('workflow_runner.ROOT', root), \
                     patch('sys.stdout', new_callable=io.StringIO), \
                     patch('workflow_runner.sandbox', side_effect=lambda workspace, *args: ['/synthetic', str(workspace)]), \
                     patch('workflow_runner.probe', return_value={}), \
                     patch('workflow_runner.collect', return_value=set()), \
                     patch('workflow_runner.capture', side_effect=fake_capture), \
                     patch('workflow_runner.summarize', side_effect=ValueError('synthetic parser failure') if failure == 'parsing' else None,
                           return_value={}):
                    result = run_session(Harness('codex', Path('/bin/true'), {}), initial('revenue'), output,
                                         product, None, ['initial_owner_request'], None, 0, True, 30)
                self.assertEqual(result['infrastructure_error'], 'EOFError' if failure == 'partial-gzip' else 'ValueError')
                self.assertTrue(result['temporary_auth_home_removed'])
                self.assertEqual((output / 'product-after/memory.md').read_text(), 'Original agent memory')
                self.assertEqual(os.readlink(output / 'product-after/link'), '/absent/synthetic-target')
                self.assertEqual((output / 'work/decision.md').read_text(), 'Original decision')
                self.assertEqual(gzip.decompress((output / 'trace.jsonl.gz').read_bytes()), b'original trace')
                if failure == 'partial-gzip':
                    self.assertFalse(result['credential_scan']['complete'])
                    self.assertEqual(result['credential_scan']['exception_type'], 'EOFError')
                    self.assertGreaterEqual(result['credential_scan']['samples'], 1)
                    self.assertNotIn('matches', result['credential_scan'])
                    self.assertTrue((output / 'product-after/partial.gz').exists())
                else:
                    self.assertEqual(result['credential_scan']['matches'], [])
                if failure == 'fifo':
                    self.assertEqual(result['artifact_errors']['product-after'][0]['path'], 'pipe')
                    self.assertFalse((output / 'product-after/pipe').exists())
                STOP_BETWEEN_CASES.clear()

    def test_frozen_source_set_imports_without_repository(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name in SOURCES:
                shutil.copyfile(ROOT / 'evals' / name, root / name)
            result = subprocess.run([sys.executable, '-I', '-c',
                                     'import sys; sys.path.insert(0, sys.argv[1]); import workflow_runner', str(root)],
                                    cwd=root, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == '__main__':
    unittest.main()
