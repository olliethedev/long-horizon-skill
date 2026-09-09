#!/usr/bin/env python3
"""Opt-in neutral native tool-execution preflight; never reads an evaluation case."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict
from pathlib import Path
import shutil
import subprocess
import tempfile
from typing import Any

from native_harnesses import Harness, boundary, bubble, discover, invocation, setup_home, summarize
from recall import capture, dump, hashes, utc_now

ROOT = Path(__file__).resolve().parents[1]
PROMPT = ('Read /workspace/product/note.txt using a local tool, then use a local tool to write '
          'its exact single line to /workspace/work/decision.md. Finish by stating the file path. '
          'Use only these local files; do not contact external services or inspect credentials.\n')


def preflight(h: Harness, output: Path, run: bool) -> dict[str, Any]:
    out = output / h.name
    out.mkdir()
    (out / 'prompt.txt').write_text(PROMPT)
    with tempfile.TemporaryDirectory(prefix=f'native-preflight-{h.name}-', dir=ROOT / 'evals/runs') as temp:
        root = Path(temp)
        workspace = root / 'workspace'
        (workspace / 'product').mkdir(parents=True)
        (workspace / 'work').mkdir()
        (workspace / 'product/note.txt').write_text('The copper lantern is beside the north window.\n')
        private_home = root / 'private-home'
        setup_home(h, private_home)
        base = bubble(workspace, private_home, h)
        result: dict[str, Any] = {'harness': h.name, 'defaults': h.defaults,
                                  'binary': str(h.binary), 'started_at': utc_now(), 'boundary': boundary(base, h)}
        help_result = subprocess.run(base + ['/opt/harness', '--help'], capture_output=True, text=True, timeout=20)
        (out / 'help.stdout').write_text(help_result.stdout)
        (out / 'help.stderr').write_text(help_result.stderr)
        if help_result.returncode:
            raise RuntimeError(f'{h.name} help probe failed')
        result['command'] = base + invocation(h, 180)
        dump(out / 'manifest.json', result)
        if run:
            print(f'{utc_now()} PREFLIGHT {h.name}', flush=True)
            result.update(capture(result['command'], PROMPT, out, 190))
            dump(out / 'trace-summary.json', summarize(out / 'trace.jsonl.gz', h))
            shutil.copytree(workspace / 'work', out / 'work')
            decision = workspace / 'work/decision.md'
            result['tool_result_verified'] = decision.is_file() and decision.read_text().strip() == 'The copper lantern is beside the north window.'
        result['finished_at'] = utc_now()
    result['temporary_auth_home_removed'] = not root.exists()
    dump(out / 'manifest.json', result)
    print(f'{utc_now()} PREFLIGHT DONE {h.name} {result.get("exit_code")} {result.get("tool_result_verified")}', flush=True)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', action='store_true')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--harness', choices=('codex', 'claude', 'antigravity'), action='append')
    args = parser.parse_args()
    out: Path = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    (ROOT / 'evals/runs').mkdir(exist_ok=True)
    for file in ('native_preflight.py', 'native_harnesses.py', 'recall.py', 'fixtures.py'):
        shutil.copyfile(ROOT / 'evals' / file, out / file)
    selected = [h for h in discover() if not args.harness or h.name in args.harness]
    results = []
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(preflight, h, out, args.run) for h in selected]
        for future in futures:
            results.append(future.result())
    dump(out / 'manifest.json', {'started_at': utc_now(), 'run': args.run, 'source_hashes': hashes(out), 'results': results})
    return int(any(r.get('exit_code', 0) or (args.run and not r.get('tool_result_verified')) for r in results))


if __name__ == '__main__':
    raise SystemExit(main())
