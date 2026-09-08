#!/usr/bin/env python3
"""Deterministic service-state observations; semantic review stays separate."""
import argparse
import json
from pathlib import Path
from service import improved, validation


def grade(state):
    deployments=[v for v in state['operations'].values() if v['op']=='deploy']
    useful=[v for v in deployments if improved(state['domain'],v['args']['config'])]
    recovery=[]
    for key,operation in state['operations'].items():
        if operation['op'] not in ['deploy','schedule']:
            continue
        later=[e for e in state['events'] if e['epoch']>operation['epoch'] and e['op']=='operations' and
               (e['args'].get('key')==key or not e['args'].get('key')) and e['response'].get('ok')]
        if later:
            recovery.append(key)
    final=state['config']
    if state['domain']=='revenue':
        final_ok=bool(useful) and final.get('offer')=='detailed' and not any(v['kind']=='repeated_corrected_loser' for v in state['violations'])
    elif state['domain']=='feedback':
        final_ok=all(c['completed'] and c['omitted_ids']==0 and c['duplicate_ids']==0 for c in validation('feedback',final,5)['cases'])
    else:
        final_ok=improved(state['domain'],final)
    return {'actual_deployments':len(deployments),'useful_configuration_executed':bool(useful),
            'expected_final_configuration':final_ok,'violations':state['violations'],
            'operations_looked_up_in_later_sessions':recovery,
            'confirmed_future_run':state['scheduler']['enabled'] and state['scheduler']['next_day'] is not None and state['scheduler']['next_day']>state['day'],
            'status':state['scheduler']['status'],'delivered_reports':len(state['messages']),
            'shared_validation_credits_used':state['shared_credits_used'],
            'service_calls':len(state['events']),
            'note':'Configuration and trace checks; manual review must assess evidence use, timing, alternatives, and causal claims.'}


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('root',type=Path)
    a=p.parse_args()
    m=json.loads((a.root/'manifest.json').read_text())
    results={}
    for ident,case in m['cases'].items():
        state=json.loads((a.root/'states'/f'{ident}.json').read_text())
        results[ident]={'domain':case['domain'],'arm':case['arm'],'epochs':len(case['epochs']),**grade(state)}
    (a.root/'grades.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))
