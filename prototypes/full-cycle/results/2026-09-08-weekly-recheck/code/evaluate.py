#!/usr/bin/env python3
"""One-command entrypoint for a new complete simulation matrix."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import time


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--agents',action='store_true',help='Run 48 fresh configured Codex sessions; consumes model allowance.')
    a=p.parse_args()
    here=Path(__file__).resolve().parent
    subprocess.run([sys.executable,str(here/'calibrate.py')],check=True)
    setup=json.loads(subprocess.check_output([sys.executable,str(here/'prepare.py')],text=True))
    root=Path(setup['root'])
    print(json.dumps(setup,indent=2),flush=True)
    if not a.agents:
        print('Prepared only. Use --agents for the model evaluation, or inspect.py ROOT for the read-only state view.')
        return
    server=subprocess.Popen([sys.executable,str(here/'service.py'),str(root)])
    try:
        deadline=time.monotonic()+10
        while not (root/'endpoint.json').exists():
            if time.monotonic()>deadline or server.poll() is not None:
                raise RuntimeError('Fixture service did not start')
            time.sleep(.05)
        subprocess.run([sys.executable,str(here/'run.py'),str(root)],check=True)
        subprocess.run([sys.executable,str(here/'grade.py'),str(root)],check=True)
    finally:
        server.terminate();server.wait()


if __name__=='__main__':
    main()
