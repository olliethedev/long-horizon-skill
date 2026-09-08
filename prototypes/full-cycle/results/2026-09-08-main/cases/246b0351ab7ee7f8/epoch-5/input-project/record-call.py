"""Call only the supplied trial client and retain request/response evidence."""
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent.parent
label, operation = sys.argv[1:3]
argument = sys.argv[3] if len(sys.argv) > 3 else '{}'
args = json.loads((root / argument[1:]).read_text() if argument.startswith('@') else argument)
record = {'operation': operation, 'args': args, 'state': 'attempting'}
target = root / 'memory' / 'evidence' / (label + '.json')
target.parent.mkdir(parents=True, exist_ok=True)
if target.exists():
    raise SystemExit('Evidence label already exists; inspect saved evidence before another call.')
target.write_text(json.dumps(record, indent=2) + '\n')
result = subprocess.run(
    [sys.executable, str(root / 'service-client.py'), operation, json.dumps(args)],
    cwd=root, text=True, capture_output=True,
)
record.update(state='returned', returncode=result.returncode)
try:
    record['response'] = json.loads(result.stdout)
except json.JSONDecodeError:
    record['stdout'] = result.stdout
if result.stderr:
    record['stderr'] = result.stderr
target.write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
sys.exit(result.returncode)
