#!/usr/bin/env python3
"""Opt-in real-clock Impulse integration in a separate IMPULSE_HOME."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
from typing import Any, Callable


def write(path: Path, value: Any) -> None:
    with path.open('w') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())


def call(binary: str, env: dict[str, str], *args: str) -> dict[str, Any]:
    result = subprocess.run([binary, *args, '--json'], env=env, text=True,
                            capture_output=True, timeout=20)
    payload: dict[str, Any] = json.loads(result.stdout)
    if result.returncode != 0 or payload.get('ok') is not True:
        raise RuntimeError(f'Impulse {args[:2]} failed: {payload}')
    return payload


def worker(root: Path, binary: str) -> int:
    env = dict(os.environ)
    action = root / 'action.json'
    if not action.exists():
        intent: dict[str, Any] = {'request_id': 'observe-once', 'input': ['task', 'next', '--after', '12s'],
                  'created_at': datetime.now(timezone.utc).isoformat(), 'pid': os.getpid()}
        write(root / 'intent.json', intent)
        receipt = call(binary, env, *intent['input'], '--request-id', intent['request_id'])
        replay = call(binary, env, *intent['input'], '--request-id', intent['request_id'])
        if receipt != replay:
            raise RuntimeError('Same request identity produced a different scheduling receipt.')
        write(action, {'intent': intent, 'receipt': receipt})
        return 17  # Explicit continuation must survive this failure.
    previous = json.loads(action.read_text())
    current = call(binary, env, 'run', 'show', '--current')
    disabled = call(binary, env, 'task', 'disable', '--request-id', 'bounded-complete')
    write(root / 'recovery.json', {'pid': os.getpid(), 'recovered': previous,
        'current_run': current, 'disabled': disabled,
        'observed_at': datetime.now(timezone.utc).isoformat()})
    return 0


def exercise(output: Path, binary: str) -> None:
    output.mkdir(parents=True, exist_ok=False)
    root = Path(tempfile.mkdtemp(prefix='long-horizon-impulse-'))
    env = dict(os.environ)
    env.pop('IMPULSE_CONTEXT', None)  # Operator test must not inherit a live assignment context.
    env['IMPULSE_HOME'] = str(root / 'impulse')
    trace: list[dict[str, Any]] = []
    task_id: str | None = None

    def command(*args: str) -> dict[str, Any]:
        try:
            response = call(binary, env, *args)
        except Exception as exc:
            trace.append({'at': datetime.now(timezone.utc).isoformat(), 'args': args, 'error': str(exc)})
            raise
        trace.append({'at': datetime.now(timezone.utc).isoformat(), 'args': args, 'response': response})
        return response

    def wait_for(predicate: Callable[[], list[dict[str, Any]] | None]) -> list[dict[str, Any]]:
        deadline = time.monotonic() + 60
        while time.monotonic() < deadline:
            result = predicate()
            if result:
                return result
            time.sleep(0.25)
        raise TimeoutError('Isolated Impulse run did not reach the expected state within 60 seconds.')

    failure: BaseException | None = None
    try:
        assert command('task', 'list')['data'] == []
        definition = root / 'task.toml'
        argv = [sys.executable, str(Path(__file__).resolve()), '--worker', str(root), '--impulse', binary]
        definition.write_text('schema_version = 1\nname = "long-horizon-integration"\ncwd = "."\n'
            '[work]\nkind = "script"\ncommand = ' + json.dumps(argv) + '\n'
            '[first_run]\nkind = "now"\n[notifications]\non_success = false\non_failure = false\non_interruption = false\n')
        command('task', 'validate', str(definition))
        command('task', 'preview', str(definition))
        task_id = command('task', 'register', str(definition))['data']['id']

        def failed_first() -> list[dict[str, Any]] | None:
            runs: list[dict[str, Any]] = command('run', 'list', '--task', str(task_id))['data']
            return runs if len(runs) == 1 and runs[0]['status'] == 'failed' else None

        first = wait_for(failed_first)
        before = command('task', 'show', task_id)['data']
        assert before['next'] is not None
        original_action = (root / 'action.json').read_bytes()
        command('daemon', 'stop')
        stopped = command('daemon', 'status')['data']
        assert stopped['running'] is False
        time.sleep(1)
        command('daemon', 'start')

        def finished_second() -> list[dict[str, Any]] | None:
            runs: list[dict[str, Any]] = command('run', 'list', '--task', str(task_id))['data']
            return runs if len(runs) == 2 and sorted(r['status'] for r in runs) == ['failed', 'succeeded'] else None

        runs = wait_for(finished_second)
        final = command('task', 'show', task_id)['data']
        assert final['enabled'] is False and final['next'] is None
        assert (root / 'action.json').read_bytes() == original_action
        recovery = json.loads((root / 'recovery.json').read_text())
        assert recovery['pid'] != recovery['recovered']['intent']['pid']
        assert len({r['id'] for r in runs}) == 2
        write(root / 'result.json', {'passed': True, 'runs': runs, 'first_failed_run': first[0]['id'],
            'final_task': final, 'action_sha256': hashlib.sha256(original_action).hexdigest(),
            'checks': ['relative continuation survives failed run and daemon restart',
                       'same request-id replays one scheduling receipt',
                       'fresh process recovers retained files', 'bounded completion disables future work'],
            'limitations': ['script exercise, not a model-driven product pilot', 'seconds of real elapsed time, not months'],
            'impulse_version': command('--version')['data']})
    except BaseException as exc:
        failure = exc
        write(root / 'result.json', {'passed': False, 'error': str(exc)})
    finally:
        cleanup_errors: list[str] = []

        def cleanup(*args: str) -> dict[str, Any] | None:
            try:
                return command(*args)
            except Exception as exc:
                cleanup_errors.append(str(exc))
                return None

        if task_id:
            cleanup('task', 'disable', task_id)
            remaining = cleanup('run', 'list', '--task', task_id)
            if remaining:
                for run in remaining['data']:
                    if run['status'] in {'queued', 'launching', 'running', 'stopping', 'uncertain'}:
                        cleanup('run', 'stop', run['id'], '--force')
        cleanup('daemon', 'stop')
        stopped = cleanup('daemon', 'status')
        if stopped and stopped['data']['running']:
            cleanup_errors.append('Isolated daemon still reports running.')
        write(output / 'cleanup.json', {'errors': cleanup_errors, 'daemon_status': stopped})
        if cleanup_errors:
            failure = failure or RuntimeError('Isolated cleanup failed; inspect cleanup.json and trace.json.')
            result = json.loads((root / 'result.json').read_text())
            result.update({'passed': False, 'cleanup_errors': cleanup_errors})
            write(root / 'result.json', result)
        write(output / 'trace.json', trace)
        for name in ['result.json', 'intent.json', 'action.json', 'recovery.json', 'task.toml']:
            if (root / name).exists():
                shutil.copy2(root / name, output / name)
        shutil.copy2(__file__, output / 'impulse_integration.py')
        write(output / 'provenance.json', {'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'temporary_root': str(root), 'isolation': 'IMPULSE_HOME; inherited IMPULSE_CONTEXT removed',
            'private_state_not_archived': True})
    print(json.dumps({'results': str(output), 'passed': failure is None}), flush=True)
    if failure:
        raise failure


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--worker', type=Path)
    parser.add_argument('--output', type=Path, default=Path('evals/results/impulse-v1'))
    parser.add_argument('--impulse', default=shutil.which('impulse'))
    args = parser.parse_args()
    if not args.impulse:
        parser.error('Install Impulse first.')
    if args.worker:
        sys.exit(worker(args.worker, args.impulse))
    exercise(args.output, args.impulse)
