#!/usr/bin/env python3
"""Validate handoff boundaries and preserve a completed exploratory run."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil


def hashes(root):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob('*')) if p.is_file()}


def archive(base, target):
    manifest = json.loads((base/'manifest.json').read_text())
    if target.exists():
        raise ValueError('Archive destination already exists')
    statistics = {}
    for name, entry in manifest['cases'].items():
        if [s['session'] for s in entry['sessions']] != [1, 2, 3]:
            raise ValueError(f'Incomplete chain: {name}')
        reviewer = Path(entry['sources'])
        stats = []
        for s in entry['sessions']:
            folder = reviewer/f"session-{s['session']}"
            for section, field in [('input', 'input_sha256'), ('memory', 'memory_sha256'), ('outbox', 'outbox_sha256')]:
                if hashes(folder/section) != s[field]:
                    raise ValueError(f'Changed snapshot: {name}, session {s["session"]}, {section}')
            if s['session'] > 1:
                previous = entry['sessions'][s['session']-2]['memory_sha256']
                if hashes(folder/'input/memory') != previous:
                    raise ValueError(f'Memory changed between agents: {name}')
            memory_files = [p for p in (folder/'memory').rglob('*') if p.is_file()]
            stats.append({'session': s['session'], 'memory_files': len(memory_files),
                'memory_bytes': sum(p.stat().st_size for p in memory_files),
                'packet_bytes': (folder/'input/current-packet.md').stat().st_size})
        statistics[name] = stats
    target.mkdir(parents=True)
    shutil.copytree(base/'reviewer', target/'cases')
    source = Path(__file__).resolve().parent
    for filename in ['prepare.py', 'sessions.py', 'archive.py', 'review-method.md']:
        shutil.copy2(source/filename, target/filename)
    first = next(iter(manifest['cases'].values()))
    shutil.copy2(Path(first['trial'])/'SKILL.md', target/'SKILL.md')
    manifest.update({'status': 'completed', 'archive_layout': 'cases/<domain>/session-<n>/{input,memory,outbox}',
        'agent_invocation_template': 'Use the long-horizon prototype skill at {trial}/SKILL.md to complete the current session described in {trial}/task.md. Work only inside that trial directory and follow its output and access restrictions. Do not inspect sibling directories or invoke subagents. Leave the requested artifacts and report completion.',
        'agent_fork_turns': 'none', 'model_override': None, 'harness': 'inherited defaults; full environment not independently audited',
        'statistics': statistics, 'review': 'manual and unblinded; see review-method.md and NOTES.md',
        'handoff_verification': 'All eight next-session memory inputs exactly match prior-session outputs; all snapshot hashes verified.',
        'first_input_archival': 'First-session empty memory reconstructed from generator contract after three agents had started; static input and packet hashes verified on collection.',
        'archive_file_sha256': hashes(target)})
    (target/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    (base/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print(json.dumps({'archive': str(target), 'statistics': statistics}, indent=2))


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('root', type=Path)
    parser.add_argument('destination', type=Path)
    args=parser.parse_args()
    archive(args.root, args.destination)
