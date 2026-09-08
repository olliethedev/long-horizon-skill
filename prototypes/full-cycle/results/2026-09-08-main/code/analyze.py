#!/usr/bin/env python3
"""Summarize captured harness evidence without another model call."""
import argparse
import json
from pathlib import Path


def analyze(root):
    manifest=json.loads((root/'manifest.json').read_text())
    result={'cases':{},'limitations':['captured command output may itself be truncated','command text is not complete OS read isolation','token telemetry is not billed cost or remaining subscription quota']}
    threads=[]
    for ident,case in manifest['cases'].items():
        sessions=[]
        for epoch in case['epochs']:
            log=root/'harness'/f"{ident}-{epoch['epoch']}.jsonl"
            stats={'epoch':epoch['epoch'],'exit_code':epoch['exit_code'],'seconds':epoch['elapsed_seconds'],
                'commands':0,'command_errors':0,'captured_output_chars':0,'million_char_outputs':[],
                'candidate_read_command_seen':False,'file_changes_outside_trial':[],
                'readonly_input_changes':[], 'usage':epoch.get('usage_events',[]),
                'injections':epoch.get('injections',[])}
            for line in log.read_text().splitlines():
                try:
                    event=json.loads(line)
                except json.JSONDecodeError:
                    continue
                if event.get('type')=='thread.started':
                    threads.append(event['thread_id'])
                    stats['thread_id']=event['thread_id']
                item=event.get('item',{})
                if event.get('type')!='item.completed':
                    continue
                if item.get('type')=='command_execution':
                    stats['commands']+=1
                    stats['command_errors']+=item.get('exit_code',0)!=0
                    command=item.get('command','')
                    size=len(item.get('aggregated_output',''))
                    stats['captured_output_chars']+=size
                    if size>1000000:
                        stats['million_char_outputs'].append({'command':command,'chars':size})
                    if 'long-horizon/SKILL.md' in command:
                        stats['candidate_read_command_seen']=True
                elif item.get('type')=='file_change':
                    for change in item.get('changes',[]):
                        path=Path(change['path'])
                        if path.is_absolute() and not path.is_relative_to(Path(case['path'])):
                            stats['file_changes_outside_trial'].append(str(path))
            for name,expected in case.get('common_input_sha256',{}).items():
                if Path(name).parts[0] in ['memory','project','outbox']:
                    continue
                if epoch['output_sha256'].get(name)!=epoch['input_sha256'].get(name,expected):
                    stats['readonly_input_changes'].append(name)
            if case['arm']=='skill':
                for name,expected in manifest['candidate_sha256'].items():
                    if epoch['output_sha256'].get('long-horizon/'+name)!=expected:
                        stats['readonly_input_changes'].append('long-horizon/'+name)
            memory=root/'snapshots'/ident/f"epoch-{epoch['epoch']}"/'memory'
            files=[p for p in memory.rglob('*') if p.is_file()]
            stats['memory_files']=len(files)
            stats['memory_bytes']=sum(p.stat().st_size for p in files)
            sessions.append(stats)
        result['cases'][ident]={'domain':case['domain'],'arm':case['arm'],'focus':case.get('focus'),'sessions':sessions}
    result['attempted_sessions']=sum(len(x['sessions']) for x in result['cases'].values())
    result['unique_thread_ids']=len(set(threads))
    result['thread_id_count']=len(threads)
    result['all_recorded_threads_distinct']=len(threads)==len(set(threads))
    (root/'analysis.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('root',type=Path)
    a=p.parse_args()
    result=analyze(a.root)
    print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))
