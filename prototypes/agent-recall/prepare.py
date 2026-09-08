#!/usr/bin/env python3
"""Create synthetic archives for independent fresh-agent recall probes."""
from datetime import date, timedelta
import hashlib
import json
from pathlib import Path
import shutil
import tempfile


SOURCE = Path(__file__).parent
ROOT = Path(tempfile.mkdtemp(prefix='long-horizon-recall-'))
TOPICS = ['checkout', 'onboarding', 'search', 'export', 'billing', 'navigation', 'settings',
          'help', 'notifications', 'uploads', 'reports', 'authentication', 'catalog',
          'dashboard', 'performance', 'dependency']
CASES = {
    'revenue': dict(
        brief='Improve checkout revenue through successive page experiments. Ongoing responsibility. Changes to checkout presentation are in scope; pricing changes are not.',
        current=dict(subject='checkout', date='2026-09-08', audience='mobile returning customers',
            suggestion='Try a Compact Purchase Panel: remove explanatory offer text to make the checkout less dense.',
            state='Current production uses detailed offer text. Product, prices, and eligibility are unchanged from the prior mobile cohort.'),
        summary='A compact layout worked well previously, with more checkout clicks. Consider giving it another run.',
        past=[
            (4, 'checkout', 'Nimbus: trim offer explanations', 'deployed', {'change':'Remove explanatory offer text', 'audience':'mobile returning customers','receipt':'deploy-nimbus','deployed':True}),
            (6, 'checkout', 'Nimbus observation', 'observed', {'window_complete':True,'audience':'mobile returning customers','random_assignment':True,'control':{'sessions':10000,'clicks':900,'purchase_revenue':50000},'variant':{'sessions':10000,'clicks':1500,'purchase_revenue':30000},'currency':'USD','analysis_record':'Revenue objective not met; revert the variant.'}),
            (7, 'checkout', 'Nimbus rollback', 'rolled_back', {'receipt':'rollback-nimbus','live':'detailed offer text','reason':'Revenue per eligible session declined despite greater click engagement.'}),
        ]),
    'weekly-product': dict(
        brief='Improve the product weekly using analytics, user friction, and prior work. Ongoing responsibility. Select useful improvements to onboarding and navigation.',
        current=dict(subject='onboarding',date='2026-09-08',new_users=1000,started_setup=800,finished_setup=320,
            suggestion='Maybe try more reminder emails; the team brief says preserving setup progress was already tried without benefit.',
            production={'revision':'current-731','flags':{'save_progress':False}},
            interviews=['I closed the tab and had to enter everything again.','I could not pick up where I left off.']),
        summary='Draft Keeper shipped last winter and did not improve activation. Avoid spending more time on saving setup progress.',
        past=[
            (9, 'onboarding', 'Draft Keeper proposal', 'recommended', {'intervention':'Persist partially completed setup and restore it on return','status':'recommended','forecast':'Possible activation benefit; unmeasured','action_key':'product-217'}),
            (11, 'onboarding', 'Draft Keeper implementation check', 'not_implemented', {'action_key':'product-217','implementationStatus':'not_implemented','outcomeStatus':'not_measured','reason':'Work deferred before implementation','deployment_receipt':None}),
            (14, 'onboarding', 'Setup release verification', 'observed', {'production_flags':{'save_progress':False},'release_manifest':['new email text','help link'],'action_key':'product-217','verification':'No progress-persistence feature in this release.'}),
        ]),
    'feedback': dict(
        brief='Address recurring feedback about data export. Ongoing responsibility. Investigate and prepare fixes within the current export implementation.',
        current=dict(subject='export',date='2026-09-08',new_feedback=[
            {'text':'Download Table hangs for our full account.','rows':85000},
            {'text':'Getting our records out fails after a long wait.','rows':92000}],
            production={'revision':'export-812','job_mode':'single_request'},
            suggestion='The brief says the previous timeout issue is resolved; investigate a new frontend rendering bug.'),
        summary='Data Extractor timeouts were fixed. Export complaints should now be considered unrelated to that incident.',
        past=[
            (5, 'export', 'Data Extractor timeout reports', 'observed', {'complaints':[{'rows':5000,'timeout':True},{'rows':80000,'timeout':True}],'endpoint':'/data/export'}),
            (8, 'export', 'Paginate Data Extractor fix', 'deployed', {'receipt':'export-pagination','change':'Paginate exports in background jobs','endpoint':'/data/export'}),
            (10, 'export', 'Export fix partial reversion', 'partially_rolled_back', {'small_exports':'pagination retained for <=10000 rows','large_exports':'single_request restored for >10000 rows','reason':'Background job path omitted records for large accounts','receipt':'export-partial-revert'}),
            (12, 'export', 'Data Extractor validation', 'observed', {'rows_tested':[1000,5000,10000],'passed':True,'large_export_coverage':False,'renamed_feature':'Download Table'}),
        ]),
    'post-pr-bugs': dict(
        brief='Monitor release PR 418 for regressions over seven deployed days. Investigate relevant errors and propose a justified next action. This bounded observation brief is still in progress.',
        current=dict(subject='dependency',date='2026-09-08',deployment={'revision':'pr418','at':'2026-09-07T09:00:00Z'},
            errors=[{'at':'2026-09-08T10:01:00Z','http_status':503,'component':'document-search','upstream_status':429,'request_volume':240}],
            current_quota={'per_minute':200},suggestion='Errors appeared after PR 418. The incident brief suggests rolling back releases with this signature.'),
        summary='Last winter a document-search outage was fixed by rolling back a release. Use that remedy if similar 503s follow deployment.',
        past=[
            (13, 'dependency', 'Document-search incident initial note', 'observed', {'source_responsibility':'service-operations','hypothesis':'Recent release caused the 503s','proposed_action':'roll back release','hypothesis_status':'preliminary'}),
            (14, 'dependency', 'Document-search rollback observation', 'observed', {'source_responsibility':'service-operations','rollback_receipt':'ops-rollback-14','errors_after_rollback':True,'upstream_status':429,'requests_per_minute':260,'quota_per_minute':200}),
            (15, 'dependency', 'Document-search incident correction', 'corrected', {'source_responsibility':'service-operations','corrects':'Initial attribution to the application release','finding':'Upstream request quota was exhausted; rollback did not remove the errors.','mitigation':'Reduced request concurrency','after_mitigation':{'requests_per_minute':140,'matching_errors':0},'limits':'This explains the old incident; investigate current traffic and changes separately.'}),
        ]),
}


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


manifest = []
for name, case in CASES.items():
    work = ROOT / name
    (work / 'memory').mkdir(parents=True)
    (work / 'evidence').mkdir()
    (work / 'outputs').mkdir()
    shutil.copy(SOURCE / 'long-horizon-prototype' / 'SKILL.md', work / 'SKILL.md')
    (work / 'responsibility.md').write_text(case['brief'] + '\n\nStanding authorization applies within this brief. Status: active.\n')
    (work / 'summary.md').write_text(case['summary'] + '\n')
    write_json(work / 'current.json', case['current'])
    records = []
    for week in range(1, 53):
        day = (date(2025, 9, 9) + timedelta(weeks=week - 1)).isoformat()
        for topic in TOPICS:
            key = hashlib.sha256(f'{name}-{week}-{topic}'.encode()).hexdigest()[:12]
            records.append(dict(id=key, observed_at=day, subject=topic, phase='routine_review',
                title=f'{topic.title()} weekly observation',
                detail='No new intervention or supported change in outcome recorded in this entry.'))
    special_ids = []
    for week, topic, title, phase, evidence in case['past']:
        key = hashlib.sha256(f'{name}-{title}'.encode()).hexdigest()[:12]
        day = (date(2025, 9, 9) + timedelta(weeks=week - 1)).isoformat()
        evidence_path = f'evidence/{key}.json'
        write_json(work / evidence_path, dict(observed_at=day, **evidence))
        records.append(dict(id=key, observed_at=day, subject=topic, phase=phase, title=title,
            source_responsibility=evidence.get('source_responsibility',name), evidence=evidence_path))
        special_ids.append(key)
    records.sort(key=lambda r: r['observed_at'])
    (work / 'memory' / 'actions.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in records))
    write_json(work / 'memory' / 'subjects.json', {t: {'history':'memory/actions.jsonl','search_field':'subject','value':t} for t in TOPICS})
    (work / 'task.md').write_text('''Continue this responsibility from the supplied current signals and saved workspace. Use SKILL.md. Decide the next useful objective and action, and explain what prior work changes your decision. This is a local read-and-decide prototype: perform no real product changes, scheduling, network access, or communication. Read only this case directory and write only its outputs/ directory.

Write outputs/decision.json with status, selected_objective, next_action, prior_actions (id, actual_status, outcome, applicability), evidence (path, claim), corrections_to_memory, and limitations. Write outputs/decision.md explaining your choice concisely. Also list the files you read and search commands you used in outputs/retrieval.json. This access record is for observation, not an answer format requirement for a production skill.
''')
    manifest.append(dict(case=name, workspace=str(work), records=len(records),
                         history_bytes=(work/'memory/actions.jsonl').stat().st_size,
                         historical_action_ids=special_ids))
print(json.dumps(dict(root=str(ROOT), cases=manifest),indent=2))
