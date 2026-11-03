"""Composed page layouts (简约学术式).

Each helper fills an existing content slide (title/footer already added),
or builds onto a blank slide that already has a title.
"""

from __future__ import annotations

from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt
from lxml import etree

from .figures import add_figure_on_slide
from .formulas import add_formula, add_formula_stack, render_latex, svg_aspect_ratio
from .layout import (
    add_bullet_box,
    add_caption,
    add_highlight_block,
    add_section_title,
    add_table,
    add_two_column_bullets,
)
from .slots import ImageSlot, add_image_placeholder, fill_image_slots
from .theme import (
    ACCENT_ORANGE,
    BLACK,
    DARK_BLUE,
    DARK_GRAY,
    FONT_CN,
    FS_BODY,
    FS_BODY_COMPACT,
    FS_CAPTION,
    FS_HIGHLIGHT,
    FS_SECTION,
    FS_TABLE_BODY,
    FS_TABLE_HEADER,
    LIGHT_GRAY,
    PALE_BLUE,
    PALE_ORANGE,
    SLIDE_WIDTH,
    WHITE,
)


def add_two_column_compare(
    slide,
    left_title: str,
    left_bullets: list[str],
    right_title: str,
    right_bullets: list[str],
    *,
    top=Inches(1.45),
    height=Inches(4.2),
    font_size=FS_BODY_COMPACT,
    note: str | None = None,
    vs_label: str = "vs",
):
    """双栏对比：左右标题+要点，中间轻量 vs 提示。"""
    add_two_column_bullets(
        slide, left_title, left_bullets, right_title, right_bullets,
        top=top, height=height, font_size=font_size,
    )
    # thin center tick — not a decorative badge
    mid = slide.shapes.add_textbox(Inches(6.25), top + Inches(2.0), Inches(0.85), Inches(0.4))
    p = mid.text_frame.paragraphs[0]
    p.text = vs_label
    p.font.size = Pt(FS_CAPTION)
    p.font.bold = True
    p.font.color.rgb = ACCENT_ORANGE
    p.font.name = FONT_CN
    p.alignment = PP_ALIGN.CENTER
    if note:
        add_highlight_block(
            slide, note, top=Inches(6.2), left=Inches(0.6),
            width=Inches(12.0), height=Inches(0.65), font_size=FS_CAPTION,
        )
    return slide


def add_table_with_conclusion(
    slide,
    headers: list[str],
    rows: list[list],
    conclusion: str | None = None,
    *,
    table_top=Inches(1.45),
    left=Inches(0.6),
    width=Inches(12.0),
    font_size_header=FS_TABLE_HEADER,
    font_size_body=FS_TABLE_BODY,
    row_height_factor=0.48,
    conclusion_top=Inches(6.15),
):
    """表格上 + 可选居中 takeaway（内容已足够清楚时可省略）。"""
    add_table(
        slide, headers, rows,
        top=table_top, left=left, width=width,
        font_size_header=font_size_header, font_size_body=font_size_body,
        row_height_factor=row_height_factor,
    )
    if conclusion:
        add_highlight_block(
            slide, conclusion, top=conclusion_top, left=left,
            width=width, height=Inches(0.7), font_size=FS_HIGHLIGHT,
        )
    return slide


def add_figure_with_conclusion(
    slide,
    img_path: str | None,
    conclusion: str | None = None,
    *,
    caption: str | None = None,
    slot_id: str = "main",
    fig_top=Inches(1.4),
    fig_height=Inches(4.2),
    left=Inches(0.6),
    width=Inches(12.0),
    conclusion_top=Inches(6.15),
) -> dict[str, ImageSlot]:
    """图片上 + 可选居中 takeaway。无图时先放占位，可用 fill_image_slots 填充。"""
    slots: dict[str, ImageSlot] = {}
    if img_path and __import__("os").path.exists(img_path):
        add_figure_on_slide(
            slide, img_path, left=left, top=fig_top,
            max_width=width, max_height=fig_height,
        )
    else:
        slots[slot_id] = add_image_placeholder(
            slide, left, fig_top, width, fig_height, slot_id,
            label=caption or "图示占位",
        )
    if caption and (img_path and __import__("os").path.exists(img_path)):
        add_caption(slide, caption, top=fig_top + fig_height + Inches(0.05),
                    left=left, width=width, font_size=FS_CAPTION)
    if conclusion:
        add_highlight_block(
            slide, conclusion, top=conclusion_top, left=left,
            width=width, height=Inches(0.7), font_size=FS_HIGHLIGHT,
        )
    return slots


def add_formula_derivation(
    slide,
    formulas: list[dict],
    bullets: list[str],
    *,
    note: str | None = None,
    formula_left=Inches(0.55),
    formula_top=Inches(1.4),
    bullet_left=Inches(7.1),
    bullet_width=Inches(5.6),
):
    """公式推导页：左侧公式栈，右侧要点，底部可选结论。"""
    add_formula_stack(slide, formulas, left=formula_left, top=formula_top)
    add_section_title(
        slide, "要点", top=formula_top, left=bullet_left,
        width=bullet_width, font_size=FS_SECTION, color=ACCENT_ORANGE,
    )
    add_bullet_box(
        slide, bullets, top=formula_top + Inches(0.55), left=bullet_left,
        width=bullet_width, height=Inches(4.0), font_size=FS_BODY_COMPACT,
    )
    if note:
        add_highlight_block(
            slide, note, top=Inches(6.15), left=Inches(0.55),
            width=Inches(12.2), height=Inches(0.7), font_size=FS_CAPTION,
        )
    return slide


def add_math_principle_page(
    slide,
    title: str,
    body: str,
    formula: str,
    *,
    note: str | None = None,
    title_top=Inches(1.35),
    body_top=Inches(2.05),
    formula_top=Inches(4.0),
    left=Inches(0.6),
    width=Inches(12.0),
    formula_height=None,
    formula_fontsize=None,
    body_font_size=FS_BODY,
    body_align=PP_ALIGN.LEFT,
):
    """数学书风格公式页：橘色标题 + 正文段落 + 居中公式 + 底部可选结论。

    参数:
        title: 橘色小标题，通常是一个短句，如“核心思想”。
        body: 正文段落，解释公式背后的直觉。
        formula: LaTeX 字符串（不要外层 $）。
        note: 底部高亮结论框，可选。
    """
    # 橘色标题：竖条与文字同为橘色
    add_section_title(
        slide, title, top=title_top, left=left, width=width,
        font_size=FS_SECTION, color=ACCENT_ORANGE, accent_color=ACCENT_ORANGE,
    )

    # 正文段落
    body_box = slide.shapes.add_textbox(left, body_top, width, Inches(1.7))
    tf = body_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = body
    p.font.size = Pt(body_font_size)
    p.font.color.rgb = DARK_GRAY
    p.font.name = FONT_CN
    p.alignment = body_align
    p.line_spacing = 1.2

    # 居中公式：先渲染，再根据实际宽度调整位置
    pic, formula_width, _ = add_formula(
        slide, formula, left=0, top=formula_top,
        height=formula_height, fontsize=formula_fontsize,
        max_width=Inches(11.0),
    )
    pic.left = int((SLIDE_WIDTH - formula_width) / 2)

    if note:
        add_highlight_block(
            slide, note, top=Inches(6.15), left=left,
            width=width, height=Inches(0.7), font_size=FS_CAPTION,
        )
    return slide


def add_theorem_formula_page(
    slide,
    label: str,
    statement: str,
    formula: str,
    *,
    interpretation: str | None = None,
    label_top=Inches(1.35),
    box_top=Inches(1.75),
    box_height=Inches(2.55),
    left=Inches(0.6),
    width=Inches(12.0),
    box_color=PALE_BLUE,
    formula_height=None,
    formula_fontsize=None,
):
    """定理框风格公式页：小标签 + 圆角框（陈述 + 居中公式）+ 框下解释。"""
    # 小标签，如“定义 / 定理 / 引理”
    label_box = slide.shapes.add_textbox(left, label_top, width, Inches(0.35))
    tf = label_box.text_frame
    p = tf.paragraphs[0]
    p.text = label
    p.font.size = Pt(FS_CAPTION)
    p.font.bold = True
    p.font.color.rgb = ACCENT_ORANGE
    p.font.name = FONT_CN

    # 定理框背景
    box = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, left, box_top, width, box_height,
    )
    box.fill.solid()
    box.fill.fore_color.rgb = box_color
    box.line.fill.background()

    # 框内陈述文字
    stmt_box = slide.shapes.add_textbox(
        left + Inches(0.3), box_top + Inches(0.22),
        width - Inches(0.6), Inches(0.55),
    )
    tf = stmt_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = statement
    p.font.size = Pt(FS_BODY)
    p.font.color.rgb = DARK_GRAY
    p.font.name = FONT_CN
    p.alignment = PP_ALIGN.LEFT

    # 框内居中公式
    pic, formula_width, _ = add_formula(
        slide, formula, left=0,
        top=box_top + Inches(0.95),
        height=formula_height, fontsize=formula_fontsize,
        max_width=Inches(11.0),
    )
    pic.left = int((SLIDE_WIDTH - formula_width) / 2)

    # 框下方解释
    if interpretation:
        interp_box = slide.shapes.add_textbox(
            left, box_top + box_height + Inches(0.25),
            width, Inches(1.25),
        )
        tf = interp_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = interpretation
        p.font.size = Pt(FS_BODY)
        p.font.color.rgb = DARK_GRAY
        p.font.name = FONT_CN
        p.alignment = PP_ALIGN.LEFT
        p.line_spacing = 1.2

    return slide


def add_formula_with_annotation(
    slide,
    title: str,
    formula: str,
    left_title: str,
    left_items: list[str],
    right_title: str,
    right_items: list[str],
    *,
    note: str | None = None,
    title_top=Inches(1.35),
    formula_top=Inches(2.05),
    columns_top=Inches(3.2),
    left=Inches(0.6),
    width=Inches(12.0),
    formula_height=None,
    formula_fontsize=None,
):
    """公式 + 双栏注释：顶部橘色标题 + 居中公式 + 下方左栏符号 / 右栏含义。"""
    add_section_title(
        slide, title, top=title_top, left=left, width=width,
        font_size=FS_SECTION, color=ACCENT_ORANGE, accent_color=ACCENT_ORANGE,
    )

    # 居中公式
    pic, formula_width, _ = add_formula(
        slide, formula, left=0, top=formula_top,
        height=formula_height, fontsize=formula_fontsize,
        max_width=Inches(11.5),
    )
    pic.left = int((SLIDE_WIDTH - formula_width) / 2)

    # 双栏
    col_width = Inches(5.9)
    gap = Inches(0.6)
    col_left = left
    col_right = left + col_width + gap

    add_section_title(
        slide, left_title, top=columns_top, left=col_left,
        width=col_width, font_size=FS_SECTION, color=DARK_BLUE,
    )
    add_bullet_box(
        slide, left_items, top=columns_top + Inches(0.55),
        left=col_left, width=col_width, height=Inches(2.6),
        font_size=FS_BODY_COMPACT,
    )

    add_section_title(
        slide, right_title, top=columns_top, left=col_right,
        width=col_width, font_size=FS_SECTION, color=DARK_BLUE,
    )
    add_bullet_box(
        slide, right_items, top=columns_top + Inches(0.55),
        left=col_right, width=col_width, height=Inches(2.6),
        font_size=FS_BODY_COMPACT,
    )

    if note:
        add_highlight_block(
            slide, note, top=Inches(6.15), left=left,
            width=width, height=Inches(0.7), font_size=FS_CAPTION,
        )
    return slide


def _add_horiz_line(slide, left, top, width, color=DARK_BLUE, thickness=Inches(0.025)):
    """画一条水平线（非表格场景下使用）。"""
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, thickness)
    line.fill.solid()
    line.fill.fore_color.rgb = color
    line.line.fill.background()
    return line


def _set_cell_border(cell, edge, *, color=None, sz=None, visible=True):
    """设置 PowerPoint 表格单元格单边边框（使用 a:lnT / a:lnB / a:lnL / a:lnR）。

    edge: 'top' | 'bottom' | 'left' | 'right'
    sz: 线宽，单位 EMU（12700 = 1pt）
    visible=False: 删除该边边框
    """
    edge_map = {"top": "lnT", "bottom": "lnB", "left": "lnL", "right": "lnR"}
    tag = edge_map[edge]
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    ln = tcPr.find(qn(f"a:{tag}"))

    if not visible:
        if ln is not None:
            tcPr.remove(ln)
        return

    if ln is None:
        ln = etree.SubElement(tcPr, qn(f"a:{tag}"))

    ln.set("w", str(sz))
    ln.set("cap", "flat")

    solidFill = ln.find(qn("a:solidFill"))
    if solidFill is None:
        solidFill = etree.SubElement(ln, qn("a:solidFill"))
        srgbClr = etree.SubElement(solidFill, qn("a:srgbClr"))
    else:
        srgbClr = solidFill.find(qn("a:srgbClr"))
        if srgbClr is None:
            srgbClr = etree.SubElement(solidFill, qn("a:srgbClr"))
    srgbClr.set("val", color)


def add_three_line_table(
    slide,
    headers: list[str],
    rows: list[list[str]],
    *,
    top=Inches(2.0),
    width=Inches(10.0),
    left=None,
    row_height=Inches(0.55),
    header_font_size=FS_TABLE_HEADER,
    body_font_size=FS_TABLE_BODY,
    line_color=BLACK,
    line_sz=25400,
    first_col_bold: bool = False,
    first_col_italic: bool = False,
    first_col_color=None,
    center_all: bool = False,
):
    """通用三线表：使用真正的表格，仅保留顶线、表头底线、底线。

    默认整体在页面水平居中（left=None 时自动计算）。
    返回字典，含 `table` 对象及数据行单元格坐标，方便调用方覆盖内容。
    """
    if left is None:
        left = int((SLIDE_WIDTH - width) / 2)

    n_rows = len(rows) + 1
    n_cols = len(headers)
    total_height = row_height * n_rows

    graphic_frame = slide.shapes.add_table(n_rows, n_cols, left, top, width, total_height)
    table = graphic_frame.table

    line_hex = str(line_color).replace("#", "").upper()

    # 填充表头
    for c, header in enumerate(headers):
        cell = table.cell(0, c)
        cell.fill.background()
        cell.text = header
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        p.font.bold = True
        p.font.size = Pt(header_font_size)
        p.font.color.rgb = BLACK
        p.font.name = FONT_CN
        p.alignment = PP_ALIGN.CENTER

    # 填充数据行
    for r_idx, row in enumerate(rows):
        padded = list(row) + [""] * (n_cols - len(row))
        for c_idx, text in enumerate(padded[:n_cols]):
            cell = table.cell(r_idx + 1, c_idx)
            cell.fill.background()
            cell.text = text
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(body_font_size)
            p.font.name = FONT_CN
            if c_idx == 0:
                p.alignment = PP_ALIGN.CENTER
                if first_col_bold:
                    p.font.bold = True
                if first_col_italic:
                    p.font.italic = True
                p.font.color.rgb = first_col_color if first_col_color else BLACK
            else:
                p.font.color.rgb = BLACK
                p.alignment = PP_ALIGN.CENTER if center_all else PP_ALIGN.LEFT

    # 隐藏所有边框
    for row in table.rows:
        for cell in row.cells:
            for edge in ("top", "left", "bottom", "right"):
                _set_cell_border(cell, edge, visible=False)

    # 顶线、表头底线、底线
    for cell in table.rows[0].cells:
        _set_cell_border(cell, "top", sz=line_sz, color=line_hex)
        _set_cell_border(cell, "bottom", sz=line_sz, color=line_hex)
    last_row = table.rows[len(table.rows) - 1]
    for cell in last_row.cells:
        _set_cell_border(cell, "bottom", sz=line_sz, color=line_hex)

    # 计算并返回单元格坐标
    cells = []
    table_left = graphic_frame.left
    table_top_pos = graphic_frame.top
    for r_idx in range(len(rows)):
        row_cells = []
        cell_top = table_top_pos + table.rows[0].height
        for rr in range(r_idx):
            cell_top += table.rows[rr + 1].height
        cell_left = table_left
        for c_idx in range(n_cols):
            cell_width = table.columns[c_idx].width
            cell_height = table.rows[r_idx + 1].height
            row_cells.append((cell_left, cell_top, cell_width, cell_height))
            cell_left += cell_width
        cells.append(row_cells)

    return {
        "table": table,
        "cells": cells,
        "table_left": table_left,
        "table_top": table_top_pos,
        "table_width": width,
        "table_height": total_height,
    }


def add_symbol_table(
    slide,
    rows: list[list[str]],
    *,
    table_top=Inches(2.0),
    width=Inches(10.0),
    left=None,
    row_height=Inches(0.55),
):
    """符号表版式：居中的三线表（符号 / 含义 / 可选备注）。

    无橘色小标题、无底部 takeaway。符号列若用 $...$ 包裹，会渲染为 LaTeX 公式图片。
    rows: 每行 2 或 3 个字符串；长度不足会自动补齐空单元格。
    """
    n_cols = max((len(row) for row in rows), default=2)
    n_cols = min(max(n_cols, 2), 3)
    headers = ["符号", "含义", "备注"][:n_cols]

    # 列宽比例：符号列固定，含义列占主要空间
    if n_cols == 2:
        col_ratios = [0.30, 0.70]
    else:
        col_ratios = [0.26, 0.54, 0.20]

    col_widths = [int(width * r) for r in col_ratios]
    col_widths[-1] += int(width) - sum(col_widths)

    # 准备数据：第一列先用空字符串占位，后续覆盖为公式图片
    placeholder_rows = []
    for row in rows:
        padded = list(row) + [""] * (n_cols - len(row))
        if padded[0].startswith("$") and padded[0].endswith("$"):
            padded[0] = " "
        placeholder_rows.append(padded[:n_cols])

    result = add_three_line_table(
        slide, headers, placeholder_rows,
        top=table_top, width=width, left=left, row_height=row_height,
    )
    table = result["table"]
    cells = result["cells"]

    # 对符号列的 LaTeX 项，清空单元格并插入渲染后的公式图片
    for r_idx, row in enumerate(rows):
        symbol_text = row[0] if len(row) > 0 else ""
        if not (symbol_text.startswith("$") and symbol_text.endswith("$")):
            cell = table.cell(r_idx + 1, 0)
            p = cell.text_frame.paragraphs[0]
            p.font.italic = True
            p.font.bold = True
            p.font.color.rgb = BLACK
            continue

        latex = symbol_text[1:-1]
        svg_path = render_latex(latex, fontsize=20)
        aspect = svg_aspect_ratio(svg_path)

        cell_left, cell_top, cell_width, cell_height = cells[r_idx][0]
        table.cell(r_idx + 1, 0).text = ""  # 清空占位空格
        max_h = cell_height - Inches(0.12)
        max_w = cell_width - Inches(0.3)
        h = max_h
        w = h * aspect
        if w > max_w:
            w = max_w
            h = w / aspect

        pic_left = int(cell_left + (cell_width - w) / 2)
        pic_top = int(cell_top + (cell_height - h) / 2)
        slide.shapes.add_picture(svg_path, pic_left, pic_top, width=w, height=h)

    return table


def add_background_page(
    slide,
    lead: str,
    bullets: list[str],
    *,
    note: str | None = None,
    top=Inches(1.4),
):
    """背景说明页：一句导语 + 要点列表。"""
    lead_box = slide.shapes.add_textbox(Inches(0.6), top, Inches(12.0), Inches(0.7))
    tf = lead_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = lead
    p.font.size = Pt(FS_SECTION)
    p.font.bold = True
    p.font.color.rgb = DARK_BLUE
    p.font.name = FONT_CN

    add_bullet_box(
        slide, bullets, top=top + Inches(0.85), left=Inches(0.6),
        width=Inches(12.0), height=Inches(3.8), font_size=FS_BODY,
    )
    if note:
        add_highlight_block(
            slide, note, top=Inches(6.15), left=Inches(0.6),
            width=Inches(12.0), height=Inches(0.7), font_size=FS_CAPTION,
        )
    return slide


def add_problem_page(
    slide,
    question: str,
    challenges: list[str],
    *,
    goal: str | None = None,
    top=Inches(1.4),
):
    """问题说明页：核心问题 + 难点列表 + 可选目标句。"""
    q_card = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(0.6), top, Inches(12.0), Inches(1.15),
    )
    q_card.fill.solid()
    q_card.fill.fore_color.rgb = PALE_ORANGE
    q_card.line.fill.background()
    q_box = slide.shapes.add_textbox(Inches(0.85), top + Inches(0.25), Inches(11.5), Inches(0.75))
    tf = q_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = question
    p.font.size = Pt(FS_SECTION)
    p.font.bold = True
    p.font.color.rgb = DARK_BLUE
    p.font.name = FONT_CN

    add_section_title(
        slide, "难点", top=top + Inches(1.4), left=Inches(0.6),
        width=Inches(12.0), font_size=FS_SECTION, color=ACCENT_ORANGE,
    )
    add_bullet_box(
        slide, challenges, top=top + Inches(1.95), left=Inches(0.6),
        width=Inches(12.0), height=Inches(2.8), font_size=FS_BODY,
    )
    if goal:
        add_highlight_block(
            slide, goal, top=Inches(6.15), left=Inches(0.6),
            width=Inches(12.0), height=Inches(0.7), font_size=FS_HIGHLIGHT,
        )
    return slide


def add_prior_work_grid(
    slide,
    items: list[dict],
    *,
    top=Inches(1.35),
    n_cols: int = 4,
    note: str | None = None,
) -> dict[str, ImageSlot]:
    """现有工作页：多栏（默认四栏），每栏标题 + 图占位 + 短注。

    items: list of dicts with keys:
      - title (str)
      - caption (str, optional short note under image)
      - slot (str, optional; default work0..)
      - image (str path, optional; if present, fill immediately)

    Returns slot map for fill_image_slots.
    """
    if not items:
        return {}
    n_cols = min(n_cols, len(items), 4)
    margin = Inches(0.55)
    gap = Inches(0.22)
    usable = Inches(12.2)
    col_w = int((usable - gap * (n_cols - 1)) / n_cols)
    img_h = Inches(2.55)
    slots: dict[str, ImageSlot] = {}

    for i, item in enumerate(items[:n_cols]):
        left = margin + i * (col_w + gap)
        title = item.get("title", f"工作 {i + 1}")
        caption = item.get("caption", "")
        slot_id = item.get("slot", f"work{i}")
        img_path = item.get("image")

        # column title bar
        hdr = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, left, top, col_w, Inches(0.42),
        )
        hdr.fill.solid()
        hdr.fill.fore_color.rgb = DARK_BLUE
        hdr.line.fill.background()
        ht = hdr.text_frame
        ht.word_wrap = True
        hp = ht.paragraphs[0]
        hp.text = title
        hp.font.size = Pt(FS_CAPTION)
        hp.font.bold = True
        hp.font.color.rgb = WHITE
        hp.font.name = FONT_CN
        hp.alignment = PP_ALIGN.CENTER

        img_top = top + Inches(0.55)
        if img_path and __import__("os").path.exists(img_path):
            add_figure_on_slide(
                slide, img_path, left=left, top=img_top,
                max_width=col_w, max_height=img_h,
            )
            slots[slot_id] = ImageSlot(slot_id, left, img_top, col_w, img_h, title)
        else:
            slots[slot_id] = add_image_placeholder(
                slide, left, img_top, col_w, img_h, slot_id,
                label=item.get("placeholder", "待填图"),
            )

        if caption:
            add_caption(
                slide, caption,
                top=img_top + img_h + Inches(0.08),
                left=left, width=col_w, height=Inches(0.85),
                font_size=FS_CAPTION, color=DARK_GRAY,
            )

    if note:
        add_highlight_block(
            slide, note, top=Inches(6.2), left=Inches(0.55),
            width=Inches(12.2), height=Inches(0.6), font_size=FS_CAPTION,
        )
    return slots


# re-export fill helper for callers that import pages
fill_prior_work_images = fill_image_slots
