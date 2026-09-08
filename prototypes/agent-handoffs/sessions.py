#!/usr/bin/env python3
"""Collect local handoff artifacts and advance to the next synthetic packet."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil


def hashes(root):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob('*')) if p.is_file()}


def begin(base, manifest, name):
    entry = manifest['cases'][name]
    trial, reviewer = Path(entry['trial']), Path(entry['sources'])
    target = reviewer / f"session-{entry['session']}" / 'input'
    if target.exists():
        raise ValueError(f'Input already captured: {target}')
    target.mkdir(parents=True)
    for filename in (*entry['static_hashes'], 'current-packet.md'):
        shutil.copy2(trial / filename, target / filename)
    if entry['session'] == 1:
        # prepare.py creates empty initial memory; reconstruct it even if the
        # first agent has begun writing before input archival is performed.
        (target / 'memory').mkdir()
    else:
        shutil.copytree(trial / 'memory', target / 'memory')
    entry['pending_input_hashes'] = hashes(target)
    print(json.dumps({'case': name, 'input_session': entry['session'], 'files': len(entry['pending_input_hashes'])}))


def finish(base, manifest, name, agent):
    entry = manifest['cases'][name]
    trial, reviewer = Path(entry['trial']), Path(entry['sources'])
    session = entry['session']
    target = reviewer / f'session-{session}'
    if not (target / 'input').is_dir() or (target / 'memory').exists():
        raise ValueError('Missing input snapshot or session already collected')
    for filename, expected in entry['static_hashes'].items():
        if hashlib.sha256((trial / filename).read_bytes()).hexdigest() != expected:
            raise ValueError(f'Static input changed: {filename}')
    if (trial / 'current-packet.md').read_bytes() != (reviewer / f'packet-{session}.md').read_bytes():
        raise ValueError('Observation packet changed')
    if not (trial / 'outbox/decision.md').is_file():
        raise ValueError('Missing decision')
    json.loads((trial / 'outbox/run.json').read_text())
    shutil.copytree(trial / 'memory', target / 'memory')
    shutil.copytree(trial / 'outbox', target / 'outbox')
    entry['sessions'].append({'session': session, 'agent': agent,
        'input_sha256': entry.pop('pending_input_hashes'),
        'memory_sha256': hashes(target / 'memory'),
        'outbox_sha256': hashes(target / 'outbox'), 'static_inputs_unchanged': True})
    if session < 3:
        # These outputs are collected evaluation artifacts, not agent memory.
        shutil.rmtree(trial / 'outbox')
        (trial / 'outbox').mkdir()
        entry['session'] += 1
        shutil.copy2(reviewer / f'packet-{session + 1}.md', trial / 'current-packet.md')
        begin(base, manifest, name)
    print(json.dumps({'case': name, 'collected_session': session, 'next_session': session + 1 if session < 3 else None}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('operation', choices=['begin', 'finish'])
    parser.add_argument('root', type=Path)
    parser.add_argument('case')
    parser.add_argument('--agent')
    args = parser.parse_args()
    manifest_path = args.root / 'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    if args.operation == 'begin':
        begin(args.root, manifest, args.case)
    else:
        finish(args.root, manifest, args.case, args.agent)
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
