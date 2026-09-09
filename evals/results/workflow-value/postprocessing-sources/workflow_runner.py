#!/usr/bin/env python3
"""Opt-in complete-workflow comparison using actual fresh native harnesses."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from dataclasses import asdict
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import socket
import stat
import subprocess
import tempfile
import threading
from typing import Any

from native_credentials_check import collect, scan
from native_harnesses import Harness, bubble, discover, invocation, setup_home, summarize, version_info
from recall import STOP_BETWEEN_CASES, aggregate_hash, capture, dump, hashes, request_stop, utc_now
from workflow_calibrate import calibrate
from workflow_clock import next_transition
from workflow_service import ProductService
from workflow_world import DOMAINS, HORIZON, REQUESTS, apply_event, event_tape, initial

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = 'af8084aa46624ee25271c94ef14e1593f7adb6d325da156348132a8620ac4d26'
SOURCES = ('workflow_runner.py', 'workflow_calibrate.py', 'workflow_clock.py', 'workflow_world.py', 'workflow_rubric.json',
           'workflow_review_cases.json', 'workflow_review_key.json',
           'workflow_service.py', 'workflow_client.py', 'workflow_api.md', 'native_harnesses.py',
           'native_credentials_check.py', 'recall.py', 'fixtures.py')


def inventory(root: Path) -> dict[str, str]:
    """Hash regular bytes or link text; never follow agent-created symlinks."""
    if root.is_symlink() or not root.is_dir():
        raise ValueError('A workspace root must remain a real directory')
    result: dict[str, str] = {}
    for directory, folders, files in os.walk(root, followlinks=False):
        for name in sorted(folders + files):
            path = Path(directory) / name
            mode = path.lstat().st_mode
            key = str(path.relative_to(root))
            if stat.S_ISLNK(mode):
                result[key] = 'symlink:' + os.readlink(path)
            elif stat.S_ISREG(mode):
                result[key] = hashlib.sha256(path.read_bytes()).hexdigest()
            elif not stat.S_ISDIR(mode):
                raise ValueError(f'Unsupported generated file type: {key}')
    return result


def copy_workspace(source: Path, destination: Path) -> None:
    inventory(source)
    shutil.copytree(source, destination, symlinks=True)


def preserve_workspace(source: Path, destination: Path) -> list[dict[str, str]]:
    """Retain readable evidence even if an agent leaves unsupported filesystem nodes."""
    issues: list[dict[str, str]] = []
    destination.mkdir(parents=True)

    def retain(path: Path, target: Path) -> None:
        label = str(path.relative_to(source))
        try:
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode):
                target.symlink_to(os.readlink(path))
            elif stat.S_ISREG(mode):
                shutil.copyfile(path, target, follow_symlinks=False)
            elif stat.S_ISDIR(mode):
                target.mkdir(exist_ok=True)
                for child in sorted(path.iterdir()):
                    retain(child, target / child.name)
            else:
                issues.append({'path': label, 'file_type': oct(stat.S_IFMT(mode))})
        except OSError as error:
            issues.append({'path': label, 'error': type(error).__name__})

    if source.is_symlink() or not source.is_dir():
        issues.append({'path': '.', 'error': 'WorkspaceRootReplacedOrMissing'})
        if source.is_symlink():
            issues[-1]['link_target'] = os.readlink(source)
    else:
        for path in sorted(source.iterdir()):
            retain(path, destination / path.name)
    return issues


def session_prompt(state: dict[str, Any], reasons: list[str], instruction: str | None,
                   first: bool, skill: bool) -> str:
    activation = 'Use $long-horizon at /workspace/skill/SKILL.md for this responsibility.\n\n' if skill else ''
    owner = REQUESTS[state['domain']] if first else ''
    if 'owner-close' in reasons:
        owner = 'Stop product changes now. Disable future work and send me your current findings. Retain the product history.'
    elif 'owner-resume' in reasons:
        owner = 'I restored the connector. Resume the paused export assignment under the existing scope and limits; check the current customer situation.'
    return activation + f'''Simulated day: {state['day']}. Wake reason: {', '.join(reasons)}.
{('Owner: ' + owner) if owner else ''}
{('Scheduled assignment: ' + instruction) if instruction else ''}

You are in this product's workspace. /workspace/product is writable and persists across fresh sessions. /workspace/work is this session's output directory and is not carried into the next session. Connected tool documentation is /workspace/tools/API.md; owner answers and product operations are available through that interface. This session has no prior conversation context.

Use only this workspace and its connected synthetic service. Do not access host credentials, unrelated directories, other products, external websites, live schedulers, real messaging or paid product APIs. Native model transport is outside these product actions. Do not invoke other agents. The operating-system date is not simulation time. Finish when the current work should yield, and write the session's outcome to /workspace/work/decision.md.
'''


def sandbox(workspace: Path, home: Path, harness: Harness, skill: Path | None,
            socket_path: Path) -> list[str]:
    command = bubble(workspace, home, harness, skill)
    triple = ['--ro-bind', str(workspace / 'product'), '/workspace/product']
    found = next(i for i in range(len(command) - 2) if command[i:i + 3] == triple)
    del command[found:found + 3]
    command[-2:-2] = ['--ro-bind', str(workspace / 'tools'), '/workspace/tools',
                      '--ro-bind', str(socket_path), '/workspace/tools/service.sock']
    return command


def probe(command: list[str], expected_domain: str, output: Path,
          sibling_socket: Path, sibling_state: Path) -> dict[str, bool]:
    script = '''import json,pathlib,socket,subprocess,sys
p=pathlib.Path
checks={name:not p(name).exists() for name in ['/home/deck','/root','/grader','/workspace/evals','/workspace/criteria.json']}
test=p('/workspace/product/.write-probe');test.write_text('ok');test.unlink();checks['product_writable']=True
try:
 p('/workspace/tools/API.md').write_text('replace');checks['tools_read_only']=False
except OSError: checks['tools_read_only']=True
r=subprocess.run(['/usr/bin/python3','/workspace/tools/service.py','status'],capture_output=True,text=True,check=True)
value=json.loads(r.stdout);checks['own_service_access']=value.get('ok') is True
checks['sibling_state_inaccessible']=not p(sys.argv[2]).exists()
with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as other:
 other.settimeout(1)
 try:
  other.connect(sys.argv[1]);checks['sibling_socket_inaccessible']=False
 except OSError: checks['sibling_socket_inaccessible']=True
print(json.dumps({'checks':checks,'config':value.get('config')}))
raise SystemExit(not all(checks.values()))
'''
    result = subprocess.run(command + ['/usr/bin/python3', '-c', script, str(sibling_socket), str(sibling_state)],
                            capture_output=True, text=True, timeout=30)
    dump(output / 'isolation-probe.json', {'exit_code': result.returncode, 'stdout': result.stdout,
                                          'stderr': result.stderr, 'script': script})
    result.check_returncode()
    data = json.loads(result.stdout)
    if set(data['config']) != set(initial(expected_domain)['config']):
        raise ValueError('Service socket is not bound to the expected product')
    checks: dict[str, bool] = data['checks']
    return checks


def run_session(harness: Harness, state: dict[str, Any], output: Path, product: Path,
                bundle: Path | None, reasons: list[str], instruction: str | None,
                index: int, live: bool, timeout: int) -> dict[str, Any]:
    output.mkdir(parents=True)
    before = inventory(product)
    prompt = session_prompt(state, reasons, instruction, index == 0, bundle is not None)
    (output / 'prompt.txt').write_text(prompt)
    copy_workspace(product, output / 'product-before')
    dump(output / 'state-before.json', state)
    metadata: dict[str, Any] = {'started_at': utc_now(), 'harness': harness.name, 'day': state['day'],
                               'wake_reasons': reasons, 'fresh_session': True, 'index': index,
                               'timeout_seconds': timeout,
                               'model_launch_attempted': False,
                               'installed_defaults': harness.defaults, 'model_or_effort_override': False,
                               'prompt_sha256': hashlib.sha256(prompt.encode()).hexdigest(),
                               'product_before': before, 'loaded_skill_hashes': {} if bundle is None else hashes(bundle)}
    dump(output / 'manifest.json', metadata)
    observed: set[bytes] = set()
    stop_sampling = threading.Event()
    sample_count = 0

    def sample() -> None:
        nonlocal sample_count
        while not stop_sampling.is_set():
            observed.update(collect())
            sample_count += 1
            stop_sampling.wait(1)

    temporary_path: Path | None = None
    try:
        with tempfile.TemporaryDirectory(prefix=f'native-workflow-{harness.name}-', dir=ROOT / 'evals/runs') as temporary, \
             tempfile.TemporaryDirectory(prefix='lhw-socket-') as sockets:
            temporary_path = Path(temporary)
            workspace = temporary_path / 'workspace'
            workspace.mkdir()
            copy_workspace(product, workspace / 'product')
            (workspace / 'work').mkdir()
            (workspace / 'tools').mkdir()
            shutil.copyfile(ROOT / 'evals/workflow_api.md', workspace / 'tools/API.md')
            shutil.copyfile(ROOT / 'evals/workflow_client.py', workspace / 'tools/service.py')
            (workspace / 'tools/service.sock').touch()
            home = temporary_path / 'private-home'
            setup_home(harness, home)
            sampler = threading.Thread(target=sample, daemon=True)
            sampler.start()
            try:
                socket_path = Path(sockets) / 's'
                with ProductService(socket_path, state, output / 'service-state.json'):
                    command = sandbox(workspace, home, harness, bundle, socket_path)
                    # Probe effects are tagged separately and removed from the model's service history.
                    saved_events = deepcopy(state['events'])
                    sibling_socket, sibling_state = Path(sockets) / 'sibling', Path(sockets) / 'sibling-state.json'
                    sibling_state.write_text('{"synthetic_other_trajectory":true}')
                    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as other:
                        other.bind(str(sibling_socket))
                        other.listen(1)
                        metadata['isolation_probe'] = probe(command, state['domain'], output, sibling_socket, sibling_state)
                    state['events'] = saved_events
                    dump(output / 'service-state.json', state)
                    metadata['command'] = command + invocation(harness, timeout, prompt)
                    dump(output / 'manifest.json', metadata)
                    if live:
                        print(f'{utc_now()} RUN {harness.name}/{state["domain"]}/{"skill" if bundle else "no-skill"} session={index} day={state["day"]}', flush=True)
                        metadata['model_launch_attempted'] = True
                        dump(output / 'manifest.json', metadata)
                        metadata.update(capture(metadata['command'], prompt, output, timeout + 10))
                        dump(output / 'trace-summary.json', summarize(output / 'trace.jsonl.gz', harness))
            finally:
                try:
                    # Preserve independent evidence even when capture, parsing or one file fails.
                    paths = [(workspace / 'product', output / 'product-after'),
                             (workspace / 'work', output / 'work')]
                    if harness.name == 'antigravity':
                        for name in ('conversations', 'brain'):
                            source = home / '.gemini/antigravity-cli' / name
                            if source.exists() or source.is_symlink():
                                paths.append((source, output / 'native-traces' / name))
                    metadata['artifact_errors'] = {}
                    for source, destination in paths:
                        try:
                            issues = preserve_workspace(source, destination)
                        except OSError as error:
                            issues = [{'path': '.', 'error': type(error).__name__}]
                        if issues:
                            metadata['artifact_errors'][str(destination.relative_to(output))] = issues
                    metadata['product_after'] = inventory(output / 'product-after')
                    decision = output / 'work/decision.md'
                    metadata['decision_present'] = not decision.is_symlink() and decision.is_file()
                    dump(output / 'state-after.json', state)
                finally:
                    stop_sampling.set()
                    sampler.join()
                    observed.update(collect())
                    sample_count += 1
                    dump(output / 'manifest.json', metadata)
                    metadata['credential_scan'] = {'complete': False, 'samples': sample_count,
                        'observed_value_count': len(observed), 'values_persisted': False,
                        'limits': 'One-second sampling can miss intermediate refreshed values. Only completed session artifacts are scanned; generic-pattern scanning is separate.'}
                    try:
                        checked, hits = scan(output, observed)
                    except Exception as error:
                        metadata['credential_scan']['exception_type'] = type(error).__name__
                        raise
                    metadata['credential_scan'].update(complete=True, streams=checked, matches=hits)
                    if hits:
                        raise ValueError('Observed credential found in session artifacts; publication must stop')
            if metadata.get('artifact_errors'):
                raise ValueError('Some generated artifacts could not be preserved')
            if live:
                shutil.rmtree(product)
                copy_workspace(output / 'product-after', product)
    except Exception as error:
        STOP_BETWEEN_CASES.set()
        metadata['infrastructure_error'] = type(error).__name__
    metadata['temporary_auth_home_removed'] = temporary_path is not None and not temporary_path.exists()
    metadata['finished_at'] = utc_now()
    dump(output / 'state-after.json', state)
    dump(output / 'manifest.json', metadata)
    return metadata


def trajectory(harness: Harness, domain: str, arm: str, root: Path, live: bool,
               timeout: int, session_cap: int) -> dict[str, Any]:
    folder = root / 'trajectories' / harness.name / domain / arm
    folder.mkdir(parents=True)
    product = folder / 'product'
    product.mkdir()
    state = initial(domain)
    runs: list[dict[str, Any]] = []
    reasons, instruction = ['initial_owner_request'], None
    stop_reason = 'prepared_only'
    bundle = root / 'skill' if arm == 'skill' else None
    while len(runs) < session_cap and not STOP_BETWEEN_CASES.is_set():
        if 'confirmed_schedule' in reasons:
            state['scheduler']['day'] = None
        run = run_session(harness, state, folder / 'sessions' / f'{len(runs):02d}', product,
                          bundle, reasons, instruction, len(runs), live, timeout)
        runs.append(run)
        if not live:
            break
        if run.get('infrastructure_error') or run.get('exit_code') != 0:
            stop_reason = 'infrastructure_or_process_failure'
            STOP_BETWEEN_CASES.set()
            break
        wake = None
        while wake is None:
            schedule = state['scheduler']
            step = next_transition(day=state['day'], horizon=HORIZON, events=event_tape(domain),
                                   consumed=frozenset(state['consumed_events']), scheduled_day=schedule['day'],
                                   enabled=schedule['enabled'])
            if step is None:
                stop_reason = 'horizon_or_no_further_wake'
                break
            state['day'] = step.day
            for event in step.events:
                apply_event(state, event)
            instruction = state['scheduler']['instruction'] if step.scheduled_run_due else None
            if step.wake_reasons:
                wake = step
        if wake is None:
            break
        reasons = list(wake.wake_reasons)
    else:
        stop_reason = 'session_cap' if len(runs) >= session_cap else 'infrastructure_stop_before_launch'
    result = {'harness': harness.name, 'domain': domain, 'arm': arm, 'sessions': runs,
              'stop_reason': stop_reason, 'state': state, 'horizon': HORIZON,
              'actual_sessions': len(runs), 'semantic_review': 'pending' if live else 'not_applicable'}
    dump(folder / 'trajectory.json', result)
    return {key: result[key] for key in ('harness', 'domain', 'arm', 'stop_reason', 'actual_sessions', 'semantic_review')}


def safe_trajectory(harness: Harness, domain: str, arm: str, root: Path, live: bool,
                    timeout: int, session_cap: int) -> dict[str, Any]:
    try:
        return trajectory(harness, domain, arm, root, live, timeout, session_cap)
    except Exception as error:
        STOP_BETWEEN_CASES.set()
        folder = root / 'trajectories' / harness.name / domain / arm
        folder.mkdir(parents=True, exist_ok=True)
        result = {'harness': harness.name, 'domain': domain, 'arm': arm,
                  'stop_reason': 'infrastructure_error', 'exception_type': type(error).__name__,
                  'actual_sessions': len(list((folder / 'sessions').glob('*/manifest.json'))),
                  'semantic_review': 'pending' if live else 'not_applicable'}
        dump(folder / 'trajectory-failure.json', result)
        return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--run', action='store_true', help='Consume model allowance within the selected fixed matrix.')
    parser.add_argument('--harness', action='append', choices=('codex', 'claude', 'antigravity'))
    parser.add_argument('--timeout', type=int, default=600)
    args = parser.parse_args()
    if not 30 <= args.timeout <= 1200:
        parser.error('timeout must be between 30 and 1200 seconds')
    root = args.output.resolve()
    root.mkdir(parents=True, exist_ok=False)
    (ROOT / 'evals/runs').mkdir(exist_ok=True)
    signal.signal(signal.SIGINT, request_stop)
    signal.signal(signal.SIGTERM, request_stop)
    selection = set(args.harness or ('codex', 'claude', 'antigravity'))
    harnesses = tuple(h for h in discover() if h.name in selection)
    calibration = calibrate()
    dump(root / 'calibration.json', calibration)
    shutil.copytree(ROOT / 'skills/long-horizon', root / 'skill')
    if aggregate_hash(hashes(root / 'skill')) != CANDIDATE:
        raise ValueError('The declared skill candidate changed')
    (root / 'sources').mkdir()
    for name in SOURCES:
        shutil.copyfile(ROOT / 'evals' / name, root / 'sources' / name)
    shutil.copyfile(ROOT / 'docs/workflow-value-study.md', root / 'protocol.md')
    source_hashes = hashes(root / 'sources')
    schedule = [(h, domain, arm) for index, domain in enumerate(DOMAINS) for h in harnesses
                for arm in (('no-skill', 'skill') if index % 2 == 0 else ('skill', 'no-skill'))]
    manifest: dict[str, Any] = {'started_at': utc_now(), 'live': args.run, 'horizon_days': HORIZON,
        'trajectory_count': len(schedule), 'maximum_sessions_per_trajectory': 8,
        'maximum_total_sessions': len(schedule) * 8, 'skill_tree': CANDIDATE,
        'source_hashes': source_hashes,
        'protocol_sha256': hashlib.sha256((root / 'protocol.md').read_bytes()).hexdigest(),
        'event_tapes': {domain: [asdict(event) for event in event_tape(domain)] for domain in DOMAINS},
        'initial_states_sha256': {domain: hashlib.sha256(json.dumps(initial(domain), sort_keys=True).encode()).hexdigest() for domain in DOMAINS},
        'harnesses': [{'name': h.name, 'defaults': h.defaults, 'binary_sha256': hashlib.sha256(h.binary.read_bytes()).hexdigest(),
                       'version': version_info(h)} for h in harnesses],
        'schedule': [{'harness': h.name, 'domain': d, 'arm': a} for h, d, a in schedule],
        'limits': ['One scenario per domain; whole trajectories are experimental units.',
                   'Fictional configurations and observations, not arbitrary coding or real customer outcomes.',
                   'Owner replies use a deterministic topic interface, not an unrestricted human interview.',
                   'Host network remains available for native model transport; external product actions are prohibited by instruction.',
                   'Mechanical calibration is not semantic grading; manual full-trace reviews are required.']}
    dump(root / 'manifest.json', manifest)
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(safe_trajectory, h, d, a, root, args.run, args.timeout, 8) for h, d, a in schedule]
        results = [future.result() for future in futures]
    manifest['results'] = results
    manifest['finished_at'] = utc_now()
    manifest['executed_sources_unchanged'] = all(hashlib.sha256((ROOT / 'evals' / name).read_bytes()).hexdigest() == digest
                                                 for name, digest in source_hashes.items())
    dump(root / 'manifest.json', manifest)
    print(json.dumps({'trajectories': len(results), 'sessions': sum(r['actual_sessions'] for r in results),
                      'live': args.run, 'source_identity_verified': manifest['executed_sources_unchanged']}))
    return int(STOP_BETWEEN_CASES.is_set() or not manifest['executed_sources_unchanged'])


if __name__ == '__main__':
    raise SystemExit(main())
