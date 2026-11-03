"""LaTeX → SVG formula rendering for slides."""

from __future__ import annotations

import hashlib
import os
from xml.etree import ElementTree

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pptx.util import Inches

from .layout import add_bullet_box, add_caption, add_highlight_block, add_title_shape, blank_slide
from .svg import _svg_viewport_px_size, apply_pptx_svg_support
from .theme import (
    ACCENT_ORANGE,
    FORMULA_COL_MAX_WIDTH,
    FORMULA_DEFAULT_FONTSIZE,
    FORMULA_DEFAULT_HEIGHT,
    FORMULA_LONG_CHAR_THRESHOLD,
    FORMULA_LONG_FONTSIZE,
    FORMULA_LONG_HEIGHT,
    FORMULA_STACK_GAP,
    FS_BODY_COMPACT,
    FS_CAPTION,
    FS_SECTION,
)

_FORMULA_DIR: str | None = None


def set_formula_dir(path: str):
    """Set cache directory for rendered formula SVGs."""
    global _FORMULA_DIR
    _FORMULA_DIR = path
    os.makedirs(path, exist_ok=True)


def get_formula_dir() -> str:
    if _FORMULA_DIR is None:
        raise RuntimeError(
            "formula dir unset; call set_formula_dir('/path/to/formula_cache') first"
        )
    return _FORMULA_DIR


def _is_long_latex(latex_str: str, explicit: bool | None = None) -> bool:
    if explicit is not None:
        return explicit
    return len(latex_str) >= FORMULA_LONG_CHAR_THRESHOLD


def render_latex(latex_str, fontsize=None, pad=0.06, fig_width=None):
    """Render LaTeX to a tight SVG. ``fontsize`` is matplotlib pt (not slide pt)."""
    if fontsize is None:
        fontsize = FORMULA_DEFAULT_FONTSIZE
    apply_pptx_svg_support()
    # Wider canvas for long expressions; keep figure height small to cut SVG padding.
    fw = fig_width or max(6.0, min(12.0, 0.055 * len(latex_str) + 3.5))
    fh = max(0.55, min(1.05, 0.028 * fontsize + 0.15))
    key = hashlib.sha1(f"{latex_str}|{fontsize}|{pad}|{fw}|{fh}".encode()).hexdigest()[:16]
    formula_dir = get_formula_dir()
    svg_path = os.path.join(formula_dir, f"{key}.svg")
    if os.path.exists(svg_path):
        return svg_path
    os.makedirs(formula_dir, exist_ok=True)
    with plt.rc_context({
        "font.family": "serif",
        "font.serif": ["Times New Roman"],
        "mathtext.fontset": "stix",
    }):
        fig = plt.figure(figsize=(fw, fh))
        fig.text(0.5, 0.5, f"${latex_str}$", fontsize=fontsize, ha="center", va="center")
        plt.axis("off")
        fig.savefig(svg_path, format="svg", bbox_inches="tight", pad_inches=pad, transparent=True)
        plt.close(fig)
    return svg_path


def svg_aspect_ratio(svg_path):
    root = ElementTree.parse(svg_path).getroot()
    width_px, height_px = _svg_viewport_px_size(root)
    return width_px / max(height_px, 1e-6)


def add_formula(
    slide,
    latex_str,
    left=Inches(0.8),
    top=Inches(1.5),
    height=None,
    fontsize=None,
    fig_width=None,
    max_width=FORMULA_COL_MAX_WIDTH,
    long: bool | None = None,
):
    """Place a formula SVG, sized to match body text scale.

    Uses ``height`` as a *max* height: start from that target, then shrink if
    width would exceed ``max_width``. Long expressions auto-pick smaller defaults
    so short/long formulas in one stack look consistent.
    """
    is_long = _is_long_latex(latex_str, long)
    if height is None:
        height = FORMULA_LONG_HEIGHT if is_long else FORMULA_DEFAULT_HEIGHT
    if fontsize is None:
        fontsize = FORMULA_LONG_FONTSIZE if is_long else FORMULA_DEFAULT_FONTSIZE

    apply_pptx_svg_support()
    svg_path = render_latex(latex_str, fontsize=fontsize, fig_width=fig_width)
    aspect = svg_aspect_ratio(svg_path)

    width = height * aspect
    if max_width is not None and width > max_width:
        width = max_width
        height = width / aspect

    pic = slide.shapes.add_picture(svg_path, left, top, width=width, height=height)
    return pic, width, height


def add_formula_stack(
    slide,
    formulas,
    left=Inches(0.6),
    top=Inches(1.45),
    label_width=Inches(1.35),
    gap=FORMULA_STACK_GAP,
    max_width=FORMULA_COL_MAX_WIDTH,
):
    """Stack labeled formulas. Each item: label, latex, optional long/fontsize/height/fig_width/gap."""
    y = top
    for item in formulas:
        label = item["label"]
        latex = item["latex"]
        is_long = _is_long_latex(latex, item.get("long"))
        fh = item.get("height", FORMULA_LONG_HEIGHT if is_long else FORMULA_DEFAULT_HEIGHT)
        fs = item.get("fontsize", FORMULA_LONG_FONTSIZE if is_long else FORMULA_DEFAULT_FONTSIZE)
        add_caption(
            slide, label, top=y + Inches(0.12), left=left,
            width=label_width, font_size=FS_SECTION, color=ACCENT_ORANGE,
        )
        latex_left = left + label_width + Inches(0.05)
        _, _, rendered_h = add_formula(
            slide, latex, left=latex_left, top=y,
            height=fh, fontsize=fs, fig_width=item.get("fig_width"),
            max_width=max_width - label_width - Inches(0.05),
            long=is_long,
        )
        y += rendered_h + item.get("gap", gap)
    return y


def add_method_formulas_slide(
    prs, title, formulas, bullets, note=None, emphasize_words=None, formula_gap=None,
):
    slide = blank_slide(prs)
    add_title_shape(slide, title)
    add_formula_stack(
        slide, formulas, left=Inches(0.55), top=Inches(1.42),
        label_width=Inches(1.35),
        gap=formula_gap if formula_gap is not None else FORMULA_STACK_GAP,
    )
    add_bullet_box(
        slide, bullets, top=Inches(1.45), left=Inches(7.05),
        width=Inches(5.65), height=Inches(4.6), font_size=FS_BODY_COMPACT,
        emphasize_words=emphasize_words or [],
    )
    if note:
        add_highlight_block(
            slide, note, top=Inches(6.15), left=Inches(0.55),
            width=Inches(12.2), height=Inches(0.7), font_size=FS_CAPTION,
        )
    return slide
