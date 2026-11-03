#!/usr/bin/env python3
"""Minimal deck built with lxm/tools/ppt.

Run from anywhere:
  python /root/autodl-tmp/lxm/tools/ppt/examples/minimal_deck.py
"""

from __future__ import annotations

import os
import sys

LXM_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, LXM_ROOT)

from pptx.util import Inches  # noqa: E402

from tools.ppt import (  # noqa: E402
    Deck,
    add_bullet_box,
    add_highlight_block,
    add_table,
    set_palette,
)

set_palette("academic")

OUT = os.path.join(os.path.dirname(__file__), "minimal_deck.pptx")


def main():
    deck = Deck(author="lxm/tools/ppt", total=3)
    deck.cover(
        "PPT 工具最小示例",
        footer_line="tools.ppt · Deck API",
        date_line="2026-08",
    )
    deck.chapter(1, "公共库能力", "封面 · 章节页 · 内容页 · 表格")

    slide = deck.content("本页用公共组件拼装")
    add_bullet_box(
        slide,
        [
            "theme: 16:9 深蓝 + 橙色学术主题",
            "layout: 标题 / 章节页 / bullet / 高亮块 / 页脚",
            "svg: python-pptx 原生 SVG 插入补丁",
            "export: LibreOffice 转 PDF（可选）",
        ],
        top=Inches(1.4),
        height=Inches(3.2),
        font_size=18,
    )
    add_table(
        slide,
        ["模块", "职责"],
        [
            ["theme.py", "颜色 / 字体 / 画布"],
            ["layout.py", "版式组件"],
            ["formulas.py", "LaTeX → SVG"],
            ["deck.py", "Deck 工厂"],
        ],
        top=Inches(4.7),
        left=Inches(0.6),
        width=Inches(12.0),
        font_size_header=14,
        font_size_body=13,
        row_height_factor=0.38,
    )
    add_highlight_block(
        slide,
        "项目脚本只保留内容；版式与主题走 tools.ppt。",
        top=Inches(6.55),
        height=Inches(0.4),
        font_size=14,
    )

    path = deck.save(OUT)
    print(f"saved: {path}")


if __name__ == "__main__":
    main()
