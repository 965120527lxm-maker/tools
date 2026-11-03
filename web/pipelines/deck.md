# Web Deck Pipeline

浏览器幻灯片：单文件 `deck.html`，← → 翻页、KaTeX 公式、可选 Chart.js。与 `tools/ppt`（python-pptx）**并列**，共用 outline 与 [`tools/ppt/copy_discipline.md`](../ppt/copy_discipline.md) 文案纪律。

## 布局

```text
tools/web/
├── deck/           # WebDeck 引擎
│   ├── components.py
│   ├── deck.py
│   ├── render.py
│   └── charts.py
├── serve.py        # 本地静态预览
├── examples/
└── pipelines/
```

## Pipeline

```text
outline.md
    → generate_*_web.py / build_deck_html.py
    → deck.html
    → python -m tools.web serve docs/progress --open deck.html
    → python -m tools.web pack docs/progress --archive site.tar.gz   # 分享整包
```

交付物是 **site 目录**，不是 lone `deck.html`（见 [`README.md`](../README.md) §产物）。

### 写内容（项目侧）

```python
from tools.web.deck import WebDeck, bullets, tbl, takeaway, chart_box, line_chart

deck = WebDeck(document_title="My talk", nav_links=[("Dashboard", "index.html")])
deck.cover('<div class="cover-inner"><h1>Title</h1></div>')
deck.slide("Overview", "Intro", bullets(["A", "B"]) + takeaway("一句结论"))
deck.save("docs/progress/deck.html", charts={"chart-1": line_chart(...)} )
```

### 图片

三种方式，按场景选一种：

| 方式 | 适用 | 写法 |
|------|------|------|
| **相对路径** | 与 `deck.html` 同站点 serve（推荐） | `figure("figures/heatmap.png", caption="…")` |
| **绝对 URL** | 图已在 CDN / 图床 | `figure("https://…/a.png")` |
| **embed** | 单文件、离线拷贝 | `figure(path, embed=True)` 或 `image_src(path, embed=True)` |

约定：

- 静态资源放在 `deck.html` 同级或子目录，例如 `docs/progress/figures/`
- caption 写**内容描述**，不写 `Fig. 1` / 本地路径（同 [`copy_discipline.md`](../../ppt/copy_discipline.md)）
- 双栏图：`figure_row(["a.png", "b.png"], ["左说明", "右说明"])`
- 图 + bullet：`figure_with_text("a.png", ["要点…"], side="left")`

```python
from tools.web.deck import figure, figure_row, image_src

deck.slide(
    "结果示意",
    "实验",
    figure("figures/t1_variogram.png", caption="variogram 与榜首差距")
    + takeaway("结构 metric 仍是 T1 主缺口"),
)

# 单文件 deck（体积会变大）
deck.slide("附录", "补充", figure("/abs/path/plot.png", embed=True))
```

### 可编辑文案（默认开启）

- `WebDeck(editable=True)`：bullet / 表格 / takeaway / 页标题等渲染为**无框线**可编辑区域
- 表格单元格 → `<input class="deck-edit">`；段落 / bullet → `contenteditable`
- **PPT 式文本框**：单击选中（八向锚点）→ 拖动移动 → 双击进入文字编辑 → Esc 退出；Ctrl/Shift+点击多选
- 方向键 **1px** 微调（Shift **10px**）；**Ctrl+Z / Ctrl+Y** 撤销重做（文字编辑时走浏览器 undo）
- 关闭：`WebDeck(editable=False)` 或 `build_vec_deck(data, editable=False)`

### 图表（Chart.js）

- 正文：`chart_box("chart-composite")` — 一页可放多个 canvas，翻页时自动初始化
- 旧写法 `deck.slide(..., chart="chart-composite")` 仍可用；推荐仅 `chart_box` + `charts` dict key 一致
- 折线 / 柱状 / 散点扫参：`line_chart` · `bar_*` · `scatter_line` · `pie_chart`（见 `deck/charts.py`）

### 与 pptx 双轨

```text
scripts/generate_week5_ppt.py   → docs/ppt/VEC_Week5.pptx   (tools.ppt)
scripts/build_deck_html.py      → docs/progress/deck.html   (tools.web.deck)
```

## 验收

1. 页序与 outline Part 2 一致  
2. 数字与 Part 1 一致（路径不进 slide 字符串）  
3. 公式页 KaTeX 正常  
4. 含 chart 的页首次进入时图表出现  
5. 过 copy_discipline §5 自检  
