# tools/web · Agent Guide

本目录是共享 **Web 内容** 工具库，与 `tools/ppt`（python-pptx）**独立**。代理写浏览器幻灯片、本地 HTML 预览时，以本文为准。

---

## 1. 模块

| 路径 | 职责 |
|------|------|
| `deck/` | `WebDeck`、版式组件（tbl / bullets / formula / flow / chart_box）、Chart.js helper |
| `serve.py` | 本地静态 HTTP 服务 |
| `pipelines/deck.md` | 幻灯片 pipeline |
| `examples/minimal_deck.py` | 冒烟示例 |

**不要**把 deck 引擎放进 `tools/ppt/`；pptx 与 web 共用 outline / 文案纪律，但代码分轨。

---

## 1.5 产物模型：site 目录

| pptx | web deck |
|------|----------|
| 单文件 `deck.pptx`（图内嵌） | **目录** `site/`：`deck.html` + `figures/` + 可选 `index.html` / `data.json` |

分享 / 备份 / 下载 = **cp 或 pack 整个目录**，不是只拷 `deck.html`。

```bash
python -m tools.web pack docs/progress --dry-run
python -m tools.web pack docs/progress /tmp/out
```

单文件 HTML 仅在有 `embed=True` 且无相对资源时可行；默认 workflow 按目录设计。

---

## 2. Web Deck（`deck/`）

### 做什么

- 16:9 浏览器幻灯片，← → / 空格翻页，F 全屏
- KaTeX 公式（翻页时 render）
- 默认 **editable**：PPT 式文本框（选中/拖动/缩放/双击编辑）；localStorage + 导出 JSON
- 可选 Chart.js（canvas id = charts dict key）
- 图片：`figure()` / `figure_row()` / `figure_with_text()`；相对路径、URL 或 `embed=True`
- 简约学术风格（与 ppt 视觉同源：深蓝 + 白底 slide）

### 项目侧写法

```python
sys.path.insert(0, "/root/autodl-tmp/lxm")  # 或项目内等价路径
from tools.web.deck import WebDeck, bullets, tbl, takeaway, chart_box, line_chart
```

- 内容留在项目 `generate_*_web.py` / `build_deck_html.py`
- **禁止**复制 HTML/CSS/翻页 JS 到项目里
- 上屏文案遵守 [`tools/ppt/copy_discipline.md`](../ppt/copy_discipline.md)

### 预览

```bash
python -m tools.web serve docs/progress --open deck.html
```

AutoDL 远程： `--host 0.0.0.0`，用实例端口映射访问。

---

## 3. Serve

```bash
python -m tools.web serve [DIR] [--port 8765] [--open PATH] [--browser]
```

项目可封装一键脚本（build + serve），但 HTTP 服务应走 `tools.web.serve`。

---

## 4. 与 tools.ppt 分工

| 产物 | 库 | 项目脚本 |
|------|-----|----------|
| `.pptx` | `tools.ppt` | `generate_*_ppt.py` |
| `deck.html` | `tools.web.deck` | `build_deck_html.py` |
| outline | 共用 | `docs/ref/*_outline.md` |

---

## 5. 改库时注意

- 新 slide 组件加进 `deck/components.py`，不要在业务脚本开旁路
- 主题/CSS 改 `deck/render.py` 模板一处
- 人类可读总览见 `README.md`
