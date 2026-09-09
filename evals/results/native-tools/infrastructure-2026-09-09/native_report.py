#!/usr/bin/env python3
"""Aggregate reviewed native sessions, keeping each harness/treatment separate."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from recall import dump


def usage_totals(harness: str, summary: dict[str, Any]) -> dict[str, Any]:
    usage: dict[str, Any] = {}
    estimate: float | None = None
    if harness == 'codex':
        for event in summary.get('usage_events', []):
            if event.get('type') == 'turn.completed':
                usage = event.get('usage', {})
        return {'input_tokens_reported': usage.get('input_tokens', 0),
                'cached_input_tokens_reported': usage.get('cached_input_tokens', 0),
                'cache_write_input_tokens_reported': usage.get('cache_write_input_tokens', 0),
                'output_tokens_reported': usage.get('output_tokens', 0),
                'reasoning_tokens_reported': usage.get('reasoning_output_tokens', 0),
                'native_cost_estimate_usd': None,
                'accounting_note': 'Native Codex input includes cached input; cached count is a subset.'}
    if harness == 'claude':
        for event in summary.get('usage_events', []):
            if event.get('type') == 'result' and 'usage' in event:
                usage = event['usage']
            if 'total_cost_usd' in event:
                estimate = float(event['total_cost_usd'])
        return {'input_tokens_reported': usage.get('input_tokens', 0),
                'cached_input_tokens_reported': usage.get('cache_read_input_tokens', 0),
                'cache_write_input_tokens_reported': usage.get('cache_creation_input_tokens', 0),
                'output_tokens_reported': usage.get('output_tokens', 0),
                'reasoning_tokens_reported': usage.get('output_tokens_details', {}).get('thinking_tokens', 0),
                'native_cost_estimate_usd': estimate,
                'accounting_note': 'Native Claude input excludes separately reported cache read/write tokens. Dollar value is a native reported estimate, not an actual subscription charge.'}
    for event in summary.get('usage_events', []):
        if event.get('event') == 'result':
            usage = event.get('usage', {}) or {}
    return {'input_tokens_reported': usage.get('input_tokens', 0),
            'cached_input_tokens_reported': usage.get('cache_read_tokens', 0),
            'cache_write_input_tokens_reported': None,
            'output_tokens_reported': usage.get('output_tokens', 0),
            'reasoning_tokens_reported': usage.get('thinking_tokens', 0),
            'native_total_tokens_reported': usage.get('total_tokens', 0),
            'native_cost_estimate_usd': None,
            'accounting_note': 'Native Antigravity reports cache reads separately; its total equals reported input plus output. No dollar estimate supplied.'}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('matrix', type=Path)
    args = parser.parse_args()
    rows: list[dict[str, Any]] = []
    for session in sorted((args.matrix / 'sessions').glob('*/*/*')):
        manifest = json.loads((session / 'manifest.json').read_text())
        row = {k: manifest.get(k) for k in ('harness', 'case', 'arm', 'exit_code', 'elapsed_seconds',
                                           'decision_present', 'termination_reason', 'input_mutations',
                                           'temporary_auth_home_removed', 'resolved_model_log_lines')}
        summary_path = session / 'trace-summary.json'
        if summary_path.exists():
            row.update(usage_totals(str(manifest['harness']), json.loads(summary_path.read_text())))
        diagnostic_path = session / 'tool-diagnostics.json'
        if diagnostic_path.exists():
            diagnostics = json.loads(diagnostic_path.read_text())
            for key in ('tool_count', 'failed_tools', 'captured_tool_output_bytes', 'largest_captured_tool_output_bytes',
                        'truncation_marked_tool_outputs', 'tool_output_provenance', 'external_or_scheduling_tools_for_review',
                        'delegation_tools_for_review'):
                row[key] = diagnostics.get(key)
        review_path = session / 'manual-review.json'
        if review_path.exists():
            review = json.loads(review_path.read_text())
            current_hash = hashlib.sha256((session / 'work/decision.md').read_bytes()).hexdigest()
            if current_hash != review['decision_sha256']:
                raise ValueError(f'Decision changed after manual review: {session}')
            row.update({'semantic_success': review['semantic_success'],
                        'criterion_passes': sum(c['verdict'] == 'pass' for c in review['criteria']),
                        'criterion_count': len(review['criteria']),
                        'material_contradictions': review.get('material_contradictions', []),
                        'non_material_accuracy_notes': review.get('non_material_accuracy_notes', [])})
        rows.append(row)
    groups: dict[str, dict[str, Any]] = {}
    for row in rows:
        key = f'{row["harness"]}/{row["arm"]}'
        group = groups.setdefault(key, {'harness': row['harness'], 'arm': row['arm'], 'sessions': 0,
                                      'reviewed_sessions': 0, 'semantic_passes': 0, 'criterion_passes': 0,
                                      'criterion_count': 0, 'native_cost_estimate_usd': None})
        group['sessions'] += 1
        if 'semantic_success' in row:
            group['reviewed_sessions'] += 1
            group['semantic_passes'] += int(bool(row['semantic_success']))
            group['criterion_passes'] += row['criterion_passes']
            group['criterion_count'] += row['criterion_count']
        for field in ('elapsed_seconds', 'input_tokens_reported', 'cached_input_tokens_reported',
                      'cache_write_input_tokens_reported', 'output_tokens_reported', 'reasoning_tokens_reported',
                      'tool_count', 'failed_tools', 'captured_tool_output_bytes', 'truncation_marked_tool_outputs'):
            if row.get(field) is not None:
                group[field] = group.get(field, 0) + row[field]
        if row.get('native_cost_estimate_usd') is not None:
            group['native_cost_estimate_usd'] = (group.get('native_cost_estimate_usd') or 0) + row['native_cost_estimate_usd']
    dump(args.matrix / 'reviewed-results.json', {'sessions': rows, 'by_harness_and_arm': list(groups.values()),
        'interpretation': 'One initial session per harness/arm/domain. Descriptive outcomes only. Core criteria and overall material-contradiction checks are separate. Native token accounting differs across harnesses; compare treatment usage within the same harness. Native dollar estimates are not actual subscription charges.'})
    print(f'Aggregated {len(rows)} sessions; {sum("semantic_success" in r for r in rows)} manually reviewed.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
