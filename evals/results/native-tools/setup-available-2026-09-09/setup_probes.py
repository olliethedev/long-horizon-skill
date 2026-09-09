#!/usr/bin/env python3
"""Three opt-in offline scheduler-choice smoke probes, separate from recall."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict
import hashlib
from pathlib import Path
import shutil
import signal
from typing import Any

from fixtures import materialize
from native_harnesses import discover, version_info
from native_matrix import evaluate, freeze_bundles
from recall import archive_inputs, dump, hashes, request_stop, utc_now
from setup_fixtures import cases

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', action='store_true', help='Run three fresh native sessions; otherwise prepare and check isolation only.')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--timeout', type=int, default=600)
    parser.add_argument('--harness', action='append', choices=('codex', 'claude', 'antigravity'),
                        help='Run only this harness’s assigned case; repeat to select several. Default: all three.')
    args = parser.parse_args()
    if not 30 <= args.timeout <= 3600:
        parser.error('--timeout must be between 30 and 3600 seconds')
    output: Path = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    (ROOT / 'evals/runs').mkdir(exist_ok=True)
    signal.signal(signal.SIGINT, request_stop)
    signal.signal(signal.SIGTERM, request_stop)
    source_names = ('setup_probes.py', 'setup_fixtures.py', 'native_matrix.py',
                    'native_harnesses.py', 'native_fixtures.py', 'fixtures.py', 'recall.py')
    for name in source_names:
        shutil.copyfile(ROOT / 'evals' / name, output / name)
    source_hashes = hashes(output)
    bundles = freeze_bundles(output)
    harnesses = discover()
    # Three distinct setup behaviors, each exercised once. This small probe is
    # deliberately not a matched comparison of harnesses or treatments.
    planned_schedule = list(zip(harnesses, cases(), strict=True))
    schedule = [(h, case) for h, case in planned_schedule
                if args.harness is None or h.name in args.harness]
    selected = [case for _, case in schedule]
    for case in selected:
        materialize(case, output / 'inputs' / case.name)
    dump(output / 'criteria.json', {case.name: [asdict(c) for c in case.criteria] for case in selected})
    manifest: dict[str, Any] = {
        'started_at': utc_now(), 'live_run': args.run, 'intended_session_count': len(schedule),
        'source_hashes': source_hashes, 'bundles': bundles,
        'harnesses': [{'name': h.name, 'binary': str(h.binary),
                      'binary_sha256': hashlib.sha256(h.binary.read_bytes()).hexdigest(),
                      'installed_defaults': h.defaults, 'version': version_info(h)} for h in harnesses],
        'criteria_sha256': hashlib.sha256((output / 'criteria.json').read_bytes()).hexdigest(),
        'case_input_hashes': {case.name: hashes(output / 'inputs' / case.name) for case in selected},
        'schedule': [{'harness': h.name, 'case': case.name, 'arm': 'native-tools'} for h, case in schedule],
        'full_setup_plan': [{'harness': h.name, 'case': case.name, 'arm': 'native-tools'} for h, case in planned_schedule],
        'interpretation': 'One assigned offline setup case per harness, all using the revised skill. Distinct cases are not a matched harness comparison; selected subsets leave other planned probes pending.',
        'limitations': [
            'One offline setup case per harness, all using the revised skill; not a matched treatment comparison.',
            'Captured inventories and help establish setup reasoning, not actual discovery or scheduler execution.',
            'No installation, task registration, external communication, or live product changes are authorized.',
            'Execution status is separate from manual source-backed semantic grading.',
        ],
    }
    dump(output / 'manifest.json', manifest)
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(evaluate, h, case, 'native-tools', output, args.run, args.timeout)
                   for h, case in schedule]
        results = [future.result() for future in futures]
    manifest['results'] = results
    manifest['finished_at'] = utc_now()
    manifest['input_archive'] = archive_inputs(output)
    dump(output / 'manifest.json', manifest)
    return int(any(r.get('infrastructure_error') or r.get('not_launched') or
                   r.get('exit_code', 0) not in (0, None) or r.get('input_mutations') or
                   (args.run and not r.get('decision_present')) for r in results))


if __name__ == '__main__':
    raise SystemExit(main())
