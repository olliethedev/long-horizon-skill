"""Supplement exact observed-value scans with generic patterns; never persist matches."""
import gzip
import hashlib
import io
import json
import re
import tarfile
from datetime import datetime, timezone
from pathlib import Path

root = Path('evals/results')
output = root / 'native-tools/credential-pattern-scan-resumed-2026-09-09.json'
patterns = {
    'private_key': rb'-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----',
    'provider_key': rb'\bsk-(?:proj-|ant-|svcacct-)?[A-Za-z0-9_-]{32,}',
    'github_token': rb'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})',
    'google_access_token': rb'\bya29\.[A-Za-z0-9_-]{30,}',
    'refresh_token_value': rb'"refresh_token"\s*:\s*"[^"\s]{30,}"',
    'jwt': rb'\beyJ[A-Za-z0-9_-]{20,}\.eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}',
}
compiled = {key: re.compile(value) for key, value in patterns.items()}
count = 0
hits = []

def check(label, content):
    global count
    count += 1
    for name, pattern in compiled.items():
        for match in pattern.finditer(content):
            hits.append({'artifact': label, 'pattern': name,
                         'match_sha256': hashlib.sha256(match.group()).hexdigest()})

for path in sorted(root.rglob('*')):
    if not path.is_file() or path.is_symlink() or path == output:
        continue
    content = path.read_bytes()
    label = str(path.relative_to(root))
    check(label, content)
    if path.name.endswith(('.tar.gz', '.tgz', '.tar')):
        with tarfile.open(fileobj=io.BytesIO(content)) as archive:
            for member in archive:
                if member.isfile():
                    stream = archive.extractfile(member)
                    assert stream is not None
                    check(label + ':' + member.name, stream.read())
    elif path.suffix == '.gz':
        check(label + ':decompressed', gzip.decompress(content))
output.write_text(json.dumps({
    'scanned_at': datetime.now(timezone.utc).isoformat(),
    'artifact_streams_scanned': count,
    'pattern_names': list(patterns),
    'matches': hits,
    'scan_complete': True,
    'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'scope': 'Generic credential patterns in raw results, decompressed gzip and tar members. Exact observed-value scans are separate; matched values are never printed or persisted. This cannot establish coverage of every possible credential format.'
}, indent=2) + '\n')
print(f'Generic pattern scan completed: {count} streams, {len(hits)} matches. No values printed.')
raise SystemExit(bool(hits))
