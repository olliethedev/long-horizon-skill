#!/usr/bin/env python3
"""Summarize captured native tool traces without assigning semantic grades."""
from __future__ import annotations

import argparse
import gzip
import json
from pathlib import Path
import re
from typing import Any

from recall import dump

SOURCE_PATH = re.compile(r'history/[A-Za-z0-9_./-]+\.(?:md|json)')


def events(path: Path) -> list[dict[str, Any]]:
    result = []
    with gzip.open(path, 'rt', encoding='utf-8', errors='replace') as stream:
        for line in stream:
            try:
                value = json.loads(line)
                if isinstance(value, dict):
                    result.append(value)
            except ValueError:
                pass
    return result


def normalized_tools(trace: list[dict[str, Any]], harness: str) -> list[dict[str, Any]]:
    tools: list[dict[str, Any]] = []
    if harness == 'codex':
        for e in trace:
            item = e.get('item', {})
            if e.get('type') == 'item.completed' and item.get('type') == 'command_execution':
                tools.append({'id': item.get('id'), 'name': 'command_execution', 'input': item.get('command', ''),
                              'output': item.get('aggregated_output', ''), 'failed': item.get('exit_code', 0) != 0,
                              'exit_code': item.get('exit_code')})
    elif harness == 'claude':
        by_id: dict[str, dict[str, Any]] = {}
        for e in trace:
            for block in e.get('message', {}).get('content', []):
                if not isinstance(block, dict):
                    continue
                if block.get('type') == 'tool_use':
                    identifier = str(block['id'])
                    by_id[identifier] = {'id': identifier, 'name': block.get('name'),
                                          'input': block.get('input', {}), 'output': '', 'failed': False}
                if block.get('type') == 'tool_result':
                    tool = by_id.get(str(block.get('tool_use_id')))
                    if tool is not None:
                        tool['output'] = block.get('content', '')
                        tool['failed'] = block.get('is_error', False)
        tools = list(by_id.values())
    else:
        by_index: dict[int, dict[str, Any]] = {}
        for e in trace:
            step = e.get('step_update', {})
            if step.get('step_type') != 'tool':
                continue
            index = int(step['step_index'])
            item = by_index.setdefault(index, {'id': str(index), 'name': step.get('tool_name'),
                                                'input': {}, 'output': '', 'failed': False})
            info = step.get('tool_info', {})
            item['input'].update(info.get('parameters', {}))
            if 'output' in info:
                item['output'] = info['output']
            if step.get('state') in ('ERROR', 'FAILED'):
                item['failed'] = True
        tools = list(by_index.values())
    return tools


def diagnose(session: Path, declared_sources: set[str]) -> dict[str, Any]:
    manifest = json.loads((session / 'manifest.json').read_text())
    trace = events(session / 'trace.jsonl.gz')
    tools = normalized_tools(trace, str(manifest['harness']))
    provenance = 'native stdout trace'
    if manifest['harness'] == 'antigravity':
        transcripts = list((session / 'native-traces').glob('brain/*/.system_generated/logs/transcript_full.jsonl'))
        if len(transcripts) == 1:
            full = {int(row['step_index']): row for line in transcripts[0].read_text().splitlines()
                    if isinstance(row := json.loads(line), dict)}
            for tool in tools:
                index = int(tool['id'])
                if 'content' in full.get(index, {}):
                    tool['output'] = full[index]['content']
                for call in full.get(index - 1, {}).get('tool_calls', []):
                    if call.get('name') == tool['name']:
                        tool['input'].update(call.get('args', {}))
            provenance = 'native full transcript, matched to streamed tool step IDs'
    details = []
    for tool in tools:
        input_text = tool['input'] if isinstance(tool['input'], str) else json.dumps(tool['input'])
        output_text = tool['output'] if isinstance(tool['output'], str) else json.dumps(tool['output'])
        details.append({'id': tool['id'], 'name': tool['name'], 'input': tool['input'], 'failed': tool['failed'],
                        'captured_output_bytes': len(output_text.encode()),
                        'truncation_marker': any(s in output_text.lower() for s in ('truncat', 'output limit', 'too many matches')),
                        'source_path_mentions': sorted(set(SOURCE_PATH.findall(input_text + '\n' + output_text))),
                        'possible_external_or_auth_command': any(s in input_text.lower() for s in
                              ('curl ', 'wget ', 'https://', 'http://', '/eval-home', '/home/', 'auth.json', '.credentials', 'oauth-token'))})
    decision_path = session / 'work/decision.md'
    decision = decision_path.read_text() if decision_path.is_file() else ''
    cited = set(SOURCE_PATH.findall(decision))
    output_sizes = [int(tool['captured_output_bytes']) for tool in details]
    return {'harness': manifest['harness'], 'case': manifest['case'], 'arm': manifest['arm'],
            'tool_count': len(details), 'tools': details, 'tool_output_provenance': provenance,
            'failed_tools': sum(bool(t['failed']) for t in details),
            'captured_tool_output_bytes': sum(output_sizes), 'largest_captured_tool_output_bytes': max(output_sizes, default=0),
            'tool_outputs_over_20000_bytes': sum(n > 20000 for n in output_sizes),
            'truncation_marked_tool_outputs': sum(bool(t['truncation_marker']) for t in details),
            'possible_external_or_auth_commands_for_review': [t for t in details if t['possible_external_or_auth_command']],
            'external_or_scheduling_tools_for_review': [t for t in details if t['name'] in ('WebSearch', 'WebFetch', 'search_web', 'read_url_content', 'send_message', 'schedule', 'CronCreate', 'RemoteTrigger', 'ScheduleWakeup') or str(t['name']).startswith('browser_')],
            'delegation_tools_for_review': [t for t in details if t['name'] in ('Task', 'Agent', 'invoke_subagent', 'define_subagent')],
            'decision_source_paths': sorted(cited),
            'criterion_sources_cited': sorted(declared_sources & cited),
            'criterion_sources_not_cited_by_path': sorted(declared_sources - cited),
            'interpretation': 'Tool-output byte counts and path mentions are captured-trace diagnostics, not semantic grades or proof of complete reading. Antigravity uses its preserved full native transcript when available, because its stdout view_file events are concise metadata. Captured bytes are not a measurement of model-context token exposure. Threshold20k is descriptive only.'}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('matrix', type=Path)
    args = parser.parse_args()
    criteria = json.loads((args.matrix / 'criteria.json').read_text())
    summaries = []
    for session in sorted((args.matrix / 'sessions').glob('*/*/*')):
        if not (session / 'trace.jsonl.gz').exists():
            continue
        manifest = json.loads((session / 'manifest.json').read_text())
        if 'finished_at' not in manifest:
            continue
        sources = {s for c in criteria[manifest['case']] for s in c['sources'] if s.startswith('history/')}
        report = diagnose(session, sources)
        dump(session / 'tool-diagnostics.json', report)
        summaries.append({k: v for k, v in report.items() if k not in ('tools', 'interpretation')})
    dump(args.matrix / 'tool-diagnostics.json', summaries)
    print(f'Summarized {len(summaries)} completed native traces; no semantic grades assigned.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
