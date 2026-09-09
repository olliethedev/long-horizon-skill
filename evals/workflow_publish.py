#!/usr/bin/env python3
"""Archive finalized workflow evidence after provenance and credential gates; no model calls."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import tarfile
import zlib
from typing import Any

from native_credentials_check import collect
from recall import dump, hashes, utc_now
from workflow_runner import inventory

PATTERNS = {
    'private_key': rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
    'github_token': rb'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{50,})',
    'provider_key': rb'\bsk-(?:ant-|proj-)?[A-Za-z0-9_-]{40,}',
    'google_oauth': rb'\bya29\.[A-Za-z0-9_-]{30,}',
    'jwt': rb'\beyJ[A-Za-z0-9_-]{16,}\.[A-Za-z0-9_-]{16,}\.[A-Za-z0-9_-]{16,}',
    'aws_access_key': rb'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b',
}


def recover_gzip(raw: bytes) -> tuple[bytes, bool]:
    """Return only the decodable prefix; callers must retain and label damaged originals."""
    try:
        return gzip.decompress(raw), bool(raw)
    except (EOFError, zlib.error):
        decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
        chunks = []
        for value in raw:
            try:
                chunks.append(decoder.decompress(bytes([value])))
            except zlib.error:
                break
        return b''.join(chunks), False


def publication_scan(root: Path) -> dict[str, Any]:
    secrets = collect()
    exact_hits = []
    incomplete = []
    generic_hits = []
    generic_streams = 0
    for path in sorted(root.rglob('*')):
        if path.is_symlink():
            contents = [os.readlink(path).encode()]
        elif path.is_file():
            raw = path.read_bytes()
            contents = [raw]
            if path.suffix == '.gz':
                recovered, complete = recover_gzip(raw)
                contents.append(recovered)
                if not complete:
                    incomplete.append(str(path.relative_to(root)))
        else:
            continue
        for content in contents:
            generic_streams += 1
            for secret in secrets:
                if secret in content:
                    exact_hits.append({'artifact': str(path.relative_to(root)),
                                       'credential_sha256': hashlib.sha256(secret).hexdigest()})
            for name, pattern in PATTERNS.items():
                if re.search(pattern, content):
                    generic_hits.append({'artifact': str(path.relative_to(root)), 'pattern': name})
    result = {'at': utc_now(), 'complete': True, 'exact_streams': generic_streams, 'exact_matches': exact_hits,
              'generic_streams': generic_streams, 'generic_matches': generic_hits,
              'incomplete_compressed_streams': incomplete,
              'patterns': {k: v.decode() for k, v in PATTERNS.items()}, 'values_persisted': False,
              'limits': 'Publication exact scan covers currently available credential values and raw/decompressible artifact bytes. Original per-session sampled-value gates have their documented limits. A process-loss recovery cannot recover its lost historical credential sampler or uncaptured native output; truncated originals and salvaged bytes are both retained/scanned. Generic patterns are heuristic; absence of every possible secret or encoded credential is not proven.'}
    if exact_hits or generic_hits:
        raise ValueError('Publication scan found a candidate credential; inspect privately before archiving')
    return result


def archive(source: Path, output: Path) -> dict[str, Any]:
    manifest = json.loads((source / 'manifest.json').read_text())
    if not manifest.get('finished_at'):
        raise ValueError('Do not archive a running study')
    if hashes(source / 'sources') != manifest['source_hashes']:
        raise ValueError('Frozen evaluator source changed')
    for p in source.glob('trajectories/*/*/*/sessions/*/manifest.json'):
        session = json.loads(p.read_text())
        credential = session.get('credential_scan', {})
        if (not session.get('finished_at') or not credential.get('complete') or credential.get('matches')
                or not session.get('temporary_auth_home_removed')):
            raise ValueError('Session artifacts are not cleared for publication')
    before = inventory(source)
    scanned = publication_scan(source)
    excluded = {}
    for p in source.glob('trajectories/*/*/*/sessions/*/publication-exclusions.json'):
        record = json.loads(p.read_text())
        for name in record['files']:
            path = p.parent / name
            key = str(path.relative_to(source))
            excluded[key] = {'sha256': before[key], 'reason': record['reason']}
    def include(item: tarfile.TarInfo) -> tarfile.TarInfo | None:
        key = str(Path(item.name).relative_to(source.name))
        return None if '__pycache__/' in key or key in excluded else item
    target = output / f'{source.name}.tar.gz'
    with target.open('xb') as raw:
        with tarfile.open(fileobj=raw, mode='w:gz', dereference=False) as tar:
            tar.add(source, arcname=source.name, filter=include)
    if inventory(source) != before:
        raise ValueError('Source changed while archiving')
    # Verify every archived regular file or symlink against its original bytes.
    recovered = {}
    with tarfile.open(target) as tar:
        for member in tar:
            key = str(Path(member.name).relative_to(source.name))
            if member.issym():
                recovered[key] = 'symlink:' + member.linkname
            elif member.isfile():
                stream = tar.extractfile(member)
                assert stream is not None
                recovered[key] = hashlib.sha256(stream.read()).hexdigest()
    expected = {k: v for k, v in before.items() if '__pycache__/' not in k and k not in excluded}
    if recovered != expected:
        raise ValueError('Archive content differs from original evidence')
    return {'name': target.name, 'sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
            'bytes': target.stat().st_size, 'live': manifest['live'], 'manifest_sha256': before['manifest.json'],
            'artifact_hashes': expected, 'withheld_local_originals': excluded, 'publication_scan': scanned}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('sources', nargs='+', type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    rows = [archive(source.resolve(), args.output) for source in args.sources]
    postprocessing = args.output / 'postprocessing-sources'
    postprocessing.mkdir(exist_ok=True)
    for name in ('workflow_publish.py', 'workflow_summary.py', 'native_credentials_check.py',
                 'native_report.py', 'native_diagnostics.py', 'recall.py', 'workflow_runner.py'):
        shutil.copyfile(Path(__file__).parent / name, postprocessing / name)
    dump(args.output / 'index.json', {'created_at': utc_now(), 'archives': rows,
         'postprocessing_source_hashes': hashes(postprocessing),
         'extraction': 'Archives retain original paths and source citations beneath their named roots; no agent files are executed during publication.'})
    print(json.dumps({'archives': [{k: row[k] for k in ('name', 'bytes', 'sha256')} for row in rows]}))


if __name__ == '__main__':
    main()
