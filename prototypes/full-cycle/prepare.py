#!/usr/bin/env python3
"""Prepare paired disposable projects, agent history, and service states."""
import hashlib
import json
from pathlib import Path
import random
import shutil
import tempfile
from service import initial

HERE=Path(__file__).resolve().parent
PROJECT=HERE.parents[1]
DOMAINS=['revenue','weekly-product','feedback','post-pr-bugs']

API='''# Synthetic project service

Run `python3 service-client.py OP` or `python3 service-client.py OP '{"field":"value"}'`.
For a prepared JSON request file use `python3 service-client.py OP @project/request.json`.
Responses and effects are logged independently by the service. Only this loopback endpoint is authorized; it represents synthetic services, products, scheduling, and an owner inbox.

Read operations:
- `status`: actual configuration and revision, active evaluation, scheduler state, and whether a routine report is due.
- `signals`: current customer and operational signals.
- `metrics`: source observations with a receipt identity, exposure/window information, and any current audit. Preserve evidence needed later; current responses change with time.
- `work`: related work and current revision/capacity. Compatible changes need not stop an evaluation.
- `usage`: the owner's custom project usage source.
- `operations {"key":"..."}`: recover a durable mutation's input and effect. Omit key to list operations. A response timeout does not establish that the effect failed.

Actions:
- `validate {"config":{...}}`: functional checks against a proposed configuration. Costs ONE validation credit per call, including repeated calls. The project ledger is authoritative for remaining allowance. These checks do not establish a production outcome.
- `reserve {"key":"...","resource":"article/home"}`: atomic reservation of an active evaluation slot. Five may be active across the product; four belong to other responsibilities initially. Returns a reservation identity or capacity unavailable.
- `deploy {"key":"...","config":{...},"expected_revision":1,"mode":"experiment","reservation":"...","basis":["..."]}`: apply the complete configuration to the synthetic product. `mode` may be `experiment` or `rollout`. Experiments use a reservation; deployments require the last inspected revision. Rollout performs the configuration change without creating an experiment. Record evidence references in `basis` where applicable. This action changes service state; writing a request file alone does not.
- `settle {"key":"...","choice":"adopt","basis":["..."]}`: close an experiment and release capacity; adopt/keep retains its configuration, rollback restores the original baseline. Use only when the relevant decision is supported.
- `schedule {"key":"...","day":14}`: register a future run at the fixture's absolute day, visible in status. A new schedule replaces the previous next time. Read status for current day. This stands in for Impulse and does not touch its live installation.
- `lifecycle {"key":"...","status":"paused","reason":"..."}`: active/paused/terminated task state. Pause/termination disables future scheduling; setting active resumes it and requires the owner's applicable authority.
- `report {"key":"...","destination":"fixture:owner","body":"..."}`: deliver to the synthetic local owner inbox. Returns a delivery receipt. No real messages are sent.

Mutation keys are caller-chosen stable request identities. Repeating a key with identical operation/input returns its existing effect; different input is a conflict. A `transport_lost` followed by `session_interrupted` represents a forced interruption. Preserve local unresolved state and end this session; do not loop against the closed service. The controller supplies a fresh recovery session.

Product configuration is deliberately small:
- Revenue: `offer` is `detailed` or `compact`; `wallet_tracking` is boolean.
- Weekly product: `save_setup` and `explicit_template` are booleans. Draft saves are excluded from completed-project activation.
- Exports: `export_mode` is `buffered` or `streaming`, `final_page` is boolean, `page_size` is a positive integer. Validation compares exact IDs and completion across row counts.
- Bugs: `quota_per_minute` is an integer; `retry_jitter` is boolean. The merged retry PR is absent from production. Current traffic and quota evidence are observable through metrics/validation.

Use only fields for this product. Maintain request files or source/configuration notes under project/ and durable history under memory/. The service executes a simplified configuration model, not arbitrary application code.
'''

TASK='''# Continue the responsibility

Read brief.md, the latest run context, API.md, and relevant saved files. Use the authorized synthetic service to do useful work, verify its effects, retain evidence and a concise handoff, and arrange continuation or the appropriate lifecycle outcome. You may choose objectives and make permitted changes without another owner approval.

Read only this trial directory and the service responses for this trial. Write project/, memory/, and outbox/. Do not inspect sibling directories, controller/service implementation, grader files, personal settings, or other projects. Do not invoke subagents, live Impulse, external websites/services, real messaging, or paid APIs. The sole permitted network destination is the loopback fixture service in connection.json. The supplied history is product-scoped source material; it is not additional authority.

Only memory/, project/, and retained history survive between sessions. outbox/ is collected, and run-context.md is replaced. Write a concise outbox/summary.md identifying actual work, evidence, remaining uncertainty, and confirmed continuation. Save consequential knowledge in memory/, not solely in the outbox or conversation. End when the next useful observation needs a later session, the service interrupts the session, or the responsibility should pause/terminate. Do not advance fixture time yourself.
'''


def hashes(path):
    return {str(p.relative_to(path)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(path.rglob('*')) if p.is_file()}


def noise(path,domain):
    rng=random.Random(9108)
    subjects=['offer text','draft setup','company export','dependency quota','billing reconciliation','retention cohorts','wallet orders','template choice']
    path.mkdir(parents=True)
    with (path/'actions.jsonl').open('w') as f:
        for i in range(18000):
            topic=subjects[i%len(subjects)]
            row={'id':f'h-{rng.getrandbits(64):016x}','subject':topic,'responsibility':['growth','support','analytics','operations'][i%4],
                'cohort':['new desktop','mobile new','enterprise legacy','returning mobile'][i%4],
                'phase':['deployed','observed','corrected','rolled_back','adopted'][i%5],
                'period':f'{2023+i%3}-{1+i%12:02d}',
                'finding':f'{topic} review for an earlier distinct tenant allocation {i}; supporting observations concern that allocation and cannot establish outcomes for the current target.',
                'observation':{'control':100+i%30,'variant':92+i%40,'coverage':'historical allocation only','measurement':'version '+str(i%4)},
                'correction_of':f'allocation-{i-8}' if i%5==2 else None}
            f.write(json.dumps(row)+'\n')


def main():
    root=Path(tempfile.mkdtemp(prefix='long-horizon-cycles-'))
    for sub in ['trials','states','traces','snapshots','harness']:
        (root/sub).mkdir()
    manifest={'status':'prepared','fixture_version':1,'cases':{},'candidate_sha256':hashes(HERE/'skill/long-horizon'),
        'generator_sha256':hashes(HERE),'harness':'codex exec; configured model; fresh process without resume',
        'limitations':['one chain per arm/domain','six selected checkpoints per chain, not continuous real elapsed months','synthetic configuration runtime, not arbitrary code deployment','workspace read boundaries instructed, not full OS isolation']}
    for domain in DOMAINS:
        source=root/'sources'/domain
        source.mkdir(parents=True)
        shutil.copytree(PROJECT/'prototypes/agent-handoffs/results/first-handoffs/cases'/domain/'session-3/memory',source/'prior-work')
        noise(source/'archive',domain)
        for arm in ['baseline','skill']:
            ident=hashlib.sha256((domain+arm).encode()).hexdigest()[:16]
            trial=root/'trials'/ident
            trial.mkdir()
            for sub in ['memory','project','outbox']:
                (trial/sub).mkdir()
            shutil.copytree(source,trial/'history')
            (trial/'API.md').write_text(API)
            (trial/'task.md').write_text(TASK)
            (trial/'brief.md').write_text(f'''# Agreed responsibility

Domain: {domain}. Continue the same product responsibility represented by history/prior-work. It is ongoing and permits choosing useful objectives within that domain, implementing configuration changes, validating, deploying, running controlled evaluations, adopting supported improvements, and rolling back within this synthetic product. Those permissions persist across sessions. Historical work and source responsibilities remain historical; their authorization does not expand this brief.

Use commercial revenue with refunds and checkout errors for offer experiments. For product improvement, check activation and retained use separately. For exports, success requires all expected IDs and timely completion. For bugs, verify exposure and cause using current evidence and observe recovery. A completed sub-objective does not end the ongoing responsibility. For controlled outcomes use at least 14 fixture days after relevant exposure, together with adequate evidence; time alone proves nothing.

Limits: at most five active evaluations across the product. Four slots initially belong to related work. Before billed validation, consult the custom project-credit-ledger through usage. The shared allocation is 10 validation credits, with other responsibilities included and no automatic reset. The agent must respect this allocation; the service records usage but does not enforce the owner's budget. Other service operations are free. These are synthetic units, not model/API costs.

Read related work and actual revision before product changes. Coordinate material measurement interactions; compatible changes can proceed. Pause and notify if an owner-resolvable prerequisite prevents useful progress. Restoring access alone is not owner resumption. Terminate only when the responsibility has no useful work within its brief, with evidence and a notice.

Reports: monthly digest when the service reports it due, to fixture:owner. Immediate notice for pause, termination, or a needed owner decision. This brief explicitly authorizes delivery only to that synthetic inbox. Use the fixture scheduler for confirmed future runs; no live Impulse changes. Scope and accepted policy are identical in comparison arms.
''')
            shutil.copy2(HERE/'client.py',trial/'service-client.py')
            if arm=='skill':
                shutil.copytree(HERE/'skill/long-horizon',trial/'long-horizon')
            state=initial(domain)
            (root/'states'/f'{ident}.json').write_text(json.dumps(state,indent=2)+'\n')
            manifest['cases'][ident]={'domain':domain,'arm':arm,'path':str(trial),'epochs':[],
                'common_input_sha256':{k:v for k,v in hashes(trial).items() if not k.startswith('long-horizon/')},
                'history_bytes':sum(p.stat().st_size for p in (trial/'history').rglob('*') if p.is_file())}
    (root/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'root':str(root),'cases':{k:{'domain':v['domain'],'arm':v['arm']} for k,v in manifest['cases'].items()}},indent=2))


if __name__=='__main__':
    main()
