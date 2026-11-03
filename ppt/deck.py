"""Presentation factory and thin Deck helper."""

from __future__ import annotations

import os

from pptx import Presentation

from .layout import (
    add_chapter_divider,
    add_simple_cover_slide,
    content_slide,
    set_slide_size,
)
from .svg import apply_pptx_svg_support


def new_presentation(enable_svg: bool = True) -> Presentation:
    """Create a 16:9 blank presentation, optionally enabling SVG pictures."""
    if enable_svg:
        apply_pptx_svg_support()
    prs = Presentation()
    set_slide_size(prs)
    return prs


class Deck:
    """Minimal page counter + shortcuts for content decks."""

    def __init__(self, author: str = "", total: int | None = None, enable_svg: bool = True):
        self.prs = new_presentation(enable_svg=enable_svg)
        self.author = author
        self.total = total
        self.page = 0

    def cover(self, title: str, footer_line: str = "", date_line: str = ""):
        return add_simple_cover_slide(self.prs, title, footer_line, date_line)

    def chapter(self, number, title: str, subtitle: str = ""):
        return add_chapter_divider(self.prs, number, title, subtitle)

    def content(self, title: str):
        self.page += 1
        return content_slide(
            self.prs,
            title,
            page_num=self.page,
            total=self.total,
            footer_left=self.author,
        )

    def save(self, path: str):
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        self.prs.save(path)
        return path
