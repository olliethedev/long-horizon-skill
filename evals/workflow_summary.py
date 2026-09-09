#!/usr/bin/env python3
"""Combine immutable workflow sessions and native usage; never assign semantic grades."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
from typing import Any

from native_diagnostics import events, session_tools
from native_report import usage_totals
from recall import dump, utc_now
from workflow_runner import inventory

FIELDS = ('elapsed_seconds', 'input_tokens_reported', 'cached_input_tokens_reported',
          'cache_write_input_tokens_reported', 'output_tokens_reported',
          'reasoning_tokens_reported', 'native_total_tokens_reported',
          'native_cost_estimate_usd', 'counted_tool_actions')


def summarize(original: Path, continuation: Path) -> dict[str, Any]:
    base = json.loads((original / 'manifest.json').read_text())
    extra = json.loads((continuation / 'manifest.json').read_text())
    if not all(m.get('live') and m.get('finished_at') for m in (base, extra)):
        raise ValueError('Only closed live batches can be summarized')
    if hashlib.sha256((original / 'manifest.json').read_bytes()).hexdigest() != extra['source_manifest_sha256']:
        raise ValueError('Continuation does not identify this original manifest')
    rows: list[dict[str, Any]] = []
    trajectories: list[dict[str, Any]] = []
    for case in base['schedule']:
        identity = '/'.join(case[k] for k in ('harness', 'domain', 'arm'))
        initial_folder = original / 'trajectories' / identity
        final_folder = continuation / 'trajectories' / identity
        initial = json.loads((initial_folder / 'trajectory.json').read_text())
        final = initial
        paths = list((initial_folder / 'sessions').glob('*/manifest.json'))
        if len(paths) != initial['actual_sessions']:
            raise ValueError('Original session inventory differs')
        if (final_folder / 'trajectory.json').exists():
            final = json.loads((final_folder / 'trajectory.json').read_text())
            if final['previous_sessions'] != initial['actual_sessions']:
                raise ValueError('Continuation prefix count differs')
            additions = list((final_folder / 'sessions').glob('*/manifest.json'))
            if len(additions) != final['actual_sessions']:
                raise ValueError('Continuation session inventory differs')
            paths += additions
        paths.sort(key=lambda p: int(p.parent.name))
        previous: dict[str, str] = {}
        days = []
        for index, path in enumerate(paths):
            session = path.parent
            m = json.loads(path.read_text())
            scan = m.get('credential_scan', {})
            if (m['index'] != index or not m.get('finished_at') or not m.get('model_launch_attempted')
                    or not scan.get('complete') or scan.get('matches')):
                raise ValueError('Repeated, missing, unfinished or uncleared native attempt')
            if m['product_before'] != previous or inventory(session / 'product-before') != previous:
                raise ValueError('Product carry-forward mismatch')
            previous = m['product_after']
            if inventory(session / 'product-after') != previous:
                raise ValueError('Retained product snapshot differs')
            batch = original.name if session.is_relative_to(original) else continuation.name
            relative = session.relative_to(original if batch == original.name else continuation)
            row = {**case, 'session_index': index, 'day': m['day'],
                   'artifact': f'{batch}/{relative}', 'manifest_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                   'elapsed_seconds': m.get('elapsed_seconds'), 'exit_code': m.get('exit_code'),
                   'infrastructure_error': m.get('infrastructure_error'),
                   'credential_scan': scan, 'temporary_auth_home_removed': m['temporary_auth_home_removed'],
                   'isolation_probe': m['isolation_probe'], 'fresh_session': m['fresh_session'],
                   'recovered_after_process_loss': m.get('recovered_after_process_loss', False),
                   'model_or_effort_override': m['model_or_effort_override']}
            row.update(usage_totals(case['harness'], json.loads((session / 'trace-summary.json').read_text())))
            trace_path = session / ('trace.jsonl-recovered.gz' if m.get('recovered_after_process_loss') else 'trace.jsonl.gz')
            provenance: Any
            if m.get('recovered_after_process_loss'):
                tools = [{'name': 'command_execution'} for event in events(trace_path)
                         if event.get('type') == 'item.completed' and event.get('item', {}).get('type') == 'command_execution']
                provenance = {'scope': 'Only complete command items in the recoverable trace prefix; incomplete native capture.'}
            else:
                tools, provenance = session_tools(session, case['harness'])
            names = Counter(str(tool['name']) for tool in tools)
            if case['harness'] == 'codex':
                completed = Counter(event.get('item', {}).get('type') for event in events(trace_path)
                                    if event.get('type') == 'item.completed')
                names['file_change'] = completed.get('file_change', 0)
                row['native_completed_item_types'] = dict(completed)
                row['unclassified_completed_types'] = sorted(set(completed) -
                    {'agent_message', 'reasoning', 'command_execution', 'file_change'})
            row.update(tool_counts_by_name=dict(names), counted_tool_actions=sum(names.values()),
                       tool_capture_provenance=provenance)
            rows.append(row)
            days.append(m['day'])
        count = len(paths)
        if inventory((final_folder if final is not initial else initial_folder) / 'product') != previous:
            raise ValueError('Final continuing workspace differs')
        state = final['state']
        failed = any(row['infrastructure_error'] or row['exit_code'] != 0
                     for row in rows if all(row[k] == case[k] for k in ('harness', 'domain', 'arm')))
        classification = ('infrastructure_failure' if failed else 'not_started' if not count else 'complete'
                          if final['stop_reason'] == 'horizon_or_no_further_wake' else 'resource_censored')
        calls = [e for e in state['events'] if e.get('type') == 'agent_call']
        trajectories.append({**case, 'sessions': count, 'days': days,
            'coverage': classification, 'stop_reason': final['stop_reason'],
            'semantic_grade': 'see source-backed review' if classification == 'complete' else 'not a complete outcome',
            'state_artifact': f'{continuation.name if final is not initial else original.name}/trajectories/{identity}/trajectory.json',
            'scheduler': state['scheduler'], 'revision': state['revision'], 'config': state['config'],
            'service_calls_by_operation': dict(Counter(e['op'] for e in calls)),
            'reports_delivered': sum(bool(e.get('response', {}).get('delivered')) for e in calls if e['op'] == 'report'),
            'confirmed_schedules': sum(bool(e.get('response', {}).get('ok')) for e in calls if e['op'] == 'schedule')})
    groups: dict[str, Any] = {}
    for row in rows:
        identity = '/'.join(row[k] for k in ('harness', 'domain', 'arm'))
        group = groups.setdefault(identity, {'recorded_attempts': 0, 'completed_sessions': 0, 'totals': {}, 'coverage': {}})
        group['recorded_attempts'] += 1
        group['completed_sessions'] += int(row['exit_code'] == 0 and not row['infrastructure_error'])
        for field in FIELDS:
            value = row.get(field)
            if value is not None:
                group['totals'][field] = group['totals'].get(field, 0) + value
                group['coverage'][field] = group['coverage'].get(field, 0) + 1
    if len(rows) > extra['maximum_total_launch_attempts'] or extra['reserved_launch_slots'] > 4:
        raise ValueError('Owner session cap exceeded')
    repo = Path(__file__).resolve().parents[1]
    return {'generated_at': utc_now(), 'semantic_grading': False, 'total_native_sessions': len(rows),
        'completed_native_sessions': sum(row['exit_code'] == 0 and not row['infrastructure_error'] for row in rows),
        'planned_trajectories': len(trajectories), 'coverage': dict(Counter(t['coverage'] for t in trajectories)),
        'skill_tree': base['skill_tree'], 'harnesses': base['harnesses'],
        'postprocessing_source_hashes': {str(p.relative_to(repo)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in [Path(__file__).resolve()] + [repo / 'evals' / name for name in
                ('native_diagnostics.py', 'native_report.py', 'recall.py', 'workflow_runner.py')]},
        'sessions': rows, 'trajectories': trajectories, 'usage_by_trajectory': groups,
        'notes': ['All original assigned cases retained; unfinished cases are not passes or failures.',
            'Sessions form dependent trajectories; 50 sessions are not 50 independent experiments.',
            'Compare native token categories only within harness. Codex input includes cached input; Claude input excludes cache reads/writes.',
            'Antigravity native total equals reported input plus output; cache and thinking are separately reported and must not be added blindly.',
            'Native dollar estimates are not subscription charges. Missing categories stay absent with coverage counts.',
            'Tool counts use native completed actions; one Codex file-change item may modify multiple files.']}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('original', type=Path)
    parser.add_argument('continuation', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = summarize(args.original.resolve(), args.continuation.resolve())
    dump(args.output, result)
    print(json.dumps({key: result[key] for key in ('total_native_sessions', 'planned_trajectories', 'coverage')}))


if __name__ == '__main__':
    main()
