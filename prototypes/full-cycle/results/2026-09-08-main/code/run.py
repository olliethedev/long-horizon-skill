#!/usr/bin/env python3
"""Run paired fresh Codex processes with snapshots and independent traces."""
import argparse
import asyncio
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import time
from service import advance,DAYS


def hashes(path):
    return {str(p.relative_to(path)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(path.rglob('*')) if p.is_file()}


def usage(log):
    found=[]
    with log.open() as f:
        for line in f:
            try:
                event=json.loads(line)
            except json.JSONDecodeError:
                continue
            if 'usage' in event:
                found.append(event['usage'])
    return found


async def run(root,selected,epochs,concurrency):
    manifest_path=root/'manifest.json'
    manifest=json.loads(manifest_path.read_text())
    endpoint=json.loads((root/'endpoint.json').read_text())['url']
    sem=asyncio.Semaphore(concurrency)
    # No model or reasoning override: retain this installation's configured defaults.
    base_args=['codex','exec','--json','--ephemeral','--skip-git-repo-check',
               '-s','workspace-write','-c','sandbox_workspace_write.network_access=true',
               '-c','approval_policy="never"']
    manifest['codex_version']=subprocess.check_output(['codex','--version'],text=True).strip()
    manifest['harness_args']=base_args
    manifest['service_url']=endpoint
    manifest['status']='running'
    controller_hash=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    shutil.copy2(Path(__file__),root/'harness'/f'controller-{controller_hash}.py')
    manifest.setdefault('controller_batches',[]).append({'sha256':controller_hash,'cases':selected,'epochs':epochs})
    manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')

    async def chain(ident):
        case=manifest['cases'][ident]
        trial=Path(case['path'])
        (trial/'connection.json').write_text(json.dumps({'url':endpoint,'trial':ident})+'\n')
        for epoch in epochs:
            if any(x['epoch']==epoch for x in case['epochs']):
                continue
            async with sem:
                if any(x['exit_code']!=0 for x in case['epochs']):
                    print(json.dumps({'case':ident,'skipped':epoch,'reason':'prior failed process requires review'}),flush=True)
                    break
                state_path=root/'states'/f'{ident}.json'
                state=json.loads(state_path.read_text())
                advance(state,epoch)
                state_path.write_text(json.dumps(state,indent=2)+'\n')
                reasons=['initial assignment','recovery after service interruption','early observation/checkpoint','mature observation checkpoint','later source-audit event','later customer review']
                reason=case.get('run_reasons',{}).get(str(epoch),reasons[epoch])
                (trial/'run-context.md').write_text(f'# Current run\n\nFixture day {DAYS[epoch]}. Wake reason: {reason}. Read the current service state and signals. This is a fresh session.\n')
                folder=root/'snapshots'/ident/f'epoch-{epoch}'
                folder.mkdir(parents=True)
                injections=[]
                if epoch==5:
                    old=root/'snapshots'/ident/'epoch-3/memory'
                    for name in ['current.md','handoff.md','CURRENT.md','HANDOFF.md']:
                        current=trial/'memory'/name
                        previous=old/name
                        if current.is_file() and previous.is_file() and current.read_bytes()!=previous.read_bytes():
                            shutil.copy2(current,folder/f'pre-injection-{name}')
                            shutil.copy2(previous,current)
                            injections.append({'kind':'stale_handoff_restore','path':'memory/'+name,'source_epoch':3})
                    for name in ['index.md','INDEX.md']:
                        index=trial/'memory'/name
                        if index.is_file():
                            shutil.copy2(index,folder/f'pre-injection-{name}')
                            index.unlink()
                            injections.append({'kind':'missing_index','path':'memory/'+name})
                for name in ['memory','project']:
                    shutil.copytree(trial/name,folder/f'input-{name}')
                for name in ['brief.md','task.md','API.md']:
                    shutil.copy2(trial/name,folder/f'input-{name}')
                shutil.copy2(trial/'run-context.md',folder/'run-context.md')
                shutil.copy2(state_path,folder/'service-before.json')
                input_hashes=hashes(trial)
                prompt='Complete the current session in task.md for this trial. '
                if case['arm']=='skill':
                    prompt+='Use $long-horizon at long-horizon/SKILL.md. '
                prompt+='Follow the trial access and output restrictions. Do the authorized work and end when a later observation or service interruption requires a new session.'
                log=root/'harness'/f'{ident}-{epoch}.jsonl'
                err=root/'harness'/f'{ident}-{epoch}.stderr'
                start=time.monotonic()
                started=datetime.now(timezone.utc).isoformat()
                print(json.dumps({'started':ident,'domain':case['domain'],'arm':case['arm'],'epoch':epoch}),flush=True)
                with log.open('wb') as out,err.open('wb') as stderr:
                    process=await asyncio.create_subprocess_exec(*base_args,'-C',str(trial),'-o',str(trial/'outbox/final.md'),'-',
                        stdin=asyncio.subprocess.PIPE,stdout=out,stderr=stderr)
                    try:
                        await asyncio.wait_for(process.communicate(prompt.encode()),timeout=600)
                        code=process.returncode
                    except asyncio.TimeoutError:
                        process.terminate()
                        await process.wait()
                        code=124
                for name in ['memory','project','outbox']:
                    shutil.copytree(trial/name,folder/name)
                shutil.copy2(state_path,folder/'service-after.json')
                case['epochs'].append({'epoch':epoch,'prompt':prompt,'started_utc':started,
                    'controller_sha256':controller_hash,'injections':injections,
                    'elapsed_seconds':round(time.monotonic()-start,2),'exit_code':code,
                    'input_sha256':input_hashes,'output_sha256':hashes(trial),
                    'usage_events':usage(log),'harness_trace':str(log)})
                manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
                shutil.rmtree(trial/'outbox')
                (trial/'outbox').mkdir()
                print(json.dumps({'completed':ident,'epoch':epoch,'exit_code':code,'seconds':case['epochs'][-1]['elapsed_seconds']}),flush=True)
    await asyncio.gather(*(chain(x) for x in selected))
    manifest['status']='batch_finished'
    manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('root',type=Path)
    p.add_argument('--cases',nargs='*')
    p.add_argument('--epochs',nargs='+',type=int,default=list(range(6)))
    p.add_argument('--concurrency',type=int,default=3)
    a=p.parse_args()
    m=json.loads((a.root/'manifest.json').read_text())
    asyncio.run(run(a.root,a.cases or list(m['cases']),a.epochs,a.concurrency))
