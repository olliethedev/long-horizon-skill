from pathlib import Path
import re
import shutil
import tempfile
import tomllib
import unittest

BUNDLE = Path(__file__).resolve().parents[1] / 'skills/long-horizon'


class InstalledBundle(unittest.TestCase):
    def test_copied_skill_has_all_references_and_templates_without_runtime_code(self):
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
            self.assertEqual(list(installed.rglob('*.py')), [])
            self.assertEqual(list(installed.rglob('*.sh')), [])
