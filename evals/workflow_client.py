#!/usr/bin/env python3
"""Call this workspace's synthetic product service; no live service access."""
from __future__ import annotations

import argparse
import http.client
import json
from pathlib import Path
import socket


class LocalConnection(http.client.HTTPConnection):
    def __init__(self, path: Path):
        super().__init__('localhost', timeout=15)
        self.path = path

    def connect(self) -> None:
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.settimeout(self.timeout)
        self.sock.connect(str(self.path))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation')
    parser.add_argument('arguments', nargs='?', default='{}', help='JSON object')
    parser.add_argument('--socket', type=Path, default=Path('/workspace/tools/service.sock'))
    args = parser.parse_args()
    arguments = json.loads(args.arguments)
    if not isinstance(arguments, dict):
        parser.error('arguments must be a JSON object')
    connection = LocalConnection(args.socket)
    try:
        connection.request('POST', '/', json.dumps({'operation': args.operation, 'arguments': arguments}),
                           {'Content-Type': 'application/json'})
        response = connection.getresponse()
        print(response.read().decode())
        return int(response.status != 200)
    finally:
        connection.close()


if __name__ == '__main__':
    raise SystemExit(main())
