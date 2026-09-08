#!/usr/bin/env python3
"""Small read-only terminal view of independently saved service state."""
import argparse
import json
from pathlib import Path
from grade import grade


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('root',type=Path)
    args=parser.parse_args()
    while True:
        manifest=json.loads((args.root/'manifest.json').read_text())
        print('\033[2J\033[H',end='')
        print('THROWAWAY — observed responsibility state\n')
        for ident,case in manifest['cases'].items():
            state=json.loads((args.root/'states'/f'{ident}.json').read_text())
            g=grade(state)
            print(f"{case['domain']:16} {case['arm']:8} sessions={len(case['epochs'])} day={state['day']:3} status={g['status']:10} deployments={g['actual_deployments']} violations={len(g['violations'])} next={state['scheduler']['next_day']}")
        print('\n[r/Enter] refresh  [q] quit')
        if input('> ').strip().lower()=='q':
            return


if __name__=='__main__':
    main()
