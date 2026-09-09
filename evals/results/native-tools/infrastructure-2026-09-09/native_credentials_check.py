#!/usr/bin/env python3
"""Watch owned native sessions, then scan archived evidence for exact credentials.

Credential values remain only in this process's memory, are never printed, and
are discarded on exit. The scanner performs no model calls or configuration
writes. Run while the matrix is active so refreshed temporary values are seen.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path
import tarfile
import time
from typing import Any

from recall import dump, utc_now

ROOT = Path(__file__).resolve().parents[1]


def extract(value: Any) -> set[bytes]:
    found: set[bytes] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = str(key).lower().replace('_', '')
            if isinstance(child, str) and len(child) > 20 and any(word in normalized for word in ('token', 'secret', 'apikey')):
                found.add(child.encode())
            found.update(extract(child))
    elif isinstance(value, list):
        for child in value:
            found.update(extract(child))
    return found


def collect() -> set[bytes]:
    paths = [Path.home() / '.codex/auth.json', Path.home() / '.claude/.credentials.json']
    runs = ROOT / 'evals/runs'
    for pattern in ('native-*/private-home/.codex/auth.json', 'native-*/private-home/.claude/.credentials.json',
                    'native-*/private-home/.gemini/antigravity-cli/antigravity-oauth-token'):
        paths.extend(runs.glob(pattern))
    values: set[bytes] = set()
    for path in paths:
        try:
            values.update(extract(json.loads(path.read_bytes())))
        except (OSError, ValueError):
            pass
    return values


def scan(root: Path, secrets: set[bytes]) -> tuple[int, list[dict[str, str]]]:
    checked = 0
    hits: list[dict[str, str]] = []
    def check(label: str, content: bytes) -> None:
        nonlocal checked
        checked += 1
        for secret in secrets:
            if secret in content:
                hits.append({'artifact': label, 'credential_sha256': hashlib.sha256(secret).hexdigest()})
    for path in sorted(root.rglob('*')):
        if not path.is_file() or path.is_symlink():
            continue
        label = str(path.relative_to(root))
        check(label, path.read_bytes())
        if path.name.endswith(('.tar.gz', '.tgz', '.tar')):
            with tarfile.open(path) as archive:
                for member in archive:
                    if member.isfile():
                        stream = archive.extractfile(member)
                        assert stream is not None
                        check(label + ':' + member.name, stream.read())
        elif path.suffix == '.gz':
            check(label + ':decompressed', gzip.decompress(path.read_bytes()))
    return checked, hits


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--matrix', type=Path, required=True)
    parser.add_argument('--artifacts', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    started = utc_now()
    values: set[bytes] = set()
    samples = 0
    while True:
        values.update(collect())
        samples += 1
        try:
            manifest = json.loads((args.matrix / 'manifest.json').read_text())
        except (OSError, ValueError):
            manifest = {}
        if 'finished_at' in manifest:
            break
        time.sleep(1)
    checked, hits = scan(args.artifacts, values)
    dump(args.output, {'started_at': started, 'finished_at': utc_now(), 'credential_value_count': len(values),
                       'samples': samples, 'artifact_streams_scanned': checked, 'matches': hits,
                       'scope': 'Exact credential values observed in installed auth files and owned temporary homes; raw files, decompressed gzip and tar members.',
                       'values_persisted': False})
    print(f'Credential scan checked {checked} streams; {len(hits)} matches. Values were never printed or persisted.')
    return int(bool(hits))


if __name__ == '__main__':
    raise SystemExit(main())
