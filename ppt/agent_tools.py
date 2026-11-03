"""Agent-callable tool registry for tools.ppt.

Register thin, explicit tools here. Retrieval / search stays with the agent —
handlers only accept paths (or other args) the agent already chose.

Follow the reference pipeline in ``pipelines/agent_deck.md``::

    outline → generate_*.py (placeholders) → list_image_slots
           → agent retrieves images → fill_image_slots → final pptx

Usage (library)::

    from tools.ppt.agent_tools import get_agent_tools, call_agent_tool
    call_agent_tool("fill_image_slots", pptx_path="x.pptx", paths={"ddpm": "a.png"})

Usage (CLI)::

    python -m tools.ppt list_image_slots --pptx deck.pptx
    python -m tools.ppt fill_image_slots --pptx deck.pptx \\
        --paths '{"ddpm":"/path/a.png","ddim":"/path/b.png"}'
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Callable

from .slots import fill_image_slots_pptx, list_image_slots


def _tool_list_image_slots(*, pptx_path: str) -> list[dict]:
    return list_image_slots(pptx_path)


def _tool_fill_image_slots(
    *,
    pptx_path: str,
    paths: dict[str, str] | str,
    output_path: str | None = None,
) -> dict:
    return fill_image_slots_pptx(pptx_path, paths, output_path=output_path)


# OpenAI-/Cursor-style schemas. No scan/search parameters on purpose.
AGENT_TOOLS: list[dict[str, Any]] = [
    {
        "name": "list_image_slots",
        "description": (
            "Pipeline step after generate_*.py: list image placeholder slots "
            "already marked in a .pptx (shape names slot:<id>). Use the result "
            "to decide what to retrieve. Does not search for image files. "
            "See tools/ppt/pipelines/agent_deck.md."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "pptx_path": {
                    "type": "string",
                    "description": "Path to the .pptx that contains placeholders.",
                },
            },
            "required": ["pptx_path"],
        },
        "handler": _tool_list_image_slots,
    },
    {
        "name": "fill_image_slots",
        "description": (
            "Pipeline final fill step: after the agent retrieved suitable local "
            "images, write them into reserved slots. Pass an explicit "
            "{slot_id: path} map only — no directory scan, no auto-pick. "
            "See tools/ppt/pipelines/agent_deck.md."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "pptx_path": {
                    "type": "string",
                    "description": "Path to the .pptx with slot:<id> placeholders.",
                },
                "paths": {
                    "type": "object",
                    "additionalProperties": {"type": "string"},
                    "description": (
                        "Map of slot_id → absolute or relative local image path. "
                        "Only keys you intentionally fill; omit slots still pending."
                    ),
                },
                "output_path": {
                    "type": "string",
                    "description": "Optional save path; default overwrites pptx_path.",
                },
            },
            "required": ["pptx_path", "paths"],
        },
        "handler": _tool_fill_image_slots,
    },
]

_BY_NAME: dict[str, dict[str, Any]] = {t["name"]: t for t in AGENT_TOOLS}


def get_agent_tools(*, include_handlers: bool = False) -> list[dict[str, Any]]:
    """Return tool specs for agent/MCP registration.

    Handlers are omitted by default so the list is JSON-serializable.
    """
    out = []
    for t in AGENT_TOOLS:
        item = {
            "name": t["name"],
            "description": t["description"],
            "parameters": t["parameters"],
        }
        if include_handlers:
            item["handler"] = t["handler"]
        out.append(item)
    return out


def call_agent_tool(name: str, **kwargs) -> Any:
    """Dispatch a registered agent tool by name."""
    spec = _BY_NAME.get(name)
    if spec is None:
        known = ", ".join(sorted(_BY_NAME))
        raise KeyError(f"unknown agent tool {name!r}; known: {known}")
    handler: Callable[..., Any] = spec["handler"]
    return handler(**kwargs)


def _cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="tools.ppt.agent_tools")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_list = sub.add_parser("list_image_slots", help="List slot:<id> placeholders")
    p_list.add_argument("--pptx", required=True, dest="pptx_path")

    p_fill = sub.add_parser("fill_image_slots", help="Fill slots from JSON path map")
    p_fill.add_argument("--pptx", required=True, dest="pptx_path")
    p_fill.add_argument(
        "--paths",
        required=True,
        help='JSON object, e.g. \'{"ddpm":"/a.png","ddim":"/b.png"}\'',
    )
    p_fill.add_argument("--out", dest="output_path", default=None)

    p_dump = sub.add_parser("dump_registry", help="Print JSON tool schemas")

    args = parser.parse_args(argv)
    if args.cmd == "dump_registry":
        print(json.dumps(get_agent_tools(), ensure_ascii=False, indent=2))
        return 0
    if args.cmd == "list_image_slots":
        result = call_agent_tool("list_image_slots", pptx_path=args.pptx_path)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    if args.cmd == "fill_image_slots":
        result = call_agent_tool(
            "fill_image_slots",
            pptx_path=args.pptx_path,
            paths=args.paths,
            output_path=args.output_path,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    return 1


def main() -> None:
    sys.exit(_cli())


if __name__ == "__main__":
    main()
