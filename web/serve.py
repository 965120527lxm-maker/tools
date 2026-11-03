"""Static file server for local HTML preview."""

from __future__ import annotations

import argparse
import http.server
import os
import socket
import socketserver
import webbrowser
from pathlib import Path


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args) -> None:  # noqa: A003
        if self.log_date_time_string:
            print(f"[{self.log_date_time_string}] {format % args}")


def find_free_port(host: str, start: int) -> int:
    for port in range(start, start + 50):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind((host, port))
                return port
            except OSError:
                continue
    raise RuntimeError(f"no free port in range {start}..{start + 49}")


def serve_directory(
    directory: str | Path,
    *,
    host: str = "0.0.0.0",
    port: int = 8765,
    open_path: str | None = None,
    open_browser: bool = False,
) -> None:
    root = Path(directory).resolve()
    if not root.is_dir():
        raise FileNotFoundError(f"not a directory: {root}")

    actual_port = find_free_port(host if host != "0.0.0.0" else "127.0.0.1", port)
    os.chdir(root)

    handler = QuietHandler
    httpd = socketserver.TCPServer((host, actual_port), handler)
    httpd.allow_reuse_address = True

    base = f"http://127.0.0.1:{actual_port}"
    target = f"{base}/{open_path.lstrip('/')}" if open_path else base
    print(f"Serving {root}")
    print(f"  → {target}")
    print("Ctrl+C to stop")

    if open_browser:
        webbrowser.open(target)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        httpd.server_close()


def add_serve_parser(subparsers: argparse._SubParsersAction) -> None:
    p = subparsers.add_parser("serve", help="serve a directory over HTTP")
    p.add_argument("directory", nargs="?", default=".", help="root directory (default: .)")
    p.add_argument("--host", default="0.0.0.0", help="bind address (default: 0.0.0.0)")
    p.add_argument("--port", type=int, default=8765, help="preferred port (default: 8765)")
    p.add_argument("--open", dest="open_path", default=None, help="path to open, e.g. deck.html")
    p.add_argument(
        "--browser",
        action="store_true",
        help="open system browser (local only)",
    )


def run_serve(args: argparse.Namespace) -> int:
    serve_directory(
        args.directory,
        host=args.host,
        port=args.port,
        open_path=args.open_path,
        open_browser=args.browser,
    )
    return 0
