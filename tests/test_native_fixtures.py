"""Verify exported evaluation evidence without model credentials or a scheduler."""
from pathlib import Path
import re
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'evals'))
from fixtures import cases as original_cases, materialize
from native_fixtures import cases


class ExportedEvidence(unittest.TestCase):
    def test_large_snapshots_keep_resolvable_sources_and_evidence_dates(self):
        # Criteria are deliberately kept outside the product snapshot supplied
        # to the agent. Their original-to-export mapping lets this check dates
        # independently of the opaque-ID implementation.
        date = re.compile(r'(?<![-/\w])\d{4}-\d{2}-\d{2}(?![-/\w])')
        for original, exported in zip(original_cases(record_count=0), cases(), strict=True):
            with self.subTest(domain=exported.name), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                materialize(exported, root)
                self.assertGreater(len(exported.files), 7000)
                self.assertGreater(sum(p.stat().st_size for p in root.rglob('*') if p.is_file()), 8_000_000)
                self.assertEqual(set(exported.files), {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()})
                for relative in exported.files:
                    content = (root / relative).read_text()
                    for reference in re.findall(r'history/[A-Za-z0-9_./-]+', content):
                        self.assertTrue((root / reference.rstrip('.,')).exists(), (relative, reference))
                for before, after in zip(original.criteria, exported.criteria, strict=True):
                    self.assertEqual(before.key, after.key)
                    for old_path, new_path in zip(before.sources, after.sources, strict=True):
                        self.assertTrue((root / new_path).is_file(), new_path)
                        self.assertEqual(date.findall(original.files[old_path]),
                                         date.findall((root / new_path).read_text()),
                                         (old_path, new_path))


if __name__ == '__main__':
    unittest.main()
