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


def credential_paths() -> list[Path]:
    paths = [Path.home() / '.codex/auth.json', Path.home() / '.claude/.credentials.json']
    runs = ROOT / 'evals/runs'
    for pattern in ('native-*/private-home/.codex/auth.json', 'native-*/private-home/.claude/.credentials.json',
                    'native-*/private-home/.gemini/antigravity-cli/antigravity-oauth-token'):
        paths.extend(runs.glob(pattern))
    return paths


def collect() -> set[bytes]:
    values: set[bytes] = set()
    for path in credential_paths():
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
        content = path.read_bytes()
        check(label, content)
        if path.name.endswith(('.tar.gz', '.tgz', '.tar')):
            with tarfile.open(path) as archive:
                for member in archive:
                    if member.isfile():
                        stream = archive.extractfile(member)
                        assert stream is not None
                        check(label + ':' + member.name, stream.read())
        elif path.suffix == '.gz':
            check(label + ':decompressed', gzip.decompress(content))
    return checked, hits


def retry_scan(root: Path, secrets: set[bytes], *, attempts: int = 60,
               retry_delay_seconds: float = 1.0) -> tuple[tuple[int, list[dict[str, str]]] | None, list[dict[str, str]]]:
    """Retain credentials while retrying incomplete concurrent archive writes.

    Production uses at most 60 full scans and 59 one-second pauses; scan time
    itself is additional. A failed scan is never interpreted as zero matches.
    """
    if attempts < 1 or retry_delay_seconds < 0:
        raise ValueError('attempts must be positive and retry delay nonnegative')
    errors: list[dict[str, str]] = []
    for attempt in range(attempts):
        secrets.update(collect())
        try:
            return scan(root, secrets), errors
        except (OSError, EOFError, tarfile.TarError) as error:
            errors.append({'at': utc_now(), 'exception_type': type(error).__name__})
            if attempt + 1 < attempts:
                time.sleep(retry_delay_seconds)
    return None, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--matrix', type=Path, required=True)
    parser.add_argument('--artifacts', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    started = utc_now()
    initial_auth_files = [str(path) for path in credential_paths() if path.is_file()]
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
    # Other evaluation batches may still be archiving traces under --artifacts.
    # Keep sampled credentials in memory and retry an incomplete scan; never
    # silently skip an unreadable archive or report it as a clean scan.
    result, scan_errors = retry_scan(args.artifacts, values)
    samples += len(scan_errors) + int(result is not None)
    if result is None:
        dump(args.output, {'started_at': started, 'finished_at': utc_now(),
                           'scan_complete': False, 'scan_errors': scan_errors,
                           'credential_value_count': len(values), 'samples': samples,
                           'observable_auth_files_at_start': initial_auth_files,
                           'values_persisted': False})
        print('Credential scan could not read all artifacts after 60 attempts; no clean result reported.')
        return 2
    checked, hits = result
    dump(args.output, {'started_at': started, 'finished_at': utc_now(), 'credential_value_count': len(values),
                       'samples': samples, 'artifact_streams_scanned': checked, 'matches': hits,
                       'observable_auth_files_at_start': initial_auth_files,
                       'scan_complete': True, 'scan_errors': scan_errors,
                       'scope': 'Exact credential values observed in installed auth files and owned temporary homes; raw files, decompressed gzip and tar members.',
                       'values_persisted': False})
    print(f'Credential scan checked {checked} streams; {len(hits)} matches. Values were never printed or persisted.')
    return int(bool(hits))


if __name__ == '__main__':
    raise SystemExit(main())
