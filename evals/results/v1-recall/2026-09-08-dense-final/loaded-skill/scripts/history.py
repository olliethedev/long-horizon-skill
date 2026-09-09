#!/usr/bin/env python3
"""Bounded, read-only navigation of a product's UTF-8 history."""
import argparse
import base64
from contextlib import contextmanager
import codecs
import hashlib
import json
import os
from pathlib import Path
import sys
import stat
from typing import Any, BinaryIO, Iterator

EXTENSIONS = {'.md', '.txt', '.json', '.jsonl', '.csv', '.yaml', '.yml', '.toml'}
OUTPUT_BYTES = 20000
LINE_BYTES = 65536
DIRECTORY_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
EXCLUDED = {'.git', '.venv', '__pycache__', '.mypy_cache'}


def encoded(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'))


def inventory(root_fd: int) -> tuple[list[tuple[str, int, int]], dict[str, int]]:
    def fail_walk(error: OSError) -> None:
        raise error

    files = []
    skipped = {'symlinks': 0, 'unsupported_files': 0, 'excluded_directories': 0}
    for directory, dirs, names, fd in os.fwalk('.', dir_fd=root_fd, follow_symlinks=False, onerror=fail_walk):
        for name in dirs[:]:
            if stat.S_ISLNK(os.stat(name, dir_fd=fd, follow_symlinks=False).st_mode):
                dirs.remove(name)
                skipped['symlinks'] += 1
            elif name in EXCLUDED:
                dirs.remove(name)
                skipped['excluded_directories'] += 1
        for name in names:
            info = os.stat(name, dir_fd=fd, follow_symlinks=False)
            if stat.S_ISLNK(info.st_mode):
                skipped['symlinks'] += 1
            elif not stat.S_ISREG(info.st_mode) or Path(name).suffix.lower() not in EXTENSIONS:
                skipped['unsupported_files'] += 1
            else:
                files.append((str(Path(directory) / name), info.st_size, info.st_mtime_ns))
    return sorted(files), skipped


@contextmanager
def open_source(root_fd: int, relative: str) -> Iterator[BinaryIO]:
    path = Path(relative)
    if path.is_absolute() or '..' in path.parts or not path.parts:
        raise ValueError('Source must be a relative file inside the product directory.')
    fd = os.dup(root_fd)
    try:
        for part in path.parts[:-1]:
            child = os.open(part, DIRECTORY_FLAGS, dir_fd=fd)
            os.close(fd)
            fd = child
        source_fd = os.open(path.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
        with os.fdopen(source_fd, 'rb') as source:
            if not stat.S_ISREG(os.fstat(source.fileno()).st_mode):
                raise ValueError('Source must be a regular file.')
            yield source
    finally:
        os.close(fd)


def search(root: Path, root_fd: int, terms: list[str], limit: int, cursor: str | None) -> dict[str, Any]:
    files, skipped = inventory(root_fd)
    version = hashlib.sha256(encoded(files).encode()).hexdigest()
    start = ('', 0)
    scope = str(root.absolute())
    if cursor:
        saved = json.loads(base64.urlsafe_b64decode(cursor))
        if saved['version'] != version or saved['scope'] != scope or saved['terms'] != terms:
            raise ValueError('History or query changed; restart the search.')
        start = (saved['path'], saved['line'])
    matches: list[dict[str, Any]] = []
    skipped['long_lines'] = 0
    skipped_examples: list[dict[str, Any]] = []
    next_cursor = None
    for relative, _, _ in files:
        with open_source(root_fd, relative) as source:
            number = 0
            while True:
                offset = source.tell()
                raw = source.readline(LINE_BYTES + 1)
                if not raw:
                    break
                number += 1
                if len(raw) > LINE_BYTES:
                    skipped['long_lines'] += 1
                    if len(skipped_examples) < 3:
                        skipped_examples.append({'path': relative, 'line': number, 'offset': offset})
                    while raw and not raw.endswith(b'\n'):
                        raw = source.readline(LINE_BYTES + 1)
                    continue
                line = raw.decode('utf-8', errors='replace')
                if (relative, number) <= start or not any(t.casefold() in line.casefold() for t in terms):
                    continue
                if len(matches) == limit:
                    previous = matches[-1]
                    next_cursor = base64.urlsafe_b64encode(encoded({'scope': scope, 'version': version,
                        'terms': terms, 'path': previous['path'], 'line': previous['line']}).encode()).decode()
                    break
                folded_position = min(line.casefold().find(t.casefold()) for t in terms if t.casefold() in line.casefold())
                position, folded_offset = 0, 0
                while folded_offset < folded_position:
                    folded_offset += len(line[position].casefold())
                    position += 1
                snippet = line.rstrip()[max(0, position - 100):max(0, position - 100) + 500]
                matches.append({'path': relative, 'line': number, 'offset': offset, 'text': snippet})
        if next_cursor:
            break
    return {'matches': matches, 'next_cursor': next_cursor, 'version': version,
            'skipped': skipped, 'skipped_examples': skipped_examples,
            'coverage': 'literal phrases in supported text files; aliases require additional queries'}


def read(root_fd: int, path: str, offset: int, size: int, version: str | None) -> dict[str, Any]:
    with open_source(root_fd, path) as source:
        before = os.fstat(source.fileno())
        hasher = hashlib.sha256()
        for chunk in iter(lambda: source.read(65536), b''):
            hasher.update(chunk)
        digest = hasher.hexdigest()
        if version is not None and version != digest:
            raise ValueError('Source changed; restart reading this file.')
        if not 0 <= offset <= before.st_size:
            raise ValueError('Offset is outside the source file.')
        source.seek(offset)
        data = source.read(size)
        decoder = codecs.getincrementaldecoder('utf-8')(errors='replace')
        text = decoder.decode(data, final=offset + len(data) == before.st_size)
        consumed = len(data) - len(decoder.getstate()[0])
        after = os.fstat(source.fileno())
        if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
            raise ValueError('Source changed while reading; restart.')
        return {'path': path, 'version': digest, 'offset': offset, 'text': text,
                'next_offset': offset + consumed if offset + consumed < before.st_size else None}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    query = sub.add_parser('search')
    query.add_argument('root', type=Path)
    query.add_argument('terms', nargs='+')
    query.add_argument('--limit', type=int, default=8, choices=range(1, 21))
    query.add_argument('--cursor')
    page = sub.add_parser('read')
    page.add_argument('root', type=Path)
    page.add_argument('path')
    page.add_argument('--offset', type=int, default=0)
    page.add_argument('--bytes', type=int, default=6000)
    page.add_argument('--version')
    args = parser.parse_args()
    try:
        if not args.root.is_dir():
            raise ValueError('Provide an existing product directory.')
        fd = os.open(args.root, DIRECTORY_FLAGS)
        try:
            if args.command == 'search':
                if any(not t.strip() for t in args.terms):
                    raise ValueError('Provide nonempty literal phrases.')
                result = search(args.root, fd, args.terms, args.limit, args.cursor)
            else:
                if not 4 <= args.bytes <= 8000:
                    raise ValueError('Read size must be between 4 and 8000 bytes.')
                result = read(fd, args.path, args.offset, args.bytes, args.version)
        finally:
            os.close(fd)
        output = encoded(result)
        if len(output.encode()) > OUTPUT_BYTES:
            raise ValueError('Response exceeds the output bound; retry with a smaller limit.')
        print(output)
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(encoded({'error': str(exc)}))
        return 2


if __name__ == '__main__':
    sys.exit(main())
