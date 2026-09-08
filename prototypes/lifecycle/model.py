"""THROWAWAY pure lifecycle model: follow the agreed responsibility lifecycle."""
from copy import deepcopy


def initial(brief):
    return dict(brief=brief, day=0, status='active', objective=None,
                objectives=[], history=[], reason='Ready to inspect the first signal.',
                evidence=None, next='Inspect signals and history.', terminal_reason=None)


def advance(previous, event):
    state = deepcopy(previous)
    if state['objective']:
        state['objective'] = state['objectives'][-1]
    if state['status'] == 'terminated':
        return state, 'Task terminated; later fixture events are not consumed.'
    state['day'] = event['day']
    state['evidence'] = event['evidence']
    state['reason'] = event.get('reason', event.get('objective', ''))
    state['history'].append(dict(day=event['day'], kind=event['kind'],
                                 evidence=event['evidence'], reason=state['reason']))
    kind = event['kind']
    if kind == 'select':
        if state['objective'] and state['objective']['status'] == 'active':
            state['objective']['status'] = 'superseded'
            state['objective']['reason'] = 'Changed approach; prior observations retained.'
        objective = dict(text=event['objective'], status='active')
        state['objectives'].append(objective)
        state['objective'] = objective
        state['status'] = 'active'
        state['next'] = 'Pursue the selected objective within the brief.'
    elif kind == 'wait':
        state['status'] = 'waiting'
        state['next'] = 'Arrange the next relevant observation.'
    elif kind == 'learn':
        state['status'] = 'active'
        state['next'] = 'Use this evidence to choose the next useful action.'
    elif kind in ('objective_reached', 'objective_impossible', 'responsibility_reached', 'responsibility_impossible'):
        if state['objective']:
            state['objective']['status'] = 'impossible' if kind.endswith('impossible') else 'reached'
            state['objective']['reason'] = event['reason']
        terminate = kind in ('responsibility_reached', 'responsibility_impossible')
        if terminate:
            state['status'] = 'terminated'
            state['terminal_reason'] = 'impossible' if kind.endswith('impossible') else 'reached'
            state['next'] = 'End future work and retain the workspace.'
        else:
            state['status'] = 'active'
            state['next'] = 'Review the broader brief and choose another useful objective or wait.'
    return state, state['reason']
