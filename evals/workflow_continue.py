#!/usr/bin/env python3
"""Continue a gracefully interrupted workflow study without repeating decisions."""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import shutil
import signal
from typing import Any

from native_harnesses import Harness, discover
from recall import STOP_BETWEEN_CASES, aggregate_hash, dump, hashes, request_stop, utc_now
import workflow_runner as runner
from workflow_clock import next_transition
from workflow_world import HORIZON, apply_event, event_tape, initial

MAX_NEW_SESSIONS = 4


class LaunchBudget:
    """Consume a durable slot before each attempt; failures never refund slots."""

    def __init__(self, root: Path) -> None:
        self.folder = root / 'launch-slots'
        self.folder.mkdir()
        self.used = 0

    def reserve(self, case: str, index: int) -> bool:
        if self.used >= MAX_NEW_SESSIONS:
            return False
        with (self.folder / f'{self.used:02d}.json').open('x') as stream:
            json.dump({'case': case, 'session_index': index, 'reserved_at': utc_now()}, stream)
        self.used += 1
        return True


def claim_live_continuation(source: Path, root: Path) -> None:
    """Refuse another live continuation even if the first crashed or used a new output path."""
    claim = source.parent / f'{source.name}.continuation-claim.json'
    with claim.open('x') as stream:
        json.dump({'source': str(source), 'output': str(root), 'claimed_at': utc_now(),
                   'maximum_new_sessions': MAX_NEW_SESSIONS}, stream)


def advance(state: dict[str, Any]) -> tuple[list[str], str | None] | None:
    """Use precisely the original event clock; never fabricate a wake."""
    while True:
        schedule = state['scheduler']
        step = next_transition(day=state['day'], horizon=HORIZON,
            events=event_tape(state['domain']), consumed=frozenset(state['consumed_events']),
            scheduled_day=schedule['day'], enabled=schedule['enabled'])
        if step is None:
            return None
        state['day'] = step.day
        for event in step.events:
            apply_event(state, event)
        instruction = state['scheduler']['instruction'] if step.scheduled_run_due else None
        if step.wake_reasons:
            return list(step.wake_reasons), instruction


def position(folder: Path) -> tuple[dict[str, Any], int, list[str], str | None]:
    """Validate the saved boundary against replay from the last completed session."""
    result = json.loads((folder / 'trajectory.json').read_text())
    if result['stop_reason'] != 'infrastructure_stop_before_launch':
        raise ValueError('Only a graceful between-session interruption can continue')
    sessions = result['sessions']
    count = len(sessions)
    if count != result['actual_sessions'] or count >= 8:
        raise ValueError('Invalid or exhausted original trajectory session allowance')
    manifests = sorted((folder / 'sessions').glob('*/manifest.json'))
    if len(manifests) != count:
        raise ValueError('Session inventory differs from recorded attempts')
    for index, path in enumerate(manifests):
        session = json.loads(path.read_text())
        scan = session.get('credential_scan', {})
        if (session != sessions[index] or session['index'] != index
                or not session.get('finished_at') or session.get('exit_code') != 0
                or session.get('infrastructure_error') or not session.get('model_launch_attempted')
                or not scan.get('complete') or scan.get('matches')
                or not session.get('temporary_auth_home_removed')):
            raise ValueError('A generated or failed attempt cannot be repeated or repaired here')
    state = deepcopy(result['state'])
    if count == 0:
        if state != initial(result['domain']) or runner.inventory(folder / 'product'):
            raise ValueError('Unlaunched trajectory must have its original empty state')
        return state, 0, ['initial_owner_request'], None
    last = manifests[-1].parent
    if runner.inventory(folder / 'product') != sessions[-1]['product_after']:
        raise ValueError('Continuing workspace differs from the completed session')
    replay = json.loads((last / 'state-after.json').read_text())
    wake = advance(replay)
    if wake is None or replay != state:
        raise ValueError('Saved boundary does not match the original next actual wake')
    return state, count, wake[0], wake[1]


def run_remainder(harness: Harness, domain: str, arm: str, source: Path,
                  root: Path, live: bool, budget: LaunchBudget) -> dict[str, Any]:
    original = source / 'trajectories' / harness.name / domain / arm
    state, previous_count, reasons, instruction = position(original)
    folder = root / 'trajectories' / harness.name / domain / arm
    folder.mkdir(parents=True)
    product = folder / 'product'
    runner.copy_workspace(original / 'product', product)
    dump(folder / 'continuation-source.json', {
        'path': str(original), 'artifact_hashes': runner.inventory(original),
        'previous_sessions': previous_count, 'next_day': state['day'],
        'wake_reasons': reasons, 'instruction': instruction})
    runs: list[dict[str, Any]] = []
    stop_reason = 'prepared_only'
    try:
        while previous_count + len(runs) < 8 and not STOP_BETWEEN_CASES.is_set():
            index = previous_count + len(runs)
            if live and not budget.reserve(f'{harness.name}/{domain}/{arm}', index):
                stop_reason = 'owner_session_budget_exhausted'
                break
            if 'confirmed_schedule' in reasons:
                state['scheduler']['day'] = None
            run = runner.run_session(harness, state, folder / 'sessions' / f'{index:02d}',
                product, root / 'skill' if arm == 'skill' else None,
                reasons, instruction, index, live, 600)
            runs.append(run)
            if not live:
                break
            if run.get('infrastructure_error') or run.get('exit_code') != 0:
                stop_reason = 'infrastructure_or_process_failure'
                STOP_BETWEEN_CASES.set()
                break
            wake = advance(state)
            if wake is None:
                stop_reason = 'horizon_or_no_further_wake'
                break
            reasons, instruction = wake
        else:
            stop_reason = ('session_cap' if previous_count + len(runs) >= 8
                           else 'infrastructure_stop_before_launch')
    except Exception as error:
        STOP_BETWEEN_CASES.set()
        stop_reason = 'infrastructure_error'
        dump(folder / 'continuation-error.json', {'exception_type': type(error).__name__})
    result = {'harness': harness.name, 'domain': domain, 'arm': arm,
        'source_trajectory': str(original), 'previous_sessions': previous_count,
        'sessions': runs, 'actual_sessions': len(runs),
        'cumulative_actual_sessions': previous_count + len(runs), 'state': state,
        'stop_reason': stop_reason, 'semantic_review': 'pending' if live else 'not_applicable'}
    dump(folder / 'trajectory.json', result)
    return {key: result[key] for key in ('harness', 'domain', 'arm', 'actual_sessions',
                                        'previous_sessions', 'stop_reason')}


def safe_remainder(harness: Harness, domain: str, arm: str, source: Path,
                   root: Path, live: bool, budget: LaunchBudget) -> dict[str, Any]:
    try:
        return run_remainder(harness, domain, arm, source, root, live, budget)
    except Exception as error:
        STOP_BETWEEN_CASES.set()
        folder = root / 'trajectories' / harness.name / domain / arm
        folder.mkdir(parents=True, exist_ok=True)
        result = {'harness': harness.name, 'domain': domain, 'arm': arm,
            'stop_reason': 'infrastructure_error', 'exception_type': type(error).__name__,
            'actual_sessions': len(list((folder / 'sessions').glob('*/manifest.json')))}
        dump(folder / 'trajectory-failure.json', result)
        return result


def prepare(source: Path, root: Path) -> tuple[dict[str, Any], list[tuple[Harness, str, str]]]:
    original = json.loads((source / 'manifest.json').read_text())
    if not original.get('live') or not original.get('finished_at') or not original.get('executed_sources_unchanged'):
        raise ValueError('Original live study must finish clean artifact capture first')
    if hashes(source / 'sources') != original['source_hashes']:
        raise ValueError('Frozen original evaluator source changed')
    for name, digest in original['source_hashes'].items():
        if hashlib.sha256((runner.ROOT / 'evals' / name).read_bytes()).hexdigest() != digest:
            raise ValueError('Executed original evaluator sources changed')
    if hashlib.sha256((source / 'protocol.md').read_bytes()).hexdigest() != original['protocol_sha256']:
        raise ValueError('Original protocol changed')
    if aggregate_hash(hashes(source / 'skill')) != original['skill_tree']:
        raise ValueError('Original skill changed')
    available = {h.name: h for h in discover() if h.name == 'codex'}
    frozen = {h['name']: h for h in original['harnesses']}
    if set(available) != {'codex'}:
        raise ValueError('Selected native harness is unavailable')
    for name, harness in available.items():
        if (harness.defaults != frozen[name]['defaults'] or
                hashlib.sha256(harness.binary.read_bytes()).hexdigest() != frozen[name]['binary_sha256']):
            raise ValueError('Native binary or installed defaults changed')
    selected = []
    excluded = []
    original_attempts = 0
    for case in original['schedule']:
        folder = source / 'trajectories' / case['harness'] / case['domain'] / case['arm']
        result = json.loads((folder / 'trajectory.json').read_text())
        original_attempts += sum(bool(s.get('model_launch_attempted')) for s in result['sessions'])
        if case['harness'] != 'codex' or case['domain'] != 'weekly-product':
            excluded.append({**case, 'original_sessions': result['actual_sessions'],
                             'reason': ('completed evidence retained' if result['stop_reason'] == 'horizon_or_no_further_wake'
                                        else 'outside owner-authorized four-session continuation')})
        elif result['stop_reason'] == 'infrastructure_stop_before_launch':
            position(folder)
            selected.append((available[case['harness']], case['domain'], case['arm']))
        elif result['stop_reason'] not in ('horizon_or_no_further_wake', 'session_cap'):
            raise ValueError('A failed generated trajectory needs separate review; never resample it')
    maximum_new = min(MAX_NEW_SESSIONS, sum(8 - position(source / 'trajectories' / h.name / d / a)[1] for h, d, a in selected))
    if original_attempts != 46 or original_attempts + maximum_new > original['maximum_total_sessions']:
        raise ValueError('Continuation would exceed the original total launch allowance')
    root.mkdir(parents=True, exist_ok=False)
    shutil.copytree(source / 'skill', root / 'skill')
    shutil.copytree(source / 'sources', root / 'sources')
    shutil.copyfile(source / 'protocol.md', root / 'protocol.md')
    shutil.copyfile(Path(__file__), root / 'continuation-runner.py')
    metadata = {'started_at': utc_now(), 'mode': 'quota_continuation', 'source_study': str(source),
        'source_manifest_sha256': hashlib.sha256((source / 'manifest.json').read_bytes()).hexdigest(),
        'source_hashes': original['source_hashes'], 'skill_tree': original['skill_tree'],
        'continuation_runner_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'original_launch_attempts': original_attempts, 'maximum_new_launch_attempts': maximum_new,
        'maximum_total_launch_attempts': original_attempts + maximum_new, 'maximum_concurrent_native_processes': 1,
        'maximum_cumulative_sessions_per_trajectory': 8, 'session_timeout_seconds': 600,
        'schedule': [{'harness': h.name, 'domain': d, 'arm': a} for h, d, a in selected],
        'excluded': excluded,
        'reason': 'After pausing for usage concerns, owner authorized exactly four more sessions, bringing 46 to 50, then ending this evaluation. Continue the partial Codex weekly-product skill trajectory first and use remaining slots for its baseline. Preserve original decisions, clocks and incomplete coverage; no Claude launches.'}
    return metadata, selected


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--run', action='store_true')
    args = parser.parse_args()
    source, root = args.source.resolve(), args.output.resolve()
    metadata, selected = prepare(source, root)
    metadata['live'] = args.run
    dump(root / 'manifest.json', metadata)
    signal.signal(signal.SIGINT, request_stop)
    signal.signal(signal.SIGTERM, request_stop)
    if args.run:
        claim_live_continuation(source, root)
    budget = LaunchBudget(root)
    metadata['results'] = [safe_remainder(h, d, a, source, root, args.run, budget)
                           for h, d, a in selected]
    metadata['reserved_launch_slots'] = budget.used
    metadata['finished_at'] = utc_now()
    metadata['executed_sources_unchanged'] = all(
        hashlib.sha256((runner.ROOT / 'evals' / name).read_bytes()).hexdigest() == digest
        for name, digest in metadata['source_hashes'].items())
    metadata['continuation_runner_unchanged'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest() == metadata['continuation_runner_sha256']
    metadata['source_manifest_unchanged'] = hashlib.sha256((source / 'manifest.json').read_bytes()).hexdigest() == metadata['source_manifest_sha256']
    dump(root / 'manifest.json', metadata)
    print(json.dumps({'live': args.run, 'new_sessions': sum(r['actual_sessions'] for r in metadata['results']),
                      'continued_trajectories': len(selected)}))
    return int(STOP_BETWEEN_CASES.is_set() or not all(metadata[k] for k in
        ('executed_sources_unchanged', 'continuation_runner_unchanged', 'source_manifest_unchanged')))


if __name__ == '__main__':
    raise SystemExit(main())
