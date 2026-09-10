"""One trajectory per Unix socket; no arm ID or filesystem path is accepted."""
from __future__ import annotations

from http.server import BaseHTTPRequestHandler
from collections.abc import Callable
import json
from pathlib import Path
import socketserver
import threading
from typing import Any

from workflow_world import call


class ProductService:
    def __init__(self, socket_path: Path, state: dict[str, Any], journal_path: Path,
                 dispatch: Callable[[dict[str, Any], str, dict[str, Any]], dict[str, Any]] = call):
        self.state = state
        self.journal_path = journal_path
        self.lock = threading.Lock()
        service = self

        class Handler(BaseHTTPRequestHandler):
            timeout = 15

            def do_POST(self) -> None:
                try:
                    length = int(self.headers.get('Content-Length', '0'))
                    if not 0 < length <= 1_000_000 or self.path != '/':
                        raise ValueError('Invalid request size or path')
                    request = json.loads(self.rfile.read(length))
                    if (not isinstance(request, dict) or set(request) != {'operation', 'arguments'}
                            or not isinstance(request['operation'], str) or not isinstance(request['arguments'], dict)):
                        raise ValueError('Expected operation and arguments only')
                    with service.lock:
                        response = dispatch(service.state, request['operation'], request['arguments'])
                        service.journal_path.write_text(json.dumps(service.state, indent=2) + '\n')
                    status = 200
                except (ValueError, KeyError, TypeError) as error:
                    response = {'ok': False, 'error': type(error).__name__}
                    status = 400
                content = json.dumps(response).encode()
                self.send_response(status)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(content)))
                self.end_headers()
                self.wfile.write(content)

            def log_message(self, format: str, *args: Any) -> None:
                pass

        self.server = socketserver.ThreadingUnixStreamServer(str(socket_path), Handler)
        # Close waits for in-flight requests before the caller snapshots state.
        self.server.daemon_threads = False
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.socket_path = socket_path

    def __enter__(self) -> ProductService:
        self.thread.start()
        return self

    def __exit__(self, *args: Any) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.socket_path.unlink(missing_ok=True)
