#!/usr/bin/env python3
"""Opt-in completion of ungenerated cells or five preselected focused probes."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import shutil
import signal
import tarfile
from typing import Any

from fixtures import Case
from native_harnesses import discover, version_info
from native_matrix import evaluate
from recall import aggregate_hash, archive_inputs, dump, hashes, request_stop, utc_now

ROOT = Path(__file__).resolve().parents[1]
FOCUSED = (('claude', 'weekly-product', 'native-tools'),
           ('antigravity', 'revenue', 'native-tools'),
           ('antigravity', 'weekly-product', 'native-tools'),
           ('antigravity', 'large-export', 'native-tools'),
           ('codex', 'large-export', 'native-tools'))


def matching_prompt(source: Path, case: str, arm: str) -> str:
    paths = sorted((source / 'sessions').glob(f'*/{case}/{arm}/prompt.txt'))
    if not paths:
        raise ValueError(f'No preserved prompt for {case}/{arm}')
    for path in paths:
        metadata = json.loads((path.parent / 'manifest.json').read_text())
        if hashlib.sha256(path.read_bytes()).hexdigest() != metadata['prompt_sha256']:
            raise ValueError(f'Preserved prompt changed: {path}')
    values = {path.read_text() for path in paths}
    if len(values) != 1:
        raise ValueError(f'Initial prompts differ for {case}/{arm}')
    return values.pop()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-matrix', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--mode', choices=('complete', 'focused'), required=True)
    parser.add_argument('--candidate-hash', help='Required exact revised tree SHA256 for focused mode only.')
    parser.add_argument('--harness', action='append', choices=('codex', 'claude', 'antigravity'))
    parser.add_argument('--run', action='store_true')
    parser.add_argument('--jobs', type=int, choices=(1, 2), default=2)
    parser.add_argument('--timeout', type=int, default=1200)
    args = parser.parse_args()
    if not 30 <= args.timeout <= 3600:
        parser.error('--timeout must be between 30 and 3600 seconds')
    if (args.mode == 'focused') != bool(args.candidate_hash):
        parser.error('--candidate-hash is required only for focused mode')
    source = args.source_matrix.resolve()
    previous = json.loads((source / 'manifest.json').read_text())
    if 'finished_at' not in previous:
        raise ValueError('Source matrix must have finished before replay')
    if args.mode == 'focused':
        selected = list(FOCUSED)
    else:
        selected = [(r['harness'], r['case'], r['arm']) for r in previous['results'] if not r.get('decision_present')]
    if args.harness:
        selected = [r for r in selected if r[0] in args.harness]
    if not selected:
        raise ValueError('No eligible cells; completed decisions are never repeated in completion mode')
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    signal.signal(signal.SIGINT, request_stop)
    signal.signal(signal.SIGTERM, request_stop)
    source_names = ('native_replay.py', 'native_matrix.py', 'native_harnesses.py', 'native_fixtures.py', 'fixtures.py', 'recall.py')
    for name in source_names:
        shutil.copyfile(ROOT / 'evals' / name, output / name)
    source_hashes = hashes(output)
    shutil.copytree(source / 'bundles', output / 'bundles')
    if args.mode == 'focused':
        shutil.rmtree(output / 'bundles/native-tools')
        shutil.copytree(ROOT / 'skills/long-horizon', output / 'bundles/native-tools', ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    bundle_files = {arm: hashes(output / 'bundles' / arm) for arm in ('published-helper', 'native-tools')}
    if bundle_files['published-helper'] != previous['bundles']['files']['published-helper']:
        raise ValueError('Frozen published-helper bytes changed')
    actual_candidate = aggregate_hash(bundle_files['native-tools'])
    expected_candidate = args.candidate_hash or previous['bundles']['candidate_tree_sha256']
    if actual_candidate != expected_candidate:
        raise ValueError(f'Candidate hash mismatch: expected {expected_candidate}, got {actual_candidate}')
    bundles = dict(previous['bundles'], files=bundle_files, candidate_tree_sha256=actual_candidate)
    cases = {case for _, case, _ in selected}
    archive_path = source / previous['input_archive']['path']
    if hashlib.sha256(archive_path.read_bytes()).hexdigest() != previous['input_archive']['sha256']:
        raise ValueError('Initial input archive changed')
    with tarfile.open(archive_path) as archive:
        for member in archive:
            parts = Path(member.name).parts
            if member.isfile() and len(parts) > 2 and parts[0] == 'inputs' and parts[1] in cases:
                if '..' in parts:
                    raise ValueError('Unsafe source archive path')
                stream = archive.extractfile(member)
                assert stream is not None
                destination = output.joinpath(*parts)
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(stream.read())
    input_hashes = {case: hashes(output / 'inputs' / case) for case in sorted(cases)}
    if any(value != previous['case_input_hashes'][case] for case, value in input_hashes.items()):
        raise ValueError('Input snapshot does not match initial matrix')
    criteria_bytes = (source / 'criteria.json').read_bytes()
    if hashlib.sha256(criteria_bytes).hexdigest() != previous['criteria_sha256']:
        raise ValueError('Original criteria bytes changed')
    criteria = json.loads(criteria_bytes)
    dump(output / 'criteria.json', {case: criteria[case] for case in sorted(cases)})
    if 'large-export' in cases:
        shutil.copyfile(source / 'large-export-observability-clarification.json', output / 'large-export-observability-clarification.json')
    harnesses = {h.name: h for h in discover()}
    for name, _, _ in selected:
        expected = next(h for h in previous['harnesses'] if h['name'] == name)
        h = harnesses[name]
        if h.defaults != expected['installed_defaults'] or hashlib.sha256(h.binary.read_bytes()).hexdigest() != expected['binary_sha256']:
            raise ValueError(f'Installed harness/defaults changed: {name}')
    prompts = {(case, arm): matching_prompt(source, case, arm) for _, case, arm in selected}
    manifest: dict[str, Any] = {
        'started_at': utc_now(), 'live_run': args.run, 'mode': args.mode,
        'intended_session_count': len(selected), 'source_matrix': str(source),
        'source_matrix_manifest_sha256': hashlib.sha256((source / 'manifest.json').read_bytes()).hexdigest(),
        'source_input_archive_sha256': previous['input_archive']['sha256'],
        'initial_candidate_tree_sha256': previous['bundles']['candidate_tree_sha256'],
        'bundles': bundles, 'source_hashes': source_hashes, 'case_input_hashes': input_hashes,
        'criteria_sha256': hashlib.sha256((output / 'criteria.json').read_bytes()).hexdigest(),
        'harnesses': [{'name': h.name, 'binary': str(h.binary), 'binary_sha256': hashlib.sha256(h.binary.read_bytes()).hexdigest(),
                      'installed_defaults': h.defaults, 'version': version_info(h)} for h in harnesses.values()],
        'schedule': [{'harness': h, 'case': c, 'arm': a} for h, c, a in selected],
        'preselected_focused_cells': [{'harness': h, 'case': c, 'arm': a} for h, c, a in FOCUSED] if args.mode == 'focused' else [],
        'interpretation': ('Infrastructure completion only: failed before-generation and skipped initial cells; no completed decision repeated.'
                           if args.mode == 'complete' else 'Five post hoc, preselected focused probes on revised bytes: four observed failure cells and one passing control. Not a new balanced matrix or reliability estimate.'),
        'semantic_policy': previous['semantic_policy'],
        'limitations': previous['limitations'],
    }
    dump(output / 'manifest.json', manifest)
    def run_cell(row: tuple[str, str, str]) -> dict[str, Any]:
        name, case, arm = row
        return evaluate(harnesses[name], Case(case, '', {}, ()), arm, output, args.run, args.timeout,
                        prompt_override=prompts[(case, arm)])
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(run_cell, selected))
    manifest['results'] = results
    manifest['finished_at'] = utc_now()
    manifest['input_archive'] = archive_inputs(output)
    dump(output / 'manifest.json', manifest)
    return int(any(r.get('infrastructure_error') or r.get('not_launched') or r.get('exit_code', 0) not in (0, None)
                   or r.get('input_mutations') or (args.run and not r.get('decision_present')) for r in results))


if __name__ == '__main__':
    raise SystemExit(main())
