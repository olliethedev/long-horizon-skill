import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest

BUNDLE = Path(__file__).resolve().parents[1] / 'skills/long-horizon'


class InstalledBundle(unittest.TestCase):
    def test_copied_skill_has_all_local_references_and_runs_without_the_repo(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            installed = root / 'installed'
            shutil.copytree(BUNDLE, installed, ignore=shutil.ignore_patterns('__pycache__'))
            for document in installed.rglob('*.md'):
                for reference in re.findall(r'\]\(([^)]+)\)', document.read_text()):
                    if '://' not in reference and not reference.startswith('#'):
                        self.assertTrue((document.parent / reference.split('#')[0]).exists(),
                                        f'{document.name}: {reference}')
            definition = tomllib.loads((installed / 'assets/task.toml').read_text())
            self.assertEqual(definition['work']['kind'], 'agent')
            self.assertEqual(definition['retention']['history'], 'forever')
            product = root / 'product'
            product.mkdir()
            (product / 'record.md').write_text('Trial D-2: corrected outcome remains inconclusive.\n')
            result = subprocess.run([sys.executable, str(installed / 'scripts/history.py'),
                'search', str(product), 'D-2'], cwd=product, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)['matches'][0]['path'], 'record.md')
