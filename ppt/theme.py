"""Shared academic PPT theme (16:9, dark-blue + orange).

Design language: 简约学术式 — see AGENTS.md.
"""

from __future__ import annotations

from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt

# Canvas
SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)

PALETTES = {
    # fudan ST / week1 / week2
    "academic": {
        "DARK_BLUE": RGBColor(0x1E, 0x3A, 0x5F),
        "ACCENT_ORANGE": RGBColor(0xE6, 0x7E, 0x22),
        "COVER_BOTTOM": RGBColor(0x1A, 0x4A, 0x7A),
        "LIGHT_GRAY": RGBColor(0xF5, 0xF5, 0xF5),
        "PALE_BLUE": RGBColor(0xE8, 0xEE, 0xF5),
        "PALE_ORANGE": RGBColor(0xFF, 0xF4, 0xE6),
        "DARK_GRAY": RGBColor(0x33, 0x33, 0x33),
        "MEDIUM_GRAY": RGBColor(0x88, 0x88, 0x88),
        "WHITE": RGBColor(0xFF, 0xFF, 0xFF),
        "BLACK": RGBColor(0x00, 0x00, 0x00),
        "FOOTER_GRAY": RGBColor(0x99, 0x99, 0x99),
    },
    # SpatialEx defense (slightly deeper blue / hotter orange)
    "defense": {
        "DARK_BLUE": RGBColor(0x1A, 0x23, 0x7E),
        "ACCENT_ORANGE": RGBColor(0xE8, 0x5D, 0x04),
        "COVER_BOTTOM": RGBColor(0x1A, 0x23, 0x7E),
        "LIGHT_GRAY": RGBColor(0xF5, 0xF5, 0xF5),
        "PALE_BLUE": RGBColor(0xEF, 0xF2, 0xFF),
        "PALE_ORANGE": RGBColor(0xFF, 0xF4, 0xE6),
        "DARK_GRAY": RGBColor(0x2B, 0x2B, 0x2B),
        "MEDIUM_GRAY": RGBColor(0x66, 0x66, 0x66),
        "WHITE": RGBColor(0xFF, 0xFF, 0xFF),
        "BLACK": RGBColor(0x00, 0x00, 0x00),
        "FOOTER_GRAY": RGBColor(0x99, 0x99, 0x99),
    },
}

# Colors — default academic
DARK_BLUE = PALETTES["academic"]["DARK_BLUE"]
ACCENT_ORANGE = PALETTES["academic"]["ACCENT_ORANGE"]
COVER_BOTTOM = PALETTES["academic"]["COVER_BOTTOM"]
LIGHT_GRAY = PALETTES["academic"]["LIGHT_GRAY"]
PALE_BLUE = PALETTES["academic"]["PALE_BLUE"]
PALE_ORANGE = PALETTES["academic"]["PALE_ORANGE"]
DARK_GRAY = PALETTES["academic"]["DARK_GRAY"]
MEDIUM_GRAY = PALETTES["academic"]["MEDIUM_GRAY"]
WHITE = PALETTES["academic"]["WHITE"]
BLACK = PALETTES["academic"]["BLACK"]
FOOTER_GRAY = PALETTES["academic"]["FOOTER_GRAY"]
ACTIVE_PALETTE = "academic"


def set_palette(name: str = "academic", sync_module=None):
    """Switch color palette and sync already-imported submodule globals.

    If ``sync_module`` is given (usually the caller module's ``globals()`` or
    ``sys.modules[__name__]``), also refresh color names there.
    """
    global ACTIVE_PALETTE
    if name not in PALETTES:
        raise KeyError(f"unknown palette {name!r}; choose from {sorted(PALETTES)}")
    ACTIVE_PALETTE = name
    palette = PALETTES[name]
    g = globals()
    for key, value in palette.items():
        g[key] = value

    # layout/text/formulas/__init__ bind color names at import time — refresh them
    from . import formulas, layout, text
    import tools.ppt as ppt_pkg

    targets = [layout, text, formulas, ppt_pkg]
    if sync_module is not None:
        targets.append(sync_module)
    for mod in targets:
        mapping = mod if isinstance(mod, dict) else mod.__dict__
        for key, value in palette.items():
            if key in mapping or (not isinstance(mod, dict) and hasattr(mod, key)):
                if isinstance(mod, dict):
                    mod[key] = value
                else:
                    setattr(mod, key, value)
    return name

# Typography — sizes are int pt (call sites wrap with Pt()).
# Scale target (AGENTS.md): title 28–32, body 18–20, caption/note 14.
FONT_CN = "华文中宋"
FONT_CN_FALLBACK = ["Noto Sans CJK SC", "WenQuanYi Micro Hei", "SimHei", "DejaVu Sans"]

FS_COVER = 40
FS_CHAPTER = 36
FS_CHAPTER_LABEL = 22
FS_CHAPTER_SUB = 18
FS_TITLE = 28          # content-page title
FS_SECTION = 20        # section / column header
FS_BODY = 18
FS_BODY_COMPACT = 16   # two-column / dense pages
FS_HIGHLIGHT = 15      # bottom conclusion bar
FS_CAPTION = 14
FS_TABLE_HEADER = 15
FS_TABLE_BODY = 14
FS_FOOTER = 11
FS_FLOW = 13           # flowchart box label

# Back-compat aliases (prefer FS_* above)
TITLE_FONT_SIZE = FS_TITLE
SECTION_FONT_SIZE = FS_SECTION
BODY_FONT_SIZE = FS_BODY
SMALL_FONT_SIZE = FS_HIGHLIGHT
CAPTION_FONT_SIZE = FS_CAPTION

LINE_SPACING_NORMAL = 1.15
LINE_SPACING_LOOSE = 1.25

# Margins
MARGIN_LEFT = Inches(0.6)
MARGIN_RIGHT = Inches(0.6)
CONTENT_WIDTH = Inches(12.0)

# Formula defaults (matplotlib fontsize + on-slide max height).
# Long eqs auto-shrink to max_width; keep max_height modest so short/long match.
FORMULA_DEFAULT_FONTSIZE = 26
FORMULA_DEFAULT_HEIGHT = Inches(0.78)
FORMULA_LONG_FONTSIZE = 22
FORMULA_LONG_HEIGHT = Inches(0.70)
FORMULA_STACK_GAP = Inches(0.22)
FORMULA_COL_MAX_WIDTH = Inches(6.6)
FORMULA_LONG_CHAR_THRESHOLD = 42  # len(latex) ≥ this → long defaults

# LibreOffice portable (AutoDL); export.py also falls back to PATH
LIBREOFFICE_PORTABLE = (
    "/root/autodl-tmp/tools/lo-portable/opt/libreoffice25.8/program/soffice"
)
