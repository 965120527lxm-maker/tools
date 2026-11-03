# tools/ppt — 共享 PPT 工具库

从 `fudan` / `SpatialEx` 脚本抽出的 **python-pptx** 公共层：主题、版式、SVG、公式、PDF 导出。浏览器幻灯片见 [`tools/web/`](../web/)。

**设计风格：简约学术式**；**文案纪律**：[`copy_discipline.md`](copy_discipline.md)（上屏禁路径/图号、takeaway、语言风格同源 `tools/writing`）。  
代理默认跟参考 Pipeline：  
[`pipelines/agent_deck.md`](pipelines/agent_deck.md)（规范总入口仍是 [`AGENTS.md`](AGENTS.md)）。

## 布局

```text
tools/ppt/
├── AGENTS.md      # 设计风格 + pipeline 摘要 + 文案纪律索引
├── copy_discipline.md  # 上屏文案 / takeaway / 语言风格（与 tools/writing 同源）
├── pipelines/     # Agent 参考流程（占位 → 列槽 → 检索 → 填槽）
├── theme.py       # 16:9、颜色、字体、公式默认尺寸
├── text.py        # run / paragraph 样式、关键字强调
├── layout.py      # 封面、章节页、标题、bullet、表格、页脚
├── figures.py     # 位图等比插入
├── formulas.py    # LaTeX → SVG（需 set_formula_dir）
├── svg.py         # python-pptx SVG 补丁
├── export.py      # LibreOffice → PDF
├── deck.py        # Deck / new_presentation
├── pages.py       # 组合版式（对比 / 表·图+结论 / 公式 / 背景·问题 / 四栏工作）
├── slots.py       # 图占位与填充（不搜图）
├── flowchart.py   # 原生方块流程图
├── agent_tools.py # Agent 可注册工具（fill/list slots）
├── templates/     # outline 模板
├── inventory.md   # 现有脚本盘点
└── examples/
    ├── minimal_deck.py
    ├── diffusion_outline.md
    └── generate_diffusion_intro_ppt.py
```

## 标准 Pipeline（Agent）

```text
outline.md
  → generate_*.py（图先 placeholder）→ draft.pptx
  → list_image_slots → Agent 检索 → fill_image_slots
  → 最终 pptx
```

详见 [`pipelines/agent_deck.md`](pipelines/agent_deck.md)；模板 [`templates/outline.template.md`](templates/outline.template.md)。

## 示例

```bash
# 冒烟
python /root/autodl-tmp/lxm/tools/ppt/examples/minimal_deck.py

# 组合版式（Diffusion Model 介绍）
python /root/autodl-tmp/lxm/tools/ppt/examples/generate_diffusion_intro_ppt.py
# → examples/diffusion_intro.pptx
```

或在项目脚本中：

```python
import sys
sys.path.insert(0, "/root/autodl-tmp/lxm")

from tools.ppt import Deck, add_bullet_box, set_formula_dir
from pptx.util import Inches

set_formula_dir("/path/to/formula_cache")  # 若用公式

deck = Deck(author="李熹鸣 · Week 1", total=10)
deck.cover("标题", footer_line="组会", date_line="2026-08")
deck.chapter(1, "背景", "一句副标题")
slide = deck.content("本周做了什么")
add_bullet_box(slide, ["要点一", "要点二"], top=Inches(1.5), height=Inches(4.5))
deck.save("out.pptx")
```

## 主题 palette

```python
from tools.ppt import set_palette
set_palette("academic")  # fudan 周报 / ST 调研（默认）
set_palette("defense")   # SpatialEx 答辩（更深蓝）
```

跨项目同进程导入时，每个脚本开头应显式 `set_palette(...)`，避免颜色串台。

## 与旧脚本关系

见 `inventory.md`：week1 / week2 / spatial / xenium / defense 均已接公共库；项目侧只留内容与图生成。

## 依赖

- `python-pptx`
- `Pillow`（插图）
- `matplotlib`（公式 SVG，可选）
- LibreOffice（`export_pdf`，可选；AutoDL 便携路径见 `theme.LIBREOFFICE_PORTABLE`）
