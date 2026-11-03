"""Native PPT flowchart primitives (boxes + simple arrows).

Uses python-pptx shapes — no external diagram tool. Style stays 简约学术式:
solid fills, short labels, thin connectors.
"""

from __future__ import annotations

from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt

from .layout import add_highlight_block
from .theme import (
    ACCENT_ORANGE,
    DARK_BLUE,
    FONT_CN,
    FS_CAPTION,
    FS_FLOW,
    FS_HIGHLIGHT,
    SLIDE_WIDTH,
    PALE_BLUE,
    PALE_ORANGE,
    WHITE,
)

# box styles: fill, text color
_BOX_STYLES = {
    "primary": (DARK_BLUE, WHITE),
    "accent": (ACCENT_ORANGE, WHITE),
    "muted": (PALE_BLUE, DARK_BLUE),
    "soft": (PALE_ORANGE, DARK_BLUE),
}


def add_flow_box(
    slide,
    left,
    top,
    width,
    height,
    text: str,
    *,
    style: str = "primary",
    font_size: int = FS_FLOW,
    rounded: bool = True,
):
    """Add a labeled rectangle / rounded rectangle on the slide."""
    fill, text_color = _BOX_STYLES.get(style, _BOX_STYLES["primary"])
    shape_type = MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE
    shape = slide.shapes.add_shape(shape_type, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.fill.background()

    tf = shape.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    try:
        shape.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    except Exception:
        pass
    # vertical center via anchor
    tf.paragraphs[0].space_before = Pt(0)
    tf.paragraphs[0].space_after = Pt(0)
    p = tf.paragraphs[0]
    p.clear()
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = True
    run.font.color.rgb = text_color
    run.font.name = FONT_CN
    p.alignment = PP_ALIGN.CENTER
    try:
        tf.paragraphs[0].font.size = Pt(font_size)
    except Exception:
        pass
    # MSO_ANCHOR on text frame
    try:
        from pptx.enum.text import MSO_ANCHOR as _ANCHOR
        tf.anchor = _ANCHOR.MIDDLE
    except Exception:
        pass
    return shape


def add_h_arrow(slide, left, top, width, *, color=None, height=None):
    """Horizontal connector: thin bar + right triangle tip."""
    color = color or ACCENT_ORANGE
    height = height or Inches(0.06)
    bar_w = width - Inches(0.14)
    if bar_w < Inches(0.05):
        bar_w = width * 0.6
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, bar_w, height)
    bar.fill.solid()
    bar.fill.fore_color.rgb = color
    bar.line.fill.background()
    tip = slide.shapes.add_shape(
        MSO_SHAPE.RIGHT_ARROW,
        left + bar_w - Inches(0.02),
        top - Inches(0.05),
        Inches(0.22),
        height + Inches(0.1),
    )
    tip.fill.solid()
    tip.fill.fore_color.rgb = color
    tip.line.fill.background()
    return bar, tip


def add_v_arrow(slide, left, top, height, *, color=None, width=None):
    """Vertical connector pointing down."""
    color = color or ACCENT_ORANGE
    width = width or Inches(0.06)
    bar_h = height - Inches(0.14)
    if bar_h < Inches(0.05):
        bar_h = height * 0.6
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, bar_h)
    bar.fill.solid()
    bar.fill.fore_color.rgb = color
    bar.line.fill.background()
    tip = slide.shapes.add_shape(
        MSO_SHAPE.DOWN_ARROW,
        left - Inches(0.05),
        top + bar_h - Inches(0.02),
        width + Inches(0.1),
        Inches(0.22),
    )
    tip.fill.solid()
    tip.fill.fore_color.rgb = color
    tip.line.fill.background()
    return bar, tip


def add_flowchart_row(
    slide,
    nodes: list[dict | str],
    *,
    top=Inches(2.2),
    left=None,
    box_width=Inches(2.1),
    box_height=Inches(0.95),
    gap=Inches(0.35),
    font_size: int = FS_FLOW,
):
    """Horizontal flow: box → box → …

    Each node is a str label, or dict with keys:
      text, style ('primary'|'accent'|'muted'|'soft'), width, height

    left=None（默认）时整行在画布中水平居中；显式 left 则按左锚排布。
    """
    if left is None:
        total = sum(
            (n.get("width", box_width) if isinstance(n, dict) else box_width) for n in nodes
        ) + gap * (len(nodes) - 1)
        left = max(Inches(0.55), (SLIDE_WIDTH - total) / 2)
    x = left
    shapes = []
    centers_y = top + box_height / 2
    for i, node in enumerate(nodes):
        if isinstance(node, str):
            text, style = node, "primary" if i % 2 == 0 else "muted"
            bw, bh = box_width, box_height
        else:
            text = node["text"]
            style = node.get("style", "primary" if i % 2 == 0 else "muted")
            bw = node.get("width", box_width)
            bh = node.get("height", box_height)
        shapes.append(add_flow_box(slide, x, top, bw, bh, text, style=style, font_size=font_size))
        next_x = x + bw + gap
        if i < len(nodes) - 1:
            arrow_left = x + bw + Inches(0.04)
            arrow_w = gap - Inches(0.08)
            add_h_arrow(slide, arrow_left, centers_y - Inches(0.03), arrow_w)
        x = next_x
    return shapes


def add_flowchart(
    slide,
    rows: list[list[dict | str]],
    *,
    top=Inches(1.45),
    left=Inches(0.55),
    box_width=Inches(2.1),
    box_height=Inches(0.9),
    h_gap=Inches(0.32),
    v_gap=Inches(0.55),
    row_label: list[str] | None = None,
    note: str | None = None,
    font_size: int = FS_FLOW,
):
    """Multi-row flowchart. Optional row_label drawn at left of each row.

    Vertical arrow is drawn from the last box of row i down to the first box of row i+1
    when both rows are non-empty (simple “continue” cue). For richer topology, place
    boxes with add_flow_box manually.
    """
    y = top
    label_w = Inches(1.15) if row_label else Inches(0)
    box_left0 = left + label_w
    all_shapes = []

    for r, nodes in enumerate(rows):
        if row_label and r < len(row_label):
            lab = slide.shapes.add_textbox(left, y + Inches(0.25), label_w - Inches(0.08), Inches(0.5))
            p = lab.text_frame.paragraphs[0]
            p.text = row_label[r]
            p.font.size = Pt(FS_CAPTION)
            p.font.bold = True
            p.font.color.rgb = ACCENT_ORANGE
            p.font.name = FONT_CN

        shapes = add_flowchart_row(
            slide, nodes,
            top=y, left=box_left0,
            box_width=box_width, box_height=box_height,
            gap=h_gap, font_size=font_size,
        )
        all_shapes.append(shapes)

        if r < len(rows) - 1 and shapes and rows[r + 1]:
            # drop from center of last box to next row
            last = shapes[-1]
            cx = last.left + last.width / 2
            arrow_top = y + box_height + Inches(0.06)
            add_v_arrow(slide, cx - Inches(0.03), arrow_top, v_gap - Inches(0.1))

        y += box_height + v_gap

    if note:
        add_highlight_block(
            slide, note, top=Inches(6.2), left=Inches(0.55),
            width=Inches(12.2), height=Inches(0.6), font_size=FS_HIGHLIGHT,
        )
    return all_shapes
