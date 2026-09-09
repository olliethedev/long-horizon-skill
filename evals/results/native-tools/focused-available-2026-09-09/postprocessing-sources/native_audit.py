#!/usr/bin/env python3
"""Audit completed matrix identities, matched inputs, frozen sources and cleanup."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import tarfile
from typing import Any

from recall import aggregate_hash, dump, hashes, utc_now


def sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def audit(matrix: Path) -> dict[str, Any]:
    manifest = json.loads((matrix / 'manifest.json').read_text())
    failures: list[str] = []
    checks: dict[str, bool] = {}

    def check(label: str, passed: bool) -> None:
        checks[label] = passed
        if not passed:
            failures.append(label)

    check('finished', 'finished_at' in manifest)
    check('declared_criteria_unchanged', sha256((matrix / 'criteria.json').read_bytes()) == manifest['criteria_sha256'])
    check('executed_frozen_sources_unchanged', all(sha256((matrix / name).read_bytes()) == digest
                                                for name, digest in manifest['source_hashes'].items()))
    for arm, expected in manifest['bundles']['files'].items():
        check(f'bundle_{arm}_unchanged', hashes(matrix / 'bundles' / arm) == expected)
    check('published_git_archive_unchanged', sha256((matrix / 'bundles/published-git-archive.tar').read_bytes()) ==
          manifest['bundles']['published_git_archive_sha256'])
    archive_path = matrix / 'inputs.tar.gz'
    actual_inputs: dict[str, dict[str, str]] = {}
    if archive_path.is_file():
        with tarfile.open(archive_path) as archive:
            for member in archive:
                if member.isfile():
                    stream = archive.extractfile(member)
                    assert stream is not None
                    parts = Path(member.name).parts
                    if parts[0] == 'inputs':
                        parts = parts[1:]
                    actual_inputs.setdefault(parts[0], {})['/'.join(parts[1:])] = sha256(stream.read())
    elif (matrix / 'inputs').is_dir():
        actual_inputs = {p.name: hashes(p) for p in (matrix / 'inputs').iterdir() if p.is_dir()}
    check('all_raw_input_bytes_unchanged', actual_inputs == manifest['case_input_hashes'])

    scheduled = {(r['harness'], r['case'], r['arm']) for r in manifest['schedule']}
    sessions = sorted((matrix / 'sessions').glob('*/*/*'))
    found: set[tuple[str, str, str]] = set()
    prompts: dict[str, set[str]] = {}
    temp_paths: set[Path] = set()
    for session in sessions:
        item = json.loads((session / 'manifest.json').read_text())
        key = (item['harness'], item['case'], item['arm'])
        found.add(key)
        label = '/'.join(key)
        check(f'{label}:finished_and_operational', 'finished_at' in item and item.get('exit_code') == 0
              and item.get('decision_present') is True and not item.get('input_mutations')
              and not item.get('infrastructure_error') and item.get('temporary_auth_home_removed') is True)
        check(f'{label}:same_raw_input', item['input_tree_sha256'] == aggregate_hash(manifest['case_input_hashes'][item['case']]))
        expected_skill = manifest['bundles']['files'].get(item['arm'], {})
        check(f'{label}:same_skill_bytes', item.get('loaded_skill_hashes') == expected_skill)
        check(f'{label}:boundary_probes_passed', bool(item.get('isolation_probe')) and all(item['isolation_probe'].values()))
        check(f'{label}:no_model_or_effort_override', item.get('model_or_effort_override') is False)
        installed = next(h['installed_defaults'] for h in manifest['harnesses'] if h['name'] == item['harness'])
        check(f'{label}:installed_defaults_preserved', item.get('installed_defaults') == installed)
        prompt = (session / 'prompt.txt').read_text()
        check(f'{label}:prompt_unchanged', sha256(prompt.encode()) == item['prompt_sha256'])
        activation = 'Use $long-horizon at /workspace/skill/SKILL.md for this handoff review.\n\n'
        check(f'{label}:correct_activation', prompt.startswith(activation) == (item['arm'] != 'no-skill'))
        prompts.setdefault(item['case'], set()).add(prompt.removeprefix(activation))
        for argument in item.get('command', []):
            path = Path(argument)
            if '/evals/runs/native-matrix-' in argument and path.name == 'private-home':
                temp_paths.add(path.parent)
        review_path = session / 'manual-review.json'
        check(f'{label}:manual_review_present', review_path.is_file())
        if review_path.is_file():
            review = json.loads(review_path.read_text())
            check(f'{label}:review_matches_decision', sha256((session / 'work/decision.md').read_bytes()) == review['decision_sha256'])
    check('exact_declared_session_set', found == scheduled and len(sessions) == manifest['intended_session_count'])
    check('identical_prompts_except_activation', all(len(values) == 1 for values in prompts.values()))
    check('all_owned_temporary_homes_removed', bool(temp_paths) and all(not path.exists() for path in temp_paths))
    # Match exact private-home session paths, never print full process arguments.
    remaining_pids = []
    for path in Path('/proc').glob('[0-9]*/cmdline'):
        try:
            command = path.read_bytes()
            if any(str(temporary).encode() in command for temporary in temp_paths):
                remaining_pids.append(int(path.parent.name))
        except OSError:
            pass
    check('no_processes_reference_owned_session_paths', not remaining_pids)
    return {'audited_at': utc_now(), 'checks': checks, 'failures': failures, 'passed': not failures,
            'session_count': len(sessions), 'temporary_session_directories_checked': len(temp_paths),
            'remaining_owned_process_ids': remaining_pids,
            'limits': 'Checks archived identities and recorded probes. Exact credential scanning and semantic source review are separate artifacts.'}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('matrix', type=Path)
    args = parser.parse_args()
    result = audit(args.matrix)
    dump(args.matrix / 'provenance-audit.json', result)
    print(f'Provenance audit: {len(result["checks"])} checks; {len(result["failures"])} failures.')
    return int(not result['passed'])


if __name__ == '__main__':
    raise SystemExit(main())
