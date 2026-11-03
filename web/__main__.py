"""python -m tools.web — serve static sites, preview decks."""

from __future__ import annotations

import argparse

from tools.web.pack import add_pack_parser, run_pack
from tools.web.serve import add_serve_parser, run_serve


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m tools.web")
    sub = parser.add_subparsers(dest="command", required=True)
    add_serve_parser(sub)
    add_pack_parser(sub)
    args = parser.parse_args(argv)

    if args.command == "serve":
        return run_serve(args)
    if args.command == "pack":
        return run_pack(args)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
