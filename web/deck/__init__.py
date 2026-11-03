"""Browser slide deck — KaTeX formulas + optional Chart.js charts."""

from .charts import bar_horizontal, bar_vertical, line_chart, pie_chart, scatter_line
from .components import (
    bullets,
    chart_box,
    cover_inner,
    esc,
    figure,
    figure_row,
    figure_with_text,
    flow,
    formula_block,
    image_src,
    note,
    set_editable,
    takeaway,
    tbl,
    twocol,
)
from .deck import WebDeck, load_json_charts

__all__ = [
    "WebDeck",
    "load_json_charts",
    "esc",
    "tbl",
    "bullets",
    "takeaway",
    "twocol",
    "flow",
    "formula_block",
    "chart_box",
    "figure",
    "figure_row",
    "figure_with_text",
    "image_src",
    "cover_inner",
    "note",
    "set_editable",
    "line_chart",
    "scatter_line",
    "pie_chart",
    "bar_vertical",
    "bar_horizontal",
]
