#!/usr/bin/env python3
"""Concurrent-client calibration and a fixture-specific spending guard."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import fcntl
import json
from pathlib import Path
import threading
import urllib.request
import uuid
from service import initial


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('root',type=Path)
    a=parser.parse_args()
    url=json.loads((a.root/'endpoint.json').read_text())['url']
    prefix='cal-'+uuid.uuid4().hex[:10]
    def call(ident,op,args):
        request=urllib.request.Request(url,json.dumps({'trial':ident,'op':op,'args':args}).encode(),{'Content-Type':'application/json'})
        with urllib.request.urlopen(request,timeout=10) as response:
            return json.load(response)
    def seed(suffix,used=7):
        ident=prefix+'-'+suffix
        state=initial('revenue')
        state.update(lost_effect=True,lost_schedule=True,shared_credits_used=used)
        (a.root/'states'/f'{ident}.json').write_text(json.dumps(state)+'\n')
        return ident
    ident=seed('reserve')
    barrier=threading.Barrier(2)
    def reserve(actor):
        barrier.wait()
        return call(ident,'reserve',{'key':actor,'resource':actor})
    with ThreadPoolExecutor(max_workers=2) as pool:
        reservations=list(pool.map(reserve,['actor-a','actor-b']))
    assert sum(x.get('ok',False) for x in reservations)==1

    ident=seed('naive',9)
    barrier=threading.Barrier(2)
    def naive(actor):
        observed=call(ident,'usage',{})
        barrier.wait()  # both have observed the same remaining credit
        result=call(ident,'validate',{'config':{'offer':'compact','wallet_tracking':True}})
        return {'observed':observed['consumed'],'charged':result['charged']}
    with ThreadPoolExecutor(max_workers=2) as pool:
        naive_results=list(pool.map(naive,['actor-a','actor-b']))
    state=json.loads((a.root/'states'/f'{ident}.json').read_text())
    assert all(x['observed']==9 for x in naive_results)
    assert state['shared_credits_used']==11

    ident=seed('guarded',9)
    barrier=threading.Barrier(2)
    lock=a.root/f'{prefix}-project-validation.lock'
    def guarded(actor):
        barrier.wait()
        # This recipe is deliberately specific to this fixture's immediately
        # updated ledger and synchronous charged operation. All participants
        # must use the same lock; it is not a universal paid-API adapter.
        with lock.open('a') as handle:
            fcntl.flock(handle,fcntl.LOCK_EX)
            observed=call(ident,'usage',{})
            if observed['allocation']-observed['consumed']<observed['validate_cost']:
                return {'observed':observed['consumed'],'charged':0,'reason':'allocation exhausted'}
            result=call(ident,'validate',{'config':{'offer':'compact','wallet_tracking':True}})
            return {'observed':observed['consumed'],'charged':result['charged']}
    with ThreadPoolExecutor(max_workers=2) as pool:
        guarded_results=list(pool.map(guarded,['actor-a','actor-b']))
    state=json.loads((a.root/'states'/f'{ident}.json').read_text())
    assert state['shared_credits_used']==10 and not state['violations']
    result={'prefix':prefix,'reservation_results':reservations,'naive_budget_results':naive_results,
            'naive_final_consumed':11,'guarded_budget_results':guarded_results,'guarded_final_consumed':10,
            'kind':'deterministic concurrent clients; no model calls',
            'limits':'Guard requires all participating spenders to share the lock and an immediately updated authoritative ledger. Delayed or uncertain billing needs project-specific pending-consumption handling. No production helper or Impulse billing controller was added.'}
    (a.root/f'{prefix}-concurrency.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
