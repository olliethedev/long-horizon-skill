#!/usr/bin/env python3
"""Fork weekly final sessions from a completed matrix's day-240 records."""
import argparse
import json
from pathlib import Path
import shutil
import tempfile
from prepare import hashes


def prepare(source):
    original=json.loads((source/'manifest.json').read_text())
    root=Path(tempfile.mkdtemp(prefix='long-horizon-weekly-recheck-'))
    for name in ['trials','states','traces','snapshots','harness']:
        (root/name).mkdir()
    manifest={'status':'prepared','kind':'weekly final-session fixture correction',
        'source_matrix':str(source),'candidate_sha256':original['candidate_sha256'],
        'change':'Use the corrected weekly metrics endpoint without a new controlled comparison.',
        'cases':{},'evaluated_code_sha256':{k:v for k,v in hashes(Path(__file__).parent).items() if '/' not in k and k.endswith('.py')}}
    for ident,case in original['cases'].items():
        if case['domain']!='weekly-product':
            continue
        old=Path(case['path']);trial=root/'trials'/ident;trial.mkdir()
        for name in ['brief.md','task.md','API.md','service-client.py']:
            shutil.copy2(old/name,trial/name)
        shutil.copytree(old/'history',trial/'history')
        if case['arm']=='skill':
            shutil.copytree(old/'long-horizon',trial/'long-horizon')
        checkpoint=source/'snapshots'/ident/'epoch-4'
        for name in ['memory','project']:
            shutil.copytree(checkpoint/name,trial/name)
        (trial/'outbox').mkdir()
        shutil.copytree(source/'snapshots'/ident/'epoch-3/memory',root/'snapshots'/ident/'epoch-3/memory')
        shutil.copy2(checkpoint/'service-after.json',root/'states'/f'{ident}.json')
        manifest['cases'][ident]={'domain':case['domain'],'arm':case['arm'],'path':str(trial),
            'epochs':[],'common_input_sha256':case['common_input_sha256'],'forked_memory_from':str(checkpoint)}
    (root/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    config=source/'harness/configured-model.json'
    if config.exists():
        shutil.copy2(config,root/'harness/configured-model.json')
    return root


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('source',type=Path)
    print(json.dumps({'root':str(prepare(p.parse_args().source))}))
