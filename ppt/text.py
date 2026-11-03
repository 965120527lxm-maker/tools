"""Text styling helpers for python-pptx."""

from __future__ import annotations

from pptx.util import Pt

from .theme import ACCENT_ORANGE, DARK_GRAY, FONT_CN, FS_BODY, FS_CAPTION


def _as_pt(font_size):
    """Accept int pt or already-constructed Length/Pt."""
    if font_size is None:
        return None
    if hasattr(font_size, "pt"):
        return font_size
    return Pt(font_size)


def style_run(run, font_size=None, bold=None, color=None, name=FONT_CN):
    run.font.name = name
    if font_size is not None:
        run.font.size = _as_pt(font_size)
    if bold is not None:
        run.font.bold = bold
    if color is not None:
        run.font.color.rgb = color


def style_paragraph(p, font_size=None, bold=None, color=None, name=FONT_CN):
    for run in p.runs:
        style_run(run, font_size, bold, color, name)


def style_text_frame(tf, font_size=None, bold=None, color=None, name=FONT_CN):
    for p in tf.paragraphs:
        style_paragraph(p, font_size, bold, color, name)


def set_shape_text(shape, text, font_size=None, bold=False, color=DARK_GRAY):
    if font_size is None:
        font_size = FS_CAPTION
    tf = shape.text_frame
    tf.text = text
    style_text_frame(tf, font_size, bold, color)


def apply_emphasis(paragraph, text, words, base_color, accent_color=ACCENT_ORANGE, font_size=None):
    """Split `text` into runs, emphasizing any of `words` with accent color + bold."""
    if font_size is None:
        font_size = FS_BODY
    size = _as_pt(font_size)
    paragraph.clear()
    if not words:
        run = paragraph.add_run()
        run.text = text
        run.font.color.rgb = base_color
        run.font.size = size
        run.font.name = FONT_CN
        return
    sorted_words = sorted(words, key=len, reverse=True)
    segments = [(text, False)]
    for word in sorted_words:
        new_segments = []
        for seg_text, emphasized in segments:
            if emphasized or word not in seg_text:
                new_segments.append((seg_text, emphasized))
                continue
            parts = seg_text.split(word)
            for i, part in enumerate(parts):
                new_segments.append((part, False))
                if i < len(parts) - 1:
                    new_segments.append((word, True))
        segments = new_segments

    for seg_text, emphasized in segments:
        if not seg_text:
            continue
        run = paragraph.add_run()
        run.text = seg_text
        run.font.size = size
        run.font.color.rgb = accent_color if emphasized else base_color
        run.font.bold = emphasized
        run.font.name = FONT_CN
