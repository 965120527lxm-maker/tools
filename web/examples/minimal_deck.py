#!/usr/bin/env python3
"""Minimal HTML deck built with tools/web/deck.

Run:
  python /root/autodl-tmp/lxm/tools/web/examples/minimal_deck.py
"""

from __future__ import annotations

import os
import sys

LXM_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, LXM_ROOT)

from tools.web.deck import (  # noqa: E402
    WebDeck,
    bullets,
    cover_inner,
    flow,
    formula_block,
    takeaway,
    tbl,
    twocol,
)

OUT = os.path.join(os.path.dirname(__file__), "minimal_deck.html")


def main() -> None:
    deck = WebDeck(document_title="Web Deck · tools.web.deck")
    deck.cover(
        cover_inner(
            "网页版幻灯片",
            "tools.web.deck · KaTeX + Chart.js",
            "lxm · 2026-08",
        )
    )

    deck.slide(
        "公共组件",
        "示例",
        twocol(
            "版式",
            ["封面 / 章节 / 内容页", "双栏 bullet", "表格 · 流程 · 公式"],
            "编辑方式",
            ["Python 里拼 HTML 片段", "运行 generate_*.py 生成 deck.html", "浏览器 ← → 翻页 · 点击文字直接改"],
        )
        + takeaway("项目脚本只保留内容；引擎与样式走 tools.web.deck。"),
    )

    deck.slide(
        "公式示例",
        "示例",
        formula_block(
            "正文 + display math，翻页时 KaTeX 自动渲染。",
            r"\hat{x} = x_{t_0} + \alpha\,\Delta_{\text{type}}",
        ),
    )

    deck.slide(
        "流程",
        "示例",
        flow(["outline.md", "generate_web_deck.py", "deck.html", "python -m tools.web serve"])
        + tbl(
            ["模块", "职责"],
            [
                ["web/deck/components.py", "tbl / bullets / formula / figure"],
                ["web/deck/deck.py", "WebDeck 收集与 save"],
                ["web/serve.py", "本地预览 HTTP 服务"],
            ],
        ),
    )

    fig_dir = os.path.join(os.path.dirname(__file__), "figures")
    sample_png = os.path.join(fig_dir, "sample_panel.png")
    if os.path.isfile(sample_png):
        from tools.web.deck import figure  # noqa: E402

        deck.slide(
            "图片示例",
            "示例",
            figure("figures/sample_panel.png", caption="相对路径 · 与 deck.html 同目录 serve")
            + takeaway("也可用 figure(..., embed=True) 嵌成单文件。"),
        )

    path = deck.save(OUT)
    print(f"saved: {path}")
    print(f"preview: python -m tools.web serve {os.path.dirname(OUT)} --open minimal_deck.html")


if __name__ == "__main__":
    main()
