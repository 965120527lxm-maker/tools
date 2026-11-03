"""Shared PPT toolkit for lxm projects (python-pptx).

Typical usage::

    from tools.ppt import Deck, add_bullet_box, add_highlight_block

    deck = Deck(author="李熹鸣 · Week 1", total=5)
    deck.cover("标题", footer_line="组会汇报", date_line="2026-08")
    slide = deck.content("本周进展")
    add_bullet_box(slide, ["第一点", "第二点"], top=Inches(1.5), height=Inches(4.5))
    deck.save("out.pptx")
"""

from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

from .theme import (
    SLIDE_WIDTH,
    SLIDE_HEIGHT,
    DARK_BLUE,
    ACCENT_ORANGE,
    COVER_BOTTOM,
    LIGHT_GRAY,
    PALE_BLUE,
    PALE_ORANGE,
    DARK_GRAY,
    MEDIUM_GRAY,
    WHITE,
    BLACK,
    FONT_CN,
    FS_COVER,
    FS_CHAPTER,
    FS_TITLE,
    FS_SECTION,
    FS_BODY,
    FS_BODY_COMPACT,
    FS_HIGHLIGHT,
    FS_CAPTION,
    FS_TABLE_HEADER,
    FS_TABLE_BODY,
    FS_FOOTER,
    FS_FLOW,
    FORMULA_DEFAULT_FONTSIZE,
    FORMULA_DEFAULT_HEIGHT,
    FORMULA_LONG_FONTSIZE,
    FORMULA_LONG_HEIGHT,
    FORMULA_STACK_GAP,
    FORMULA_COL_MAX_WIDTH,
    FORMULA_LONG_CHAR_THRESHOLD,
    set_palette,
    PALETTES,
)
from .svg import apply_pptx_svg_support, _svg_viewport_px_size
from .text import style_run, style_paragraph, style_text_frame, set_shape_text, apply_emphasis
from .layout import (
    set_slide_size,
    blank_slide,
    walk_shapes,
    add_footer,
    add_title_shape,
    add_section_title,
    add_bullet_box,
    add_two_column_bullets,
    add_highlight_block,
    add_caption,
    add_finding_box,
    add_table,
    add_table_slide,
    add_simple_cover_slide,
    copy_cover_from_template,
    add_chapter_divider,
    content_slide,
    add_divider_line,
    add_section_divider,
)
from .figures import add_figure_on_slide
from .formulas import (
    set_formula_dir,
    get_formula_dir,
    render_latex,
    svg_aspect_ratio,
    add_formula,
    add_formula_stack,
    add_method_formulas_slide,
)
from .slots import (
    ImageSlot,
    add_image_placeholder,
    fill_image_slots,
    fill_image_slots_pptx,
    list_image_slots,
    slots_to_json,
)
from .agent_tools import get_agent_tools, call_agent_tool
from .flowchart import (
    add_flow_box,
    add_h_arrow,
    add_v_arrow,
    add_flowchart_row,
    add_flowchart,
)
from .pages import (
    add_two_column_compare,
    add_table_with_conclusion,
    add_figure_with_conclusion,
    add_formula_derivation,
    add_math_principle_page,
    add_theorem_formula_page,
    add_formula_with_annotation,
    add_three_line_table,
    add_symbol_table,
    add_background_page,
    add_problem_page,
    add_prior_work_grid,
    fill_prior_work_images,
)
from .export import find_soffice, export_pdf
from .deck import new_presentation, Deck

# Aliases matching older fudan script private names
_style_run = style_run
_style_paragraph = style_paragraph
_style_text_frame = style_text_frame
_set_shape_text = set_shape_text
_apply_emphasis = apply_emphasis
_walk_shapes = walk_shapes
_svg_aspect_ratio = svg_aspect_ratio
_find_soffice = find_soffice

__all__ = [
    "Inches",
    "Pt",
    "RGBColor",
    "PP_ALIGN",
    "MSO_ANCHOR",
    "MSO_SHAPE",
    "SLIDE_WIDTH",
    "SLIDE_HEIGHT",
    "DARK_BLUE",
    "ACCENT_ORANGE",
    "COVER_BOTTOM",
    "LIGHT_GRAY",
    "PALE_BLUE",
    "PALE_ORANGE",
    "DARK_GRAY",
    "MEDIUM_GRAY",
    "WHITE",
    "BLACK",
    "FONT_CN",
    "FS_COVER",
    "FS_CHAPTER",
    "FS_TITLE",
    "FS_SECTION",
    "FS_BODY",
    "FS_BODY_COMPACT",
    "FS_HIGHLIGHT",
    "FS_CAPTION",
    "FS_TABLE_HEADER",
    "FS_TABLE_BODY",
    "FS_FOOTER",
    "FS_FLOW",
    "set_palette",
    "PALETTES",
    "FORMULA_DEFAULT_FONTSIZE",
    "FORMULA_DEFAULT_HEIGHT",
    "FORMULA_LONG_FONTSIZE",
    "FORMULA_LONG_HEIGHT",
    "FORMULA_STACK_GAP",
    "FORMULA_COL_MAX_WIDTH",
    "FORMULA_LONG_CHAR_THRESHOLD",
    "apply_pptx_svg_support",
    "_svg_viewport_px_size",
    "set_slide_size",
    "blank_slide",
    "add_footer",
    "add_title_shape",
    "add_section_title",
    "add_bullet_box",
    "add_two_column_bullets",
    "add_highlight_block",
    "add_caption",
    "add_finding_box",
    "add_table",
    "add_table_slide",
    "add_simple_cover_slide",
    "copy_cover_from_template",
    "add_chapter_divider",
    "content_slide",
    "add_divider_line",
    "add_section_divider",
    "add_figure_on_slide",
    "set_formula_dir",
    "render_latex",
    "add_formula",
    "add_formula_stack",
    "add_method_formulas_slide",
    "ImageSlot",
    "add_image_placeholder",
    "fill_image_slots",
    "fill_image_slots_pptx",
    "list_image_slots",
    "slots_to_json",
    "get_agent_tools",
    "call_agent_tool",
    "add_flow_box",
    "add_h_arrow",
    "add_v_arrow",
    "add_flowchart_row",
    "add_flowchart",
    "add_two_column_compare",
    "add_table_with_conclusion",
    "add_figure_with_conclusion",
    "add_formula_derivation",
    "add_math_principle_page",
    "add_theorem_formula_page",
    "add_formula_with_annotation",
    "add_three_line_table",
    "add_symbol_table",
    "add_background_page",
    "add_problem_page",
    "add_prior_work_grid",
    "fill_prior_work_images",
    "export_pdf",
    "new_presentation",
    "Deck",
]
