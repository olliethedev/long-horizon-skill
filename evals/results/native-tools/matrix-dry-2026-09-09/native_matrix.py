#!/usr/bin/env python3
"""Opt-in 36-session native-harness recall comparison (Python 3.11+).

Three actual CLIs x three treatments x four matched domains. No model/effort
flags are accepted: installed defaults are copied, recorded and left unchanged.
Without --run, freeze inputs/criteria/bundles and probe every isolated workspace.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import shutil
import signal
import subprocess
import tarfile
import tempfile
from typing import Any

from fixtures import Case, materialize
from native_fixtures import cases
from native_harnesses import Harness, boundary, bubble, discover, invocation, setup_home, summarize
from recall import (STOP_BETWEEN_CASES, aggregate_hash, archive_inputs, capture, dump,
                    hashes, request_stop, utc_now)

ROOT = Path(__file__).resolve().parents[1]
BASELINE_COMMIT = 'be8d5901028abb11247664cea1e0f3af087e34fd'
CANDIDATE_HASH = 'd2fc4f19934888d2b59fae0cbac46eb87b1b43c00033593be2563d5ba22b9b7e'
ARMS = ('no-skill', 'published-helper', 'native-tools')


def prompt_for(case: Case, arm: str) -> str:
    activation = 'Use $long-horizon at /workspace/skill/SKILL.md for this handoff review.\n\n' if arm != 'no-skill' else ''
    return activation + case.request + '\n\n' + (
        'The product workspace is /workspace/product. Start with brief.md and current.md. '
        'The attached source archive is a read-only snapshot; you may search it and inspect original records. '
        'Use only this local snapshot for the review. No external systems are connected and no live actions are authorized here. '
        'Write your dated recommendation to /workspace/work/decision.md, including the relevant prior actions, '
        'what the evidence supports now, the next useful action, and important uncertainty. Cite specific source paths and source IDs '
        'so the product owner can inspect your reasoning. Preserve unknown dates. Finish with a brief response pointing to your decision.\n'
    )


def freeze_bundles(output: Path) -> dict[str, Any]:
    bundle = output / 'bundles'
    baseline = bundle / 'published-helper'
    baseline.mkdir(parents=True)
    raw = subprocess.run(['git', 'archive', BASELINE_COMMIT, 'skills/long-horizon'], cwd=ROOT,
                         check=True, capture_output=True).stdout
    archive_path = bundle / 'published-git-archive.tar'
    archive_path.write_bytes(raw)
    with tarfile.open(archive_path) as archive:
        for member in archive.getmembers():
            path = Path(member.name)
            if member.isfile():
                relative = path.relative_to('skills/long-horizon')
                target = baseline / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                stream = archive.extractfile(member)
                assert stream is not None
                target.write_bytes(stream.read())
                target.chmod(member.mode)
    candidate = bundle / 'native-tools'
    shutil.copytree(ROOT / 'skills/long-horizon', candidate, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    candidate_hash = aggregate_hash(hashes(candidate))
    if candidate_hash != CANDIDATE_HASH:
        raise ValueError(f'Candidate changed: expected {CANDIDATE_HASH}; got {candidate_hash}')
    return {'published_commit': BASELINE_COMMIT,
            'published_tree_sha256': aggregate_hash(hashes(baseline)),
            'candidate_tree_sha256': candidate_hash,
            'published_git_archive_sha256': hashlib.sha256(raw).hexdigest(),
            'files': {arm: hashes(bundle / arm) for arm in ARMS if arm != 'no-skill'}}


def evaluate(h: Harness, case: Case, arm: str, output: Path, run: bool, timeout: int) -> dict[str, Any]:
    if STOP_BETWEEN_CASES.is_set():
        return {'harness': h.name, 'case': case.name, 'arm': arm, 'not_launched': 'operator_or_infrastructure_stop'}
    destination = output / 'sessions' / h.name / case.name / arm
    destination.mkdir(parents=True)
    prompt = prompt_for(case, arm)
    (destination / 'prompt.txt').write_text(prompt)
    input_root = output / 'inputs' / case.name
    before = hashes(input_root)
    metadata: dict[str, Any] = {'harness': h.name, 'case': case.name, 'arm': arm, 'started_at': utc_now(),
                               'installed_defaults': h.defaults, 'input_tree_sha256': aggregate_hash(before),
                               'prompt_sha256': hashlib.sha256(prompt.encode()).hexdigest(),
                               'fresh_session': True, 'model_or_effort_override': False}
    dump(destination / 'manifest.json', metadata)
    try:
        with tempfile.TemporaryDirectory(prefix=f'native-matrix-{h.name}-{case.name}-{arm}-', dir=ROOT / 'evals/runs') as temp:
            temporary = Path(temp)
            workspace = temporary / 'workspace'
            shutil.copytree(input_root, workspace / 'product')
            (workspace / 'work').mkdir()
            private_home = temporary / 'private-home'
            setup_home(h, private_home)
            skill = None if arm == 'no-skill' else output / 'bundles' / arm
            base = bubble(workspace, private_home, h, skill)
            metadata['isolation_probe'] = boundary(base, h)
            metadata['loaded_skill_hashes'] = {} if skill is None else hashes(skill)
            metadata['command'] = base + invocation(h, timeout, prompt)
            dump(destination / 'manifest.json', metadata)
            print(f'{utc_now()} {"RUN" if run else "PREPARE"} {h.name}/{case.name}/{arm}', flush=True)
            if run:
                metadata.update(capture(metadata['command'], prompt, destination, timeout + 10))
                dump(destination / 'trace-summary.json', summarize(destination / 'trace.jsonl.gz', h))
                shutil.copytree(workspace / 'work', destination / 'work')
                metadata['decision_present'] = (destination / 'work/decision.md').is_file()
                # Preserve actual native Antigravity conversation traces separately;
                # its print stream can omit internal tool output/usage.
                if h.name == 'antigravity':
                    for folder in ('conversations', 'brain'):
                        source = private_home / '.gemini/antigravity-cli' / folder
                        if source.exists():
                            shutil.copytree(source, destination / 'native-traces' / folder)
                if metadata.get('exit_code') != 0 or not metadata['decision_present']:
                    STOP_BETWEEN_CASES.set()
            after = hashes(workspace / 'product')
            metadata['input_mutations'] = {key: {'before': before.get(key), 'after': after.get(key)}
                                           for key in before.keys() | after.keys() if before.get(key) != after.get(key)}
        metadata['temporary_auth_home_removed'] = not temporary.exists()
    except Exception as exc:
        STOP_BETWEEN_CASES.set()
        metadata['infrastructure_error'] = f'{type(exc).__name__}: {exc}'
    metadata['finished_at'] = utc_now()
    dump(destination / 'manifest.json', metadata)
    print(f'{utc_now()} DONE {h.name}/{case.name}/{arm} exit={metadata.get("exit_code")} decision={metadata.get("decision_present")}', flush=True)
    return {k: metadata.get(k) for k in ('harness', 'case', 'arm', 'exit_code', 'termination_reason', 'decision_present',
                                         'elapsed_seconds', 'input_mutations', 'infrastructure_error', 'temporary_auth_home_removed')}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', action='store_true', help='Opt into exactly 36 authenticated native sessions.')
    parser.add_argument('--output', type=Path, required=True, help='New output path; existing evidence is never overwritten.')
    parser.add_argument('--jobs', type=int, choices=(1, 2), default=2)
    parser.add_argument('--timeout', type=int, default=1200)
    args = parser.parse_args()
    output: Path = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    signal.signal(signal.SIGINT, request_stop)
    signal.signal(signal.SIGTERM, request_stop)
    selected = cases()
    harnesses = discover()
    (ROOT / 'evals/runs').mkdir(exist_ok=True)
    for name in ('native_matrix.py', 'native_harnesses.py', 'native_fixtures.py', 'fixtures.py', 'recall.py'):
        shutil.copyfile(ROOT / 'evals' / name, output / name)
    bundle_identity = freeze_bundles(output)
    for case in selected:
        materialize(case, output / 'inputs' / case.name)
    dump(output / 'criteria.json', {case.name: [asdict(c) for c in case.criteria] for case in selected})
    # Rotate treatment ordering by domain, preserving a predeclared deterministic
    # schedule. Each harness uses its installed defaults; report separately.
    schedule = [(h, case, ARMS[(arm_index + case_index) % 3])
                for case_index, case in enumerate(selected) for h in harnesses for arm_index in range(3)]
    manifest: dict[str, Any] = {'started_at': utc_now(), 'live_run': args.run, 'intended_session_count': 36,
        'bundles': bundle_identity, 'case_input_hashes': {c.name: hashes(output / 'inputs' / c.name) for c in selected},
        'criteria_sha256': hashlib.sha256((output / 'criteria.json').read_bytes()).hexdigest(),
        'source_hashes': {n: v for n, v in hashes(output).items() if '/' not in n},
        'harnesses': [{'name': h.name, 'binary': str(h.binary), 'binary_sha256': hashlib.sha256(h.binary.read_bytes()).hexdigest(),
                       'installed_defaults': h.defaults} for h in harnesses],
        'schedule': [{'harness': h.name, 'case': c.name, 'arm': a} for h, c, a in schedule],
        'semantic_policy': 'All five source-backed criteria must pass and no material contradictory decision. Exit status, artifact presence and retrieval size are not semantic success. Manual source/trace review is required.',
        'limitations': ['One initial session per harness/arm/domain; descriptive case outcomes, no significance estimates.',
                        'Synthetic histories contain repeated templates despite varied cohorts, corrections, dispositions and shared opaque ID space.',
                        'Filesystem and PID isolation; host network retained for native model transport, external restraint is task-level.',
                        'Offline decisions cannot establish live scheduling, mutation or customer outcomes.',
                        'Skill source is explicitly activated by file path; this evaluates instruction use, not automatic discovery.',
                        'Antigravity uses its native fresh local project; temporary credential homes are destroyed and not archived.']}
    dump(output / 'manifest.json', manifest)
    print(f'FROZEN {json.dumps(bundle_identity, sort_keys=True)[:220]}', flush=True)
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = [pool.submit(evaluate, h, c, a, output, args.run, args.timeout) for h, c, a in schedule]
        results = [f.result() for f in futures]
    manifest['results'] = results
    manifest['finished_at'] = utc_now()
    manifest['input_archive'] = archive_inputs(output)
    dump(output / 'manifest.json', manifest)
    return int(any(r.get('infrastructure_error') or r.get('not_launched') or r.get('exit_code', 0) not in (0, None) or r.get('input_mutations') for r in results))


if __name__ == '__main__':
    raise SystemExit(main())
