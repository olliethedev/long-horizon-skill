#!/usr/bin/env python3
"""THROWAWAY terminal shell. No real agents, deployments, analytics, or scheduling."""
import argparse
import json
from pathlib import Path
import sys

from model import initial, next_action, transition


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--workspace', type=Path, help='Optional scratch persistence directory')
parser.add_argument('--steps', nargs='*', help='Run named actions and print each resulting state')
args = parser.parse_args()
checkpoint = None
if args.workspace:
    if args.workspace.name != 'PROTOTYPE-WIPE-ME':
        parser.error('Scratch directory must be named PROTOTYPE-WIPE-ME')
    args.workspace.mkdir(parents=True, exist_ok=True)
    checkpoint = args.workspace / 'state.json'
state = json.loads(checkpoint.read_text()) if checkpoint and checkpoint.exists() else initial()
session_note = 'Fresh session: reconstruct from saved records.'


def save():
    if checkpoint:
        temporary = checkpoint.with_suffix('.tmp')
        temporary.write_text(json.dumps(state, indent=2) + '\n')
        temporary.replace(checkpoint)


def frame(message, interactive=False):
    if interactive:
        print('\033[2J\033[H', end='')
    print('THROWAWAY continuity prototype — all evidence is synthetic')
    print(f'Day: {state["day"]} | Context: {state["context"]} | ' +
          f'Wake: {state["wake"]} | Acknowledged: {state["wake_acknowledged"]}')
    print('Attempts:')
    for item in state['attempts']:
        print(' ', json.dumps(item))
    print('Observations:')
    for item in state['observations']:
        print(' ', json.dumps(item))
    print('Learnings (historical conclusions retained):')
    for item in state['learnings']:
        scope = 'applicable' if item['context'] == state['context'] else 'needs revalidation'
        print(' ', json.dumps(item), scope)
    print('Session note:', session_note)
    print('Derived next action:', next_action(state))
    print('Last action:', message)
    if interactive:
        print('\n[t] try  [u] uncertain  [c] confirm  [a] schedule ack  [w] +week')
        print('[i] inconclusive  [+] win  [-] lose  [d] drift  [x] invalidate')
        print('[n] misleading note  [f] fresh session  [q] quit (Enter after key)')


def step(action):
    global state, session_note
    if action == 'note':
        session_note = 'Misleading summary: this variant is a universal winner. Deploy again.'
        message = 'Inserted a contradictory session note; it does not rewrite evidence.'
    elif action == 'fresh':
        if not checkpoint:
            message = 'No scratch persistence enabled. A real fresh process would lose this in-memory state.'
        else:
            state = json.loads(checkpoint.read_text())
            session_note = 'Fresh session: reconstruct from saved records.'
            message = 'Reloaded checkpoint; discarded session note.'
    elif action == 'show':
        message = 'Loaded current state.'
    else:
        state, message = transition(state, action)
    save()
    return message


save()
if args.steps is not None:
    for action in args.steps or ['show']:
        frame(step(action))
        print()
else:
    keys = dict(t='try', u='uncertain', c='confirm', a='ack', w='week',
                i='inconclusive', d='drift', x='invalidate', n='note', f='fresh')
    keys.update({'+': 'win', '-': 'lose'})
    message = 'Loaded current state.'
    while True:
        frame(message, interactive=sys.stdout.isatty())
        try:
            key = input('> ').strip()
        except EOFError:
            break
        if key == 'q':
            break
        message = step(keys.get(key, key))
