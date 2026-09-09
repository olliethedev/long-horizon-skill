from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest

REPORT = Path(__file__).resolve().parents[1] / 'evals/native_report.py'


class ReviewedArtifacts(unittest.TestCase):
    def test_report_preserves_missing_usage_and_detects_changed_decision(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            session = root / 'sessions/codex/example/native-tools'
            (session / 'work').mkdir(parents=True)
            decision = session / 'work/decision.md'
            decision.write_text('The evidence remains inconclusive.\n')
            manifest = {'harness': 'codex', 'case': 'example', 'arm': 'native-tools',
                        'exit_code': 0, 'decision_present': True, 'elapsed_seconds': 1.0}
            review = {'semantic_success': True, 'material_contradictions': [],
                      'criteria': [{'key': 'uncertainty', 'verdict': 'pass'}],
                      'decision_sha256': hashlib.sha256(decision.read_bytes()).hexdigest(),
                      'review_notes': 'One supplied source; limited coverage.'}
            summary = {'usage_events': [{'type': 'turn.completed',
                                        'usage': {'input_tokens': 25, 'output_tokens': 0}}]}
            for name, value in [('manifest.json', manifest), ('manual-review.json', review),
                                ('trace-summary.json', summary)]:
                (session / name).write_text(json.dumps(value))
            result = subprocess.run([sys.executable, str(REPORT), str(root)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            row = json.loads((root / 'reviewed-results.json').read_text())['sessions'][0]
            self.assertEqual(row['input_tokens_reported'], 25)
            self.assertEqual(row['output_tokens_reported'], 0)
            self.assertIsNone(row.get('reasoning_tokens_reported'))
            self.assertIsNone(row.get('cached_input_tokens_reported'))
            self.assertEqual(row.get('review_notes'), review['review_notes'])
            decision.write_text('Changed after review.\n')
            changed = subprocess.run([sys.executable, str(REPORT), str(root)], capture_output=True, text=True)
            self.assertNotEqual(changed.returncode, 0)
            self.assertIn('Decision changed after manual review', changed.stderr)


if __name__ == '__main__':
    unittest.main()
