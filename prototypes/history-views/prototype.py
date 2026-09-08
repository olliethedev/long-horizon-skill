#!/usr/bin/env python3
"""THROWAWAY memory views: synthetic history, no agent or real task access."""
import argparse
import json
import sys

from model import history, inspect


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--weeks', type=int, choices=[26, 52, 104], default=104)
parser.add_argument('--compare', action='store_true')
args = parser.parse_args()
weeks = args.weeks
mode = 'current'


def frame(mode, weeks, clear=False):
    result = inspect(history(weeks), mode)
    if clear:
        print('\033[2J\033[H', end='')
    print('THROWAWAY history views — data access only; no LLM recall has been tested.')
    print(f'History: {weeks} weeks | Total records: {result["total_records"]} | View: {mode}')
    print('Subject: subject-00 (supplied lookup key, not inferred from a natural-language query)')
    print(f'Returned records: {result["returned_records"]}')
    print('Historical action records reachable through this view:')
    for record in result['historical_action_records']:
        print(f'  {record["id"]}, week {record["week"]}, {record["kind"]}: {record["text"]}')
    if not result['historical_action_records']:
        print('  None; this view supplies only current routine observations.')
    print('Record references:', ', '.join(result['referenced_record_ids']) or 'none')
    print('Routine observations are counted above; the listed records expose the retained attempt history.')


if args.compare:
    for weeks in (26, 52, 104):
        for mode in ('current', 'previous-week', 'indexed-archive'):
            print(json.dumps(dict(weeks=weeks, mode=mode, **inspect(history(weeks), mode))))
else:
    while True:
        frame(mode, weeks, clear=sys.stdout.isatty())
        print('\n[c] current row  [p] previous week  [i] indexed archive  [t] change horizon  [q] quit')
        try:
            key = input('> ').strip()
        except EOFError:
            break
        if key == 'q':
            break
        mode = {'c': 'current', 'p': 'previous-week', 'i': 'indexed-archive'}.get(key, mode)
        if key == 't':
            horizons = [26, 52, 104]
            weeks = horizons[(horizons.index(weeks) + 1) % len(horizons)]
