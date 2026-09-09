import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HELPER = Path(__file__).resolve().parents[1] / 'skills/long-horizon/scripts/history.py'


class HistoryCLI(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def call(self, *args):
        return subprocess.run([sys.executable, str(HELPER), *map(str, args)],
                              text=True, capture_output=True)

    def test_bounded_search_retains_later_correction_and_source_identity(self):
        source = self.root / 'actions.jsonl'
        source.write_text('\n'.join(['Routine unrelated observation.'] * 200 +
            ['Compact offer deployed: receipt D-7.',
             'Compact offer correction: refunds reverse the gain; receipt A-19.']) + '\n')
        before = source.read_bytes()
        result = self.call('search', self.root, 'compact offer', '--limit', '1')
        self.assertEqual(result.returncode, 0, result.stderr)
        page = json.loads(result.stdout)
        self.assertEqual([(m['path'], m['line']) for m in page['matches']], [('actions.jsonl', 201)])
        self.assertIsNotNone(page['next_cursor'])
        next_page = json.loads(self.call('search', self.root, 'compact offer',
                                        '--limit', '1', '--cursor', page['next_cursor']).stdout)
        self.assertIn('refunds reverse the gain', next_page['matches'][0]['text'])
        self.assertLess(len(result.stdout.encode()), 20000)
        self.assertEqual(source.read_bytes(), before)

    def test_cursor_rejects_history_changes(self):
        source = self.root / 'history.md'
        source.write_text('offer deployed\noffer failed\n')
        cursor = json.loads(self.call('search', self.root, 'offer', '--limit', '1').stdout)['next_cursor']
        source.write_text('offer deployed\noffer corrected\nnew evidence\n')
        response = self.call('search', self.root, 'offer', '--cursor', cursor)
        self.assertEqual(response.returncode, 2)
        self.assertIn('changed', response.stdout.lower())

    def test_cursor_rejects_same_size_correction_with_preserved_timestamps(self):
        source = self.root / 'history.md'
        source.write_text('offer failed\noffer review\n')
        original = source.stat()
        cursor = json.loads(self.call('search', self.root, 'offer', '--limit', '1').stdout)['next_cursor']
        replacement = self.root / 'replacement'
        replacement.write_text('offer passed\noffer review\n')
        os.utime(replacement, ns=(original.st_atime_ns, original.st_mtime_ns))
        replacement.replace(source)
        response = self.call('search', self.root, 'offer', '--limit', '1', '--cursor', cursor)
        self.assertEqual(response.returncode, 2, response.stdout)
        self.assertIn('changed', response.stdout.lower())

    def test_read_refuses_traversal_symlinks_and_special_files(self):
        product = self.root / 'product'
        product.mkdir()
        (self.root / 'private.md').write_text('SECRET_OTHER_PRODUCT')
        (product / 'link.md').symlink_to(self.root / 'private.md')
        os.mkfifo(product / 'pipe')
        for path in ['../private.md', str(self.root / 'private.md'), 'link.md', 'pipe']:
            with self.subTest(path=path):
                result = self.call('read', product, path)
                self.assertEqual(result.returncode, 2)
                self.assertNotIn('SECRET_OTHER_PRODUCT', result.stdout)

    def test_search_does_not_follow_links_into_another_product(self):
        outside = self.root / 'other-product'
        outside.mkdir()
        (outside / 'private.md').write_text('compact offer SECRET_OTHER_PRODUCT')
        product = self.root / 'product'
        product.mkdir()
        (product / 'linked.md').symlink_to(outside / 'private.md')
        (product / 'linked-directory').symlink_to(outside, target_is_directory=True)
        result = self.call('search', product, 'compact offer')
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertNotIn('SECRET_OTHER_PRODUCT', result.stdout)
        page = json.loads(result.stdout)
        self.assertEqual(page['matches'], [])
        self.assertEqual(page['skipped']['symlinks'], 2)

    def test_source_pages_preserve_unicode_and_reject_changed_versions(self):
        source = self.root / 'evidence.md'
        source.write_text('部署 — request date unknown; retrieved 2026-09-08.\n')
        first = self.call('read', self.root, 'evidence.md', '--bytes', '7')
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        page = json.loads(first.stdout)
        text = page['text']
        offset = page['next_offset']
        while offset is not None:
            part = json.loads(self.call('read', self.root, 'evidence.md', '--bytes', '7',
                '--offset', offset, '--version', page['version']).stdout)
            text += part['text']
            offset = part['next_offset']
        self.assertEqual(text, source.read_text())
        source.write_text('Changed evidence; no such observation window.')
        stale = self.call('read', self.root, 'evidence.md', '--version', page['version'])
        self.assertNotEqual(stale.returncode, 0)
        self.assertIn('changed', stale.stdout.lower())

    def test_oversized_records_are_reported_without_hiding_later_matches(self):
        (self.root / 'history.jsonl').write_text('x' * 100000 + ' compact offer\nCompact offer corrected.\n')
        result = self.call('search', self.root, 'compact offer')
        self.assertEqual(result.returncode, 0, result.stdout)
        page = json.loads(result.stdout)
        self.assertEqual(page['skipped']['long_lines'], 1)
        self.assertEqual(page['matches'][0]['line'], 2)
        self.assertEqual(page['skipped_examples'][0]['path'], 'history.jsonl')
        self.assertLess(len(result.stdout.encode()), 20000)

    def test_unicode_casefolding_does_not_lose_the_matched_excerpt(self):
        (self.root / 'history.md').write_text('ß' * 1000 + ' compact offer corrected\n')
        response = self.call('search', self.root, 'compact offer')
        self.assertIn('compact offer corrected', json.loads(response.stdout)['matches'][0]['text'])

    @unittest.skipIf(os.geteuid() == 0, 'Root can traverse mode-000 directories')
    def test_unreadable_subtree_cannot_be_reported_as_exhausted_history(self):
        private = self.root / 'restricted'
        private.mkdir()
        (private / 'record.md').write_text('compact offer lost')
        private.chmod(0)
        try:
            response = self.call('search', self.root, 'compact offer')
            self.assertEqual(response.returncode, 2, response.stdout)
            self.assertIn('error', json.loads(response.stdout))
        finally:
            private.chmod(0o700)
