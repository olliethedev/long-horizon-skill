"""THROWAWAY: can explicit attempts/evidence reconstruct the next useful action?"""
from copy import deepcopy


def initial():
    return dict(day=0, context=1, attempts=[], observations=[], learnings=[],
                wake=None, wake_acknowledged=False)


def active(state):
    return next((a for a in reversed(state['attempts'])
                 if a['status'] in ('intent', 'uncertain', 'observing')), None)


def transition(previous, action):
    """Pure reducer. Evidence verdicts are supplied fixtures, not statistics."""
    state = deepcopy(previous)
    attempt = active(state)
    message = 'No transition.'
    if action == 'try':
        old = [a for a in state['attempts'] if a['context'] == state['context']]
        if attempt:
            message = 'Resolve the existing attempt before proposing another.'
        elif any(a['status'] == 'lost' for a in old):
            message = 'This exact variant already lost in these conditions; propose a different idea.'
        elif any(a['status'] == 'won' for a in old):
            message = 'This variant already won here; repeating it adds no new question.'
        else:
            state['attempts'].append(dict(id=f'a{len(state["attempts"])+1}',
                variant='short-copy', context=state['context'], status='intent',
                rationale='Shorter copy might improve conversion.', receipt=None))
            state['wake'] = None
            state['wake_acknowledged'] = False
            message = 'Recorded intent. Deployment has not been established.'
    elif action == 'uncertain' and attempt and attempt['status'] == 'intent':
        attempt['status'] = 'uncertain'
        message = 'Simulated missing deployment acknowledgment. Do not infer failure.'
    elif action == 'confirm' and attempt and attempt['status'] in ('intent', 'uncertain'):
        attempt['status'] = 'observing'
        attempt['receipt'] = f'fixture-deployment-{attempt["id"]}'
        state['wake'] = state['day'] + 7
        state['wake_acknowledged'] = False
        message = 'Fixture confirms this deployment. Proposed a review in seven days.'
    elif action == 'ack' and state['wake'] is not None:
        state['wake_acknowledged'] = True
        message = 'Simulated successful scheduler acknowledgment; next wake is recorded.'
    elif action == 'week':
        state['day'] += 7
        message = 'Advanced observation clock; elapsed time alone supplies no evidence.'
    elif action in ('inconclusive', 'win', 'lose') and attempt and attempt['status'] == 'observing':
        if attempt['context'] != state['context']:
            message = 'Conditions changed. Close the invalidated attempt before interpreting new results.'
        elif state['day'] < (state['wake'] or 0):
            message = 'The planned observation window has not ended.'
        else:
            evidence_id = f'e{len(state["observations"])+1}'
            state['observations'].append(dict(id=evidence_id, attempt=attempt['id'],
                day=state['day'], context=state['context'], verdict=action))
            if action == 'inconclusive':
                state['wake'] = state['day'] + 7
                state['wake_acknowledged'] = False
                message = 'Insufficient evidence. Keep the attempt open and propose another observation.'
            else:
                attempt['status'] = 'won' if action == 'win' else 'lost'
                state['learnings'].append(dict(attempt=attempt['id'], evidence=evidence_id,
                    context=state['context'], conclusion=attempt['status']))
                state['wake'] = None
                state['wake_acknowledged'] = False
                message = 'Recorded a scoped conclusion. Goal completion and rollout remain undecided.'
    elif action == 'drift':
        state['context'] += 1
        message = 'Simulated a material audience/product change; older conclusions remain historical.'
    elif action == 'invalidate' and attempt and attempt['context'] != state['context']:
        if attempt['status'] in ('intent', 'uncertain'):
            message = 'First reconcile whether the external action occurred; drift does not resolve uncertainty.'
        else:
            attempt['status'] = 'invalidated'
            state['wake'] = None
            state['wake_acknowledged'] = False
            message = 'Closed a confounded attempt without recording a win or loss.'
    return state, message


def next_action(state):
    attempt = active(state)
    if not attempt:
        return 'Review scoped learnings and choose the next question; the goal is not automatically complete.'
    if attempt['status'] in ('intent', 'uncertain'):
        return f'Reconcile deployment for {attempt["id"]} before repeating any external action.'
    if attempt['context'] != state['context']:
        return 'Record that conditions invalidated the current comparison.'
    if not state['wake_acknowledged']:
        return f'Confirm scheduling for day {state["wake"]}; a local plan is not a scheduler receipt.'
    if state['day'] < state['wake']:
        return f'Wait until day {state["wake"]}.'
    return 'Gather evidence about this attempt; do not choose a winner from elapsed time.'
