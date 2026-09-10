#!/usr/bin/env python3
"""Opt-in ten-session Codex comparison; owner answers are manually moderated."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import shutil
import signal
import subprocess
import tempfile
import threading
import time
from typing import Any

from lean_world import DAYS, OWNER_FACTS, REQUEST, advance, call, initial
from native_credentials_check import extract, scan
from native_harnesses import Harness, invocation, setup_home, summarize, version_info
from recall import STOP_BETWEEN_CASES, aggregate_hash, capture, configured_defaults, dump, hashes, request_stop, utc_now
from workflow_runner import inventory, preserve_workspace, sandbox
from workflow_service import ProductService

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ('lean_runner.py', 'lean_world.py', 'lean_api.md', 'workflow_client.py', 'workflow_service.py',
           'workflow_runner.py', 'workflow_world.py', 'workflow_clock.py', 'workflow_calibrate.py',
           'native_harnesses.py', 'native_credentials_check.py', 'recall.py', 'fixtures.py')


def prompt(index: int, skill: bool) -> str:
    activation = 'Use $long-horizon at /workspace/skill/SKILL.md.\n' if skill else ''
    request = REQUEST if index == 0 else 'Continue the responsibility.'
    return activation + request + f'''

Environment: day {DAYS[index]}. This is a fresh session in /workspace/product; its files persist. Available connected tools are documented in /workspace/tools/API.md. /workspace/work is temporary output. The existing review calendar provides five checkpoints; this is checkpoint {index + 1}. Use the simulation's date and tools, not real websites, host files, live schedulers, paid services or other agents. Native model transport is separate. Finish after the useful work for this checkpoint. The outcome is your normal final response.
'''


def probe(command: list[str]) -> dict[str, bool]:
    script = '''import json,pathlib,subprocess
p=pathlib.Path
checks={name:not p(name).exists() for name in ['/home/deck','/root','/grader','/workspace/owner-facts.txt']}
checks['no_run_artifacts_in_skill']=not p('/workspace/skill/product').exists() and not p('/workspace/skill/session-0').exists()
f=p('/workspace/product/.probe');f.write_text('ok');f.unlink();checks['writable_project']=True
try:
 p('/workspace/tools/API.md').write_text('bad');checks['tools_read_only']=False
except OSError:checks['tools_read_only']=True
r=subprocess.run(['/usr/bin/python3','/workspace/tools/service.py','site.list'],text=True,capture_output=True,check=True)
checks['connected_service']=json.loads(r.stdout)['ok']
print(json.dumps(checks));raise SystemExit(not all(checks.values()))
'''
    result = subprocess.run(command + ['/usr/bin/python3', '-c', script], capture_output=True, text=True, timeout=20)
    result.check_returncode()
    value: dict[str, bool] = json.loads(result.stdout)
    return value


def session(harness: Harness, state: dict[str, Any], product: Path, output: Path,
            bundle: Path | None, index: int, live: bool, timeout: int, questions: Path) -> dict[str, Any]:
    output.mkdir(parents=True)
    request = prompt(index, bundle is not None)
    (output / 'prompt.txt').write_text(request)
    dump(output / 'state-before.json', state)
    metadata: dict[str, Any] = {'started_at': utc_now(), 'day': DAYS[index], 'fresh_session': True,
        'model_launch_attempted': False, 'wall_timeout_seconds': timeout, 'product_before': inventory(product),
        'prompt_sha256': hashlib.sha256(request.encode()).hexdigest(), 'installed_defaults': harness.defaults,
        'loaded_skill_hashes': hashes(bundle) if bundle else {}, 'owner_questions': 0, 'owner_wait_seconds': 0.0}
    dump(output / 'manifest.json', metadata)
    observed: set[bytes] = set()
    stop = threading.Event()
    temp_path: Path | None = None

    def dispatch(world: dict[str, Any], operation: str, args: dict[str, Any]) -> dict[str, Any]:
        if operation != 'owner.ask':
            return call(world, operation, args)
        question = args.get('question')
        if not isinstance(question, str) or not question.strip():
            return {'ok': False, 'error': 'Provide a question'}
        metadata['owner_questions'] += 1
        identity = f'{output.parent.name}-{index}-{metadata["owner_questions"]}'
        path = questions / f'{identity}.json'
        dump(path, {'question': question, 'session': str(output), 'status': 'pending'})
        print(f'OWNER {identity}: {question}', flush=True)
        answer_file = questions / f'{identity}.answer.txt'
        waiting_since = time.monotonic()
        deadline = waiting_since + 170
        while not answer_file.exists() and time.monotonic() < deadline and not stop.is_set():
            time.sleep(0.2)
        metadata['owner_wait_seconds'] += time.monotonic() - waiting_since
        if answer_file.exists():
            answer = answer_file.read_text()
            response = {'ok': True, 'answer': answer}
            dump(path, {'question': question, 'answer': answer, 'session': str(output), 'status': 'answered'})
        else:
            response = {'ok': False, 'error': 'Owner response unavailable; preserve uncertainty.'}
        world['events'].append({'day': world['day'], 'operation': operation, 'arguments': args, 'response': response})
        return response

    try:
        with tempfile.TemporaryDirectory(prefix='native-lean-', dir=ROOT / 'evals/runs') as temporary, \
             tempfile.TemporaryDirectory(prefix='lh-lean-socket-') as socket_dir:
            temp_path = Path(temporary)
            workspace = temp_path / 'workspace'
            shutil.copytree(product, workspace / 'product', symlinks=True)
            (workspace / 'work').mkdir()
            (workspace / 'tools').mkdir()
            shutil.copyfile(ROOT / 'evals/lean_api.md', workspace / 'tools/API.md')
            shutil.copyfile(ROOT / 'evals/workflow_client.py', workspace / 'tools/service.py')
            (workspace / 'tools/service.sock').touch()
            home = temp_path / 'private-home'
            setup_home(harness, home)

            def sample() -> None:
                while not stop.is_set():
                    try:
                        observed.update(extract(json.loads((home / '.codex/auth.json').read_bytes())))
                    except (OSError, ValueError):
                        pass
                    stop.wait(0.5)

            sampler = threading.Thread(target=sample, daemon=True)
            sampler.start()
            try:
                with ProductService(Path(socket_dir) / 'service.sock', state, output / 'service-state.json', dispatch):
                    command = sandbox(workspace, home, harness, bundle, Path(socket_dir) / 'service.sock')
                    command[-1] = '/workspace/product'
                    events = deepcopy(state['events'])
                    metadata['isolation_probe'] = probe(command)
                    state['events'] = events
                    if live:
                        metadata['model_launch_attempted'] = True
                        dump(output / 'manifest.json', metadata)
                        print(f'RUN {output.parent.name} checkpoint={index} day={state["day"]}', flush=True)
                        metadata.update(capture(command + invocation(harness, timeout, request), request, output, timeout))
                        dump(output / 'trace-summary.json', summarize(output / 'trace.jsonl.gz', harness))
            finally:
                stop.set()
                sampler.join()
                for source, target in [(workspace / 'product', output / 'product-after'), (workspace / 'work', output / 'work')]:
                    issues = preserve_workspace(source, target)
                    if issues:
                        metadata.setdefault('artifact_errors', []).extend(issues)
                metadata['product_after'] = inventory(output / 'product-after')
                dump(output / 'state-after.json', state)
                checked, hits = scan(output, observed)
                metadata['credential_scan'] = {'complete': True, 'streams': checked, 'matches': hits,
                    'values_persisted': False, 'limitation': 'Half-second sampling may miss intermediate refreshes.'}
                if hits or metadata.get('artifact_errors'):
                    raise ValueError('Artifact preservation or credential check failed')
            if live and metadata.get('exit_code') == 0 and not metadata.get('termination_reason'):
                shutil.rmtree(product)
                shutil.copytree(output / 'product-after', product, symlinks=True)
            elif live:
                STOP_BETWEEN_CASES.set()
    except Exception as error:
        metadata['infrastructure_error'] = type(error).__name__ + ': ' + str(error)
        STOP_BETWEEN_CASES.set()
    metadata['temporary_auth_home_removed'] = temp_path is not None and not temp_path.exists()
    metadata['finished_at'] = utc_now()
    dump(output / 'manifest.json', metadata)
    print(f'DONE {output.parent.name} checkpoint={index} exit={metadata.get("exit_code")} questions={metadata["owner_questions"]}', flush=True)
    return metadata


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--run', action='store_true')
    parser.add_argument('--timeout', type=int, default=600)
    parser.add_argument('--continue-from', type=Path, help='Continue only unattempted checkpoints from preserved state; never replay a session.')
    args = parser.parse_args()
    if not 60 <= args.timeout <= 600:
        parser.error('timeout must be between 60 and 600 seconds')
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    (ROOT / 'evals/runs').mkdir(exist_ok=True)
    (output / 'owner-questions').mkdir()
    (output / 'owner-facts.txt').write_text(OWNER_FACTS)
    source_run = args.continue_from.resolve() if args.continue_from else None
    shutil.copytree(ROOT / 'skills/long-horizon', output / 'bundle')
    shutil.copyfile(ROOT / 'evals/lean_protocol.md', output / 'protocol.md')
    for name in SOURCES:
        target = output / 'sources' / name
        target.parent.mkdir(exist_ok=True)
        shutil.copyfile(ROOT / 'evals' / name, target)
    binary = shutil.which('codex')
    if binary is None:
        raise ValueError('Codex is unavailable')
    harness = Harness('codex', Path(binary).resolve(), configured_defaults(Path.home() / '.codex'))
    original_hashes = hashes(output / 'sources')
    manifest: dict[str, Any] = {'started_at': utc_now(), 'live': args.run, 'planned_sessions': 10, 'days': DAYS,
        'harness': version_info(harness), 'binary_sha256': hashlib.sha256(harness.binary.read_bytes()).hexdigest(),
        'installed_defaults': harness.defaults, 'model_or_effort_override': False,
        'candidate_tree_sha256': aggregate_hash(hashes(output / 'bundle')), 'source_hashes': original_hashes,
        'protocol_sha256': hashlib.sha256((ROOT / 'evals/lean_protocol.md').read_bytes()).hexdigest(),
        'method': 'Two independent arms, five fixed checkpoints each. Only skill mount/activation differ. Same owner facts, answers only on request. No seeded histories or setup-topic checklist. The supplied calendar controls checkpoints; scheduler use is observed but cannot create extra sessions.',
        'limitations': ['One synthetic task, not independent repeated trials.', 'Approach-driven metrics do not assess copy quality.', 'Manual owner moderation; inspect question/answer parity.', 'No no-skill superiority or skill advantage is assumed.', 'Host files/processes isolated; model transport networking is available, product network restraint is instructional.']}
    dump(output / 'manifest.json', manifest)
    signal.signal(signal.SIGTERM, request_stop)
    signal.signal(signal.SIGINT, request_stop)
    worlds = {arm: initial() for arm in ('no-skill', 'skill')}
    start_index = 0
    if source_run:
        parent_manifest = json.loads((source_run / 'manifest.json').read_text())
        if not parent_manifest.get('finished_at'):
            raise ValueError('The preceding run must be finished')
        if parent_manifest['candidate_tree_sha256'] != manifest['candidate_tree_sha256']:
            raise ValueError('Skill content changed')
        if parent_manifest['binary_sha256'] != manifest['binary_sha256'] or parent_manifest['installed_defaults'] != harness.defaults:
            raise ValueError('Harness identity/defaults changed')
        for filename in SOURCES:
            if filename != 'lean_runner.py' and hashlib.sha256((ROOT / 'evals' / filename).read_bytes()).hexdigest() != parent_manifest['source_hashes'][filename]:
                raise ValueError('Case or tool source changed: ' + filename)
        previous = {arm: sorted((source_run / arm).glob('session-*')) for arm in worlds}
        lengths = {len(items) for items in previous.values()}
        if len(lengths) != 1 or not all(previous.values()):
            raise ValueError('Continuation requires the same attempted checkpoints in both arms')
        start_index = int(previous['skill'][-1].name.split('-')[-1]) + 1
        if not 0 < start_index < len(DAYS):
            raise ValueError('No unattempted checkpoints remain')
        for arm, items in previous.items():
            last = items[-1]
            if not json.loads((last / 'manifest.json').read_text())['model_launch_attempted']:
                raise ValueError('Cannot continue an unlaunched preparation')
            worlds[arm] = json.loads((last / 'state-after.json').read_text())
            shutil.copytree(last / 'product-after', output / arm / 'product', symlinks=True)
        manifest.update(continued_from=str(source_run), inherited_attempts=parent_manifest.get('inherited_attempts', 0) + parent_manifest['attempted_sessions'],
                        first_checkpoint=start_index, planned_new_sessions=2 * (len(DAYS) - start_index),
                        continuation_note='Preserve prior incomplete work and all original evidence. Only remaining checkpoints run; the wall-time guard was widened equally for both arms.')
        dump(output / 'manifest.json', manifest)
    else:
        for arm in worlds:
            product = output / arm / 'product'
            product.mkdir(parents=True)
            (product / 'README.md').write_text('# Benchside\n\nDeveloper buying guides with affiliate links. Content is in the connected CMS; tools are documented in /workspace/tools/API.md.\n')
            subprocess.run(['git', 'init', '-q', str(product)], check=True)
    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=2) as pool:
        for index in range(start_index, len(DAYS)):
            day = DAYS[index]
            if STOP_BETWEEN_CASES.is_set():
                break
            jobs = []
            for arm in worlds:
                advance(worlds[arm], day)
                jobs.append(pool.submit(session, harness, worlds[arm], output / arm / 'product', output / arm / f'session-{index}',
                                        output / 'bundle' if arm == 'skill' else None, index, args.run, args.timeout, output / 'owner-questions'))
            results.extend(job.result() for job in jobs)
    manifest.update(finished_at=utc_now(), attempted_sessions=sum(r['model_launch_attempted'] for r in results),
                    sessions=results, stopped=STOP_BETWEEN_CASES.is_set(),
                    frozen_sources_unchanged=hashes(output / 'sources') == original_hashes,
                    frozen_skill_unchanged=aggregate_hash(hashes(output / 'bundle')) == manifest['candidate_tree_sha256'])
    dump(output / 'manifest.json', manifest)
    return int(STOP_BETWEEN_CASES.is_set())


if __name__ == '__main__':
    raise SystemExit(main())
