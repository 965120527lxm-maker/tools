"""HTML slide building blocks for browser decks."""

from __future__ import annotations

import base64
import html
from pathlib import Path

_MIME = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
    ".svg": "image/svg+xml",
}


def esc(text: str) -> str:
    return html.escape(str(text))


def esc_attr(text: str) -> str:
    return html.escape(str(text), quote=True)


_editable = False


def set_editable(enabled: bool) -> None:
    """Toggle borderless in-browser editing for text components."""
    global _editable
    _editable = enabled


def _line(text: str, *, cls: str = "", edit_key: str = "") -> str:
    t = str(text)
    if not _editable:
        return esc(t)
    keys = f' data-edit-key="{esc_attr(edit_key)}"' if edit_key else ""
    extra = f" {cls}".strip()
    return (
        f'<input type="text" class="deck-edit deck-edit-line{extra}"{keys} '
        f'value="{esc_attr(t)}"/>'
    )


def _block(text: str, *, tag: str = "div", cls: str = "", edit_key: str = "") -> str:
    t = str(text)
    if not _editable:
        return esc(t)
    keys = f' data-edit-key="{esc_attr(edit_key)}"' if edit_key else ""
    classes = f"deck-edit deck-edit-block {cls}".strip()
    return (
        f'<{tag} class="{classes}" contenteditable="false" spellcheck="false"{keys}>'
        f"{esc(t)}</{tag}>"
    )


def cover_inner(title: str, subtitle: str = "", meta: str = "") -> str:
    """Cover / title slide with optional borderless editable fields."""
    if not _editable:
        sub = f'<p class="subtitle">{esc(subtitle)}</p>' if subtitle else ""
        meta_html = f'<p class="meta">{esc(meta)}</p>' if meta else ""
        return (
            f'<div class="cover-inner"><h1>{esc(title)}</h1>{sub}{meta_html}</div>'
        )
    sub = (
        f'<p class="subtitle deck-edit deck-edit-block" contenteditable="false" '
        f'spellcheck="false" data-edit-key="subtitle">{esc(subtitle)}</p>'
        if subtitle
        else ""
    )
    meta_html = (
        f'<p class="meta deck-edit deck-edit-block" contenteditable="false" '
        f'spellcheck="false" data-edit-key="meta">{esc(meta)}</p>'
        if meta
        else ""
    )
    return (
        f'<div class="cover-inner">'
        f'<h1 class="deck-edit deck-edit-block deck-edit-cover-title" contenteditable="false" '
        f'spellcheck="false" data-edit-key="title">{esc(title)}</h1>'
        f"{sub}{meta_html}</div>"
    )


def chapter_inner(section: str, title: str, subtitle: str = "") -> str:
    if not _editable:
        sub = f'<p class="subtitle">{esc(subtitle)}</p>' if subtitle else ""
        return (
            f'<div class="cover-inner chapter-inner">'
            f'<div class="sec">{esc(section)}</div>'
            f"<h1>{esc(title)}</h1>{sub}</div>"
        )
    sub = (
        f'<p class="subtitle deck-edit deck-edit-block" contenteditable="false" '
        f'spellcheck="false" data-edit-key="subtitle">{esc(subtitle)}</p>'
        if subtitle
        else ""
    )
    return (
        f'<div class="cover-inner chapter-inner">'
        f'<div class="sec deck-edit deck-edit-block" contenteditable="false" '
        f'spellcheck="false" data-edit-key="section">{esc(section)}</div>'
        f'<h1 class="deck-edit deck-edit-block" contenteditable="false" '
        f'spellcheck="false" data-edit-key="title">{esc(title)}</h1>'
        f"{sub}</div>"
    )


def image_src(path: str | Path, *, embed: bool = False) -> str:
    """Return a URL for <img src>: relative web path, http(s) URL, or data URI.

    embed=True reads the file and returns base64 data URI (single-file deck).
    """
    raw = str(path)
    if raw.startswith(("http://", "https://", "data:")):
        return raw
    p = Path(path)
    if embed:
        if not p.is_file():
            raise FileNotFoundError(p)
        mime = _MIME.get(p.suffix.lower(), "application/octet-stream")
        b64 = base64.b64encode(p.read_bytes()).decode("ascii")
        return f"data:{mime};base64,{b64}"
    return raw.replace("\\", "/")


def figure(
    src: str | Path,
    caption: str = "",
    *,
    alt: str = "",
    max_height: str = "220px",
    embed: bool = False,
) -> str:
    """Single figure with optional caption (content description, not Fig. N)."""
    url = image_src(src, embed=embed)
    alt_text = esc(alt or caption or "figure")
    cap_html = (
        f'<figcaption class="deck-edit deck-edit-block" contenteditable="false" '
        f'spellcheck="false">{esc(caption)}</figcaption>'
        if caption and _editable
        else (f"<figcaption>{esc(caption)}</figcaption>" if caption else "")
    )
    return (
        f'<figure class="figure">'
        f'<img src="{esc(url)}" alt="{alt_text}" style="max-height:{esc(max_height)}"/>'
        f"{cap_html}</figure>"
    )


def figure_row(
    sources: list[str | Path],
    captions: list[str] | None = None,
    *,
    max_height: str = "180px",
    embed: bool = False,
) -> str:
    """Side-by-side figures (2–3 panels)."""
    caps = captions or [""] * len(sources)
    panels = []
    for src, cap in zip(sources, caps):
        url = image_src(src, embed=embed)
        cap_html = (
            f'<figcaption class="deck-edit deck-edit-block" contenteditable="false" '
            f'spellcheck="false">{esc(cap)}</figcaption>'
            if cap and _editable
            else (f"<figcaption>{esc(cap)}</figcaption>" if cap else "")
        )
        panels.append(
            f'<div class="figure-panel">'
            f'<img src="{esc(url)}" alt="{esc(cap or "panel")}" '
            f'style="max-height:{esc(max_height)}"/>{cap_html}</div>'
        )
    return f'<div class="figure-row">{"".join(panels)}</div>'


def figure_with_text(
    src: str | Path,
    bullets_items: list[str],
    *,
    caption: str = "",
    side: str = "left",
    max_height: str = "200px",
    embed: bool = False,
) -> str:
    """Figure on one side, bullet list on the other."""
    fig = figure(src, caption, max_height=max_height, embed=embed)
    text = bullets(bullets_items)
    if side == "right":
        return f'<div class="figure-split">{text}<div>{fig}</div></div>'
    return f'<div class="figure-split"><div>{fig}</div>{text}</div>'


def tbl(headers: list[str], rows: list[list[str]], *, compact: bool = False) -> str:
    cls = "data-table compact" if compact else "data-table"
    if not _editable:
        thead = "".join(f"<th>{esc(c)}</th>" for c in headers)
        body = ""
        for row in rows:
            cells = row + [""] * (len(headers) - len(row))
            body += "<tr>" + "".join(f"<td>{esc(c)}</td>" for c in cells[: len(headers)]) + "</tr>"
    else:
        thead = "".join(f"<th>{_line(c, cls='deck-edit-cell')}</th>" for c in headers)
        body = ""
        for row in rows:
            cells = row + [""] * (len(headers) - len(row))
            body += (
                "<tr>"
                + "".join(
                    f"<td>{_line(c, cls='deck-edit-cell')}</td>"
                    for c in cells[: len(headers)]
                )
                + "</tr>"
            )
    return (
        f'<div class="table-wrap"><table class="{cls}">'
        f"<thead><tr>{thead}</tr></thead><tbody>{body}</tbody></table></div>"
    )


def bullets(items: list[str]) -> str:
    if not _editable:
        return "<ul>" + "".join(f"<li>{esc(x)}</li>" for x in items) + "</ul>"
    lis = "".join(
        f'<li><div class="deck-edit deck-edit-block" contenteditable="false" '
        f'spellcheck="false">{esc(x)}</div></li>'
        for x in items
    )
    return f"<ul>{lis}</ul>"


def takeaway(text: str) -> str:
    if not _editable:
        return f'<div class="takeaway">{esc(text)}</div>'
    return (
        f'<div class="takeaway deck-edit deck-edit-block" contenteditable="false" '
        f'spellcheck="false">{esc(text)}</div>'
    )


def note(text: str) -> str:
    if not _editable:
        return f'<p class="note">{esc(text)}</p>'
    return (
        f'<p class="note deck-edit deck-edit-block" contenteditable="false" '
        f'spellcheck="false">{esc(text)}</p>'
    )


def twocol(
    left_title: str,
    left: list[str],
    right_title: str,
    right: list[str],
    note_text: str = "",
) -> str:
    if not _editable:
        note_html = f'<p class="note">{esc(note_text)}</p>' if note_text else ""
        return f"""
    <div class="twocol">
      <div><h3>{esc(left_title)}</h3>{bullets(left)}</div>
      <div><h3>{esc(right_title)}</h3>{bullets(right)}</div>
    </div>{note_html}"""
    note_html = note(note_text) if note_text else ""
    return f"""
    <div class="twocol">
      <div><h3 class="deck-edit deck-edit-block" contenteditable="false" spellcheck="false">{esc(left_title)}</h3>{bullets(left)}</div>
      <div><h3 class="deck-edit deck-edit-block" contenteditable="false" spellcheck="false">{esc(right_title)}</h3>{bullets(right)}</div>
    </div>{note_html}"""


def flow(steps: list[str]) -> str:
    if not _editable:
        parts = "".join(
            f'<div class="flow-step"><span>{i + 1}</span>{esc(s)}</div>'
            for i, s in enumerate(steps)
        )
    else:
        parts = "".join(
            f'<div class="flow-step"><span>{i + 1}</span>'
            f'<span class="deck-edit deck-edit-block" contenteditable="false" spellcheck="false">{esc(s)}</span></div>'
            for i, s in enumerate(steps)
        )
    return f'<div class="flow">{parts}</div>'


def formula_block(body: str, tex: str, note_text: str = "") -> str:
    if not _editable:
        note_html = f'<p class="note">{esc(note_text)}</p>' if note_text else ""
        return f"""
    <p class="lead">{esc(body)}</p>
    <div class="math display">\\[{tex}\\]</div>
    {note_html}"""
    note_html = note(note_text) if note_text else ""
    return f"""
    <p class="lead deck-edit deck-edit-block" contenteditable="false" spellcheck="false">{esc(body)}</p>
    <div class="math display">\\[{tex}\\]</div>
    {note_html}"""


def chart_box(canvas_id: str, *, tall: bool = False) -> str:
    cls = "chart-box tall" if tall else "chart-box"
    return f'<div class="{cls}"><canvas id="{esc(canvas_id)}"></canvas></div>'
