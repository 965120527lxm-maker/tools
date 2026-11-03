"""WebDeck — browser slide presentation (KaTeX + optional Chart.js)."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .render import render_deck_html


@dataclass
class WebSlide:
    title: str
    section: str
    body: str
    kind: str = "content"
    chart: str | None = None


@dataclass
class WebDeck:
    """Collect slides and render a self-contained HTML deck."""

    document_title: str = "Presentation"
    nav_links: list[tuple[str, str]] = field(default_factory=list)
    editable: bool = True
    _slides: list[WebSlide] = field(default_factory=list, init=False)

    def cover(self, body_html: str) -> None:
        self._slides.append(WebSlide("", "封面", body_html, kind="cover"))

    def chapter(self, section: str, title: str, subtitle: str = "") -> None:
        from .components import chapter_inner

        body = chapter_inner(section, title, subtitle)
        self._slides.append(WebSlide("", section, body, kind="chapter"))

    def slide(
        self,
        title: str,
        section: str,
        body_html: str,
        *,
        chart: str | None = None,
    ) -> None:
        self._slides.append(WebSlide(title, section, body_html, chart=chart))

    def to_dicts(self) -> list[dict[str, Any]]:
        return [
            {
                "title": s.title,
                "section": s.section,
                "body": s.body,
                "kind": s.kind,
                "chart": s.chart,
            }
            for s in self._slides
        ]

    def save(
        self,
        path: str | Path,
        *,
        charts: dict[str, Any] | None = None,
    ) -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        from . import components

        components.set_editable(self.editable)
        try:
            html = render_deck_html(
                document_title=self.document_title,
                slides=self.to_dicts(),
                charts=charts or {},
                nav_links=self.nav_links,
                editable=self.editable,
            )
        finally:
            components.set_editable(False)
        out.write_text(html, encoding="utf-8")
        return out

    def __len__(self) -> int:
        return len(self._slides)


def load_json_charts(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    if not p.is_file():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))
