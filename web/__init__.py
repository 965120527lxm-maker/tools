"""Shared web tooling — browser decks, static preview, project HTML sites."""

from tools.web.deck import WebDeck, bullets, tbl, takeaway
from tools.web.serve import serve_directory

__all__ = [
    "WebDeck",
    "bullets",
    "tbl",
    "takeaway",
    "serve_directory",
]
