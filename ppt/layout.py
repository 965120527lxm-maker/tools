"""Slide layout primitives: cover, chapter, title, bullets, tables, footer."""

from __future__ import annotations

from copy import deepcopy

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE, MSO_SHAPE_TYPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt

from .text import apply_emphasis, set_shape_text, style_text_frame
from .theme import (
    ACCENT_ORANGE,
    COVER_BOTTOM,
    DARK_BLUE,
    DARK_GRAY,
    FONT_CN,
    FOOTER_GRAY,
    FS_BODY,
    FS_BODY_COMPACT,
    FS_CAPTION,
    FS_CHAPTER,
    FS_CHAPTER_LABEL,
    FS_CHAPTER_SUB,
    FS_COVER,
    FS_FOOTER,
    FS_HIGHLIGHT,
    FS_SECTION,
    FS_TABLE_BODY,
    FS_TABLE_HEADER,
    FS_TITLE,
    LIGHT_GRAY,
    LINE_SPACING_NORMAL,
    MEDIUM_GRAY,
    PALE_BLUE,
    SLIDE_HEIGHT,
    SLIDE_WIDTH,
    WHITE,
)


def set_slide_size(prs):
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT


def blank_slide(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])


def walk_shapes(shapes):
    for shape in shapes:
        yield shape
        if shape.shape_type == MSO_SHAPE_TYPE.GROUP:
            yield from walk_shapes(shape.shapes)


def add_footer(slide, page_num, total=None, left_text="", right_fmt=None):
    """Bottom bar: left_text + page number."""
    if right_fmt is None:
        right_fmt = f"{page_num} / {total}" if total else str(page_num)
    box = slide.shapes.add_textbox(Inches(11.5), Inches(7.05), Inches(1.5), Inches(0.35))
    p = box.text_frame.paragraphs[0]
    p.text = right_fmt
    p.font.size = Pt(FS_FOOTER)
    p.font.color.rgb = FOOTER_GRAY
    p.font.name = FONT_CN
    p.alignment = PP_ALIGN.RIGHT
    if left_text:
        nb = slide.shapes.add_textbox(Inches(0.6), Inches(7.05), Inches(3.0), Inches(0.35))
        p2 = nb.text_frame.paragraphs[0]
        p2.text = left_text
        p2.font.size = Pt(FS_FOOTER)
        p2.font.color.rgb = FOOTER_GRAY
        p2.font.name = FONT_CN


def add_title_shape(
    slide,
    text,
    top=Inches(0.4),
    height=Inches(0.85),
    left=Inches(0.6),
    width=Inches(12.0),
    font_size=FS_TITLE,
    bold=True,
    color=DARK_BLUE,
    align=PP_ALIGN.LEFT,
    add_underline=True,
):
    shape = slide.shapes.add_textbox(left, top, width, height)
    tf = shape.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.font.name = FONT_CN
    p.alignment = align
    p.space_after = Pt(6)

    if add_underline:
        line_y = top + height - Inches(0.12)
        line = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, left, line_y, width, Inches(0.035)
        )
        line.fill.solid()
        line.fill.fore_color.rgb = DARK_BLUE
        line.line.fill.background()
    return shape


def add_section_title(
    slide,
    text,
    top=Inches(1.45),
    left=Inches(0.6),
    width=Inches(12.0),
    height=Inches(0.7),
    font_size=FS_SECTION,
    color=DARK_BLUE,
    accent_color=ACCENT_ORANGE,
):
    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, left, top + Inches(0.12), Inches(0.08), Inches(0.45)
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = accent_color
    bar.line.fill.background()

    shape = slide.shapes.add_textbox(
        left + Inches(0.18), top, width - Inches(0.18), height
    )
    tf = shape.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.bold = True
    p.font.color.rgb = color
    p.font.name = FONT_CN
    p.alignment = PP_ALIGN.LEFT
    return shape


def add_bullet_box(
    slide,
    bullets,
    top=Inches(1.6),
    left=Inches(0.6),
    width=Inches(12.0),
    height=Inches(5.4),
    font_size=FS_BODY,
    color=DARK_GRAY,
    line_spacing=LINE_SPACING_NORMAL,
    bullet_levels=None,
    emphasize_words=None,
    card_background=False,
):
    if bullet_levels is None:
        bullet_levels = [0] * len(bullets)
    if emphasize_words is None:
        emphasize_words = []

    if card_background:
        card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            left - Inches(0.08),
            top - Inches(0.08),
            width + Inches(0.16),
            height + Inches(0.16),
        )
        card.fill.solid()
        card.fill.fore_color.rgb = LIGHT_GRAY
        card.line.fill.background()

    shape = slide.shapes.add_textbox(left, top, width, height)
    tf = shape.text_frame
    tf.word_wrap = True
    for i, bullet in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        text = bullet
        if not text.lstrip().startswith(("·", "•", "-", "–", "—")):
            text = ("•  " if bullet_levels[i] == 0 else "–  ") + text
        apply_emphasis(p, text, emphasize_words, color, ACCENT_ORANGE, font_size)
        p.space_before = Pt(6 if bullet_levels[i] == 0 else 0)
        p.space_after = Pt(8)
        p.level = bullet_levels[i]
        p.line_spacing = line_spacing
    return shape


def add_two_column_bullets(
    slide,
    left_title,
    left_bullets,
    right_title,
    right_bullets,
    top=Inches(1.5),
    height=Inches(4.8),
    font_size=FS_BODY_COMPACT,
):
    col_width = Inches(5.9)
    gap = Inches(0.6)
    add_section_title(
        slide, left_title, top=top, left=Inches(0.6), width=col_width,
        font_size=FS_SECTION, color=ACCENT_ORANGE,
    )
    add_bullet_box(
        slide, left_bullets, top=top + Inches(0.65),
        left=Inches(0.6), width=col_width, height=height, font_size=font_size,
    )
    add_section_title(
        slide, right_title, top=top,
        left=Inches(0.6) + col_width + gap, width=col_width,
        font_size=FS_SECTION, color=ACCENT_ORANGE,
    )
    add_bullet_box(
        slide, right_bullets, top=top + Inches(0.65),
        left=Inches(0.6) + col_width + gap, width=col_width,
        height=height, font_size=font_size,
    )


def add_highlight_block(
    slide,
    text,
    top=Inches(5.8),
    left=Inches(0.6),
    width=Inches(12.0),
    height=Inches(0.8),
    font_size=FS_HIGHLIGHT,
    color=DARK_BLUE,
    bg_color=PALE_BLUE,
    *,
    align=PP_ALIGN.CENTER,
):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.fill.background()
    tf = shape.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.bold = True
    p.font.color.rgb = color
    p.alignment = align
    p.space_before = Pt(0)
    p.space_after = Pt(0)
    return shape


def add_caption(
    slide,
    text,
    top=Inches(6.5),
    left=Inches(0.8),
    width=Inches(11.8),
    height=Inches(0.8),
    font_size=FS_CAPTION,
    color=DARK_BLUE,
):
    shape = slide.shapes.add_textbox(left, top, width, height)
    tf = shape.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.name = FONT_CN
    p.alignment = PP_ALIGN.LEFT
    return shape


def add_finding_box(
    slide,
    findings,
    top=Inches(1.6),
    left=Inches(0.6),
    width=Inches(12.0),
    height=Inches(5.4),
    font_size=FS_CAPTION,
    conclusion_color=DARK_GRAY,
    detail_color=MEDIUM_GRAY,
):
    """findings: list of (conclusion, detail)."""
    shape = slide.shapes.add_textbox(left, top, width, height)
    tf = shape.text_frame
    tf.word_wrap = True
    for i, (conclusion, detail) in enumerate(findings):
        p_conc = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p_conc.space_before = Pt(10 if i > 0 else 0)
        p_conc.space_after = Pt(2)
        p_conc.line_spacing = LINE_SPACING_NORMAL
        run_c = p_conc.add_run()
        run_c.text = conclusion
        run_c.font.bold = True
        run_c.font.size = Pt(font_size)
        run_c.font.color.rgb = conclusion_color
        run_c.font.name = FONT_CN

        p_detail = tf.add_paragraph()
        p_detail.space_before = Pt(0)
        p_detail.space_after = Pt(6)
        p_detail.line_spacing = LINE_SPACING_NORMAL
        run_d = p_detail.add_run()
        run_d.text = detail
        run_d.font.bold = False
        run_d.font.size = Pt(font_size - 1)
        run_d.font.color.rgb = detail_color
        run_d.font.name = FONT_CN
    return shape


def add_table(
    slide,
    headers,
    rows,
    top=Inches(1.4),
    left=Inches(0.6),
    width=Inches(12.0),
    font_size_header=FS_TABLE_HEADER,
    font_size_body=FS_TABLE_BODY,
    row_height_factor=0.55,
):
    n_rows = len(rows) + 1
    n_cols = len(headers)
    height = Inches(row_height_factor * n_rows)
    table = slide.shapes.add_table(n_rows, n_cols, left, top, width, height).table

    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = DARK_BLUE
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        p.font.color.rgb = WHITE
        p.font.bold = True
        p.font.size = Pt(font_size_header)
        p.font.name = FONT_CN
        p.alignment = PP_ALIGN.CENTER

    for r_idx, row in enumerate(rows):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx + 1, c_idx)
            cell.text = str(val)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(font_size_body)
            p.font.color.rgb = DARK_GRAY
            p.font.name = FONT_CN
            p.alignment = PP_ALIGN.CENTER
            if r_idx % 2 == 1:
                cell.fill.solid()
                cell.fill.fore_color.rgb = LIGHT_GRAY
    return table


def add_table_slide(
    slide,
    title,
    headers,
    rows,
    top=Inches(1.4),
    left=Inches(0.6),
    width=Inches(12.0),
    font_size_header=FS_TABLE_HEADER,
    font_size_body=FS_TABLE_BODY,
    row_height_factor=0.55,
):
    """Backward-compatible name used by fudan scripts."""
    if title:
        add_title_shape(slide, title, top=Inches(0.3), height=Inches(0.8), font_size=FS_TITLE)
    return add_table(
        slide, headers, rows, top=top, left=left, width=width,
        font_size_header=font_size_header, font_size_body=font_size_body,
        row_height_factor=row_height_factor,
    )


def add_simple_cover_slide(
    prs,
    title,
    footer_line="",
    date_line="",
):
    slide = blank_slide(prs)
    bg = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), SLIDE_WIDTH, SLIDE_HEIGHT
    )
    bg.fill.solid()
    bg.fill.fore_color.rgb = LIGHT_GRAY
    bg.line.fill.background()
    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(6.35), SLIDE_WIDTH, Inches(1.15)
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = COVER_BOTTOM
    bar.line.fill.background()
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(2.2), Inches(11.5), Inches(2.0))
    tf = title_box.text_frame
    tf.word_wrap = True
    tf.text = title
    style_text_frame(tf, font_size=FS_COVER, bold=True, color=DARK_BLUE)
    if footer_line:
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(6.55), Inches(11.5), Inches(0.45))
        footer_box.text_frame.text = footer_line
        style_text_frame(footer_box.text_frame, font_size=FS_CAPTION, color=WHITE)
    if date_line:
        date_box = slide.shapes.add_textbox(Inches(0.8), Inches(6.95), Inches(11.5), Inches(0.35))
        date_box.text_frame.text = date_line
        style_text_frame(date_box.text_frame, font_size=FS_CAPTION, color=WHITE)
    return slide


def copy_cover_from_template(
    prs,
    template_path,
    title,
    footer_line="",
    date_line="",
    fallback=True,
):
    """Copy first slide shapes from a template pptx (skip pictures), then patch text."""
    import os

    if not template_path or not os.path.exists(template_path):
        if fallback:
            return add_simple_cover_slide(prs, title, footer_line, date_line)
        raise FileNotFoundError(f"cover template missing: {template_path}")

    tpl = Presentation(template_path)
    tpl_slide = tpl.slides[0]
    slide = blank_slide(prs)

    for shape in tpl_slide.shapes:
        if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
            continue
        newel = deepcopy(shape.element)
        slide.shapes._spTree.insert_element_before(newel, "p:extLst")

    for shape in walk_shapes(slide.shapes):
        if not shape.has_text_frame:
            continue
        text = shape.text_frame.text
        if "学术汇报" in text or "Academic Statement" in text:
            set_shape_text(shape, title, font_size=FS_COVER, bold=True, color=DARK_BLUE)
        elif "TEL." in text or "MAIL." in text:
            set_shape_text(shape, footer_line, font_size=FS_CAPTION, bold=False, color=WHITE)
        elif "2026年" in text:
            set_shape_text(shape, date_line, font_size=FS_CAPTION, bold=False, color=WHITE)
    return slide


def add_chapter_divider(prs, number, title, subtitle=""):
    slide = blank_slide(prs)

    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_WIDTH, SLIDE_HEIGHT)
    bg.fill.solid()
    bg.fill.fore_color.rgb = DARK_BLUE
    bg.line.fill.background()

    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(2.7), Inches(0.12), Inches(1.4)
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = ACCENT_ORANGE
    bar.line.fill.background()

    num_box = slide.shapes.add_textbox(Inches(0.9), Inches(2.75), Inches(11.5), Inches(0.7))
    p = num_box.text_frame.paragraphs[0]
    p.text = f"Chapter {number}"
    p.font.size = Pt(FS_CHAPTER_LABEL)
    p.font.bold = True
    p.font.color.rgb = ACCENT_ORANGE
    p.font.name = FONT_CN

    title_box = slide.shapes.add_textbox(Inches(0.9), Inches(3.4), Inches(11.5), Inches(1.0))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(FS_CHAPTER)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.font.name = FONT_CN

    if subtitle:
        sub_box = slide.shapes.add_textbox(Inches(0.9), Inches(4.45), Inches(11.5), Inches(0.7))
        tf = sub_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = subtitle
        p.font.size = Pt(FS_CHAPTER_SUB)
        p.font.color.rgb = LIGHT_GRAY
        p.font.name = FONT_CN
    return slide


def content_slide(prs, title, page_num=None, total=None, footer_left=""):
    """Blank content page with title + optional footer."""
    slide = blank_slide(prs)
    add_title_shape(slide, title, font_size=FS_TITLE)
    if page_num is not None:
        add_footer(slide, page_num, total=total, left_text=footer_left)
    return slide


def add_divider_line(
    slide, top=Inches(5.0), left=Inches(0.6), width=Inches(12.0), color=DARK_BLUE,
):
    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, left, top, width, Inches(0.025)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = color
    line.line.fill.background()
    return line


def add_section_divider(slide, main_title, subtitle=""):
    """Chapter card used by SpatialEx defense: blue top bar + white title card."""
    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), SLIDE_WIDTH, Inches(1.2)
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = DARK_BLUE
    bar.line.fill.background()

    title_card = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(1.0), Inches(2.2), Inches(11.333), Inches(1.6),
    )
    title_card.fill.solid()
    title_card.fill.fore_color.rgb = WHITE
    title_card.line.fill.background()

    add_title_shape(
        slide, main_title,
        top=Inches(2.45), height=Inches(1.1), left=Inches(1.2), width=Inches(11.0),
        font_size=FS_COVER, bold=True, color=DARK_BLUE, align=PP_ALIGN.CENTER,
        add_underline=False,
    )
    if subtitle:
        add_title_shape(
            slide, subtitle,
            top=Inches(3.75), height=Inches(0.7), left=Inches(1.2), width=Inches(11.0),
            font_size=FS_SECTION, bold=False, color=ACCENT_ORANGE, align=PP_ALIGN.CENTER,
            add_underline=False,
        )
    return slide
