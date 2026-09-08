#!/usr/bin/env python3
"""THROWAWAY: four domains, scripted evidence, agreed responsibility lifecycle."""
import argparse
import json
import sys

from model import advance, initial
from scenarios import CASES


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--case', choices=CASES, default='weekly-product')
parser.add_argument('--walkthrough', action='store_true', help='Print every transition for the chosen case')
parser.add_argument('--compare', action='store_true', help='Print final states across all cases')
args = parser.parse_args()


def run_case(name):
    case = CASES[name]
    state = initial(case['brief'])
    for event in case['events']:
        state, _ = advance(state, event)
    return state


def frame(name, state, index, message, clear=False):
    if clear:
        print('\033[2J\033[H', end='')
    print('THROWAWAY: scripted scenarios; no agent or live service is running.')
    print(f'Case: {name} | Day: {state["day"]} | Status: {state["status"]}')
    print('Brief:', state['brief'])
    print('Current objective:', json.dumps(state['objective']))
    print('All objectives:', json.dumps(state['objectives']))
    print('Latest evidence:', state['evidence'])
    print('Reason:', state['reason'])
    print('Next:', state['next'])
    print('Terminal reason:', state['terminal_reason'])
    print('Retained history:')
    for record in state['history']:
        print(f'  Day {record["day"]}: {record["kind"]} | {record["evidence"]}')
    print(f'Consumed events: {index}/{len(CASES[name]["events"])} | {message}')


if args.compare:
    for name in CASES:
        state = run_case(name)
        print(json.dumps(dict(case=name, day=state['day'], status=state['status'],
            terminal_reason=state['terminal_reason'], objectives=state['objectives'],
            history_count=len(state['history']), evidence=state['evidence'], next=state['next'])))
elif args.walkthrough:
    state = initial(CASES[args.case]['brief'])
    for index, event in enumerate(CASES[args.case]['events'], 1):
        state, message = advance(state, event)
        frame(args.case, state, len(state['history']), message)
        print()
else:
    name = args.case
    state = initial(CASES[name]['brief'])
    index = 0
    message = 'Advance the fixture clock to inspect the next event.'
    while True:
        frame(name, state, index, message, clear=sys.stdout.isatty())
        print('\n[n] next event  [c] next case/reset')
        print('[f] serialize/reload memory  [r] reset  [q] quit (Enter after key)')
        try:
            key = input('> ').strip()
        except EOFError:
            break
        if key == 'q':
            break
        if key == 'n':
            if index >= len(CASES[name]['events']):
                message = 'End of supplied narrative; no further evidence exists in this fixture.'
            elif state['status'] == 'terminated':
                message = 'Task terminated; later fixture events are not consumed.'
            else:
                state, message = advance(state, CASES[name]['events'][index])
                index += 1
        elif key == 'f':
            state = json.loads(json.dumps(state))
            message = 'Reloaded explicit state through JSON; no actual agent session was launched.'
        elif key in ('c', 'r'):
            if key == 'c':
                names = list(CASES)
                name = names[(names.index(name) + 1) % len(names)]
            state = initial(CASES[name]['brief'])
            index = 0
            message = 'Reset this throwaway scenario.'
