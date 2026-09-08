"""THROWAWAY: which past facts remain reachable through three memory views?"""
from collections import defaultdict


def history(weeks=104):
    """Synthetic weekly observations plus an attempt and its later correction."""
    records = []
    for week in range(1, weeks + 1):
        for subject in range(24):
            records.append(dict(id=f'w{week:03}-s{subject:02}', week=week,
                subject=f'subject-{subject:02}', kind='observation', attempt=None,
                text=f'Routine observation of subject {subject:02} in week {week}.'))
    important = [
        dict(id='a17-launch', week=3, kind='deployed', attempt='a17',
             text='Nimbus trial: shorter checkout copy deployed for mobile visitors.'),
        dict(id='a17-outcome', week=4, kind='outcome', attempt='a17',
             text='Clicks rose 16%; observed revenue fell 8%. Initial analysis rejected the variant.'),
        dict(id='a17-rollback', week=5, kind='rolled_back', attempt='a17',
             text='Rollback receipt verified. The control copy is restored.'),
        dict(id='a17-correction', week=17, kind='correction', attempt='a17',
             text='Reanalysis: loss supported for mobile; desktop evidence was inconclusive.'),
        dict(id='a63-proposal', week=70, kind='recommended', attempt='a63',
             text='Proposed Compact Purchase Panel for a new audience; no deployment receipt exists.'),
    ]
    for record in important:
        if record['week'] <= weeks:
            records.append(dict(subject='subject-00', **record))
    return sorted(records, key=lambda item: item['week'])


def views(records):
    current = {}
    by_subject = defaultdict(list)
    by_id = {}
    for record in records:
        current[record['subject']] = record
        by_subject[record['subject']].append(record['id'])
        by_id[record['id']] = record
    previous_week = max(record['week'] for record in records)
    previous_report = [record for record in records if record['week'] == previous_week]
    return dict(current=current, previous_report=previous_report,
                index=dict(by_subject), archive=by_id)


def retrieve(memory, mode, subject='subject-00'):
    if mode == 'current':
        return [memory['current'][subject]]
    if mode == 'previous-week':
        return [record for record in memory['previous_report'] if record['subject'] == subject]
    return [memory['archive'][record_id] for record_id in memory['index'][subject]]


def inspect(records, mode):
    memory = views(records)
    retrieved = retrieve(memory, mode)
    attempted = [record for record in retrieved if record['attempt']]
    return dict(total_records=len(records), returned_records=len(retrieved),
                historical_action_records=attempted,
                referenced_record_ids=[record['id'] for record in attempted])
