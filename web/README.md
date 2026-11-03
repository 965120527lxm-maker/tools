# tools/web — 共享 Web 工具库

浏览器端内容：**幻灯片**（`deck/`）、**本地预览**（`serve`）。与 `tools/ppt`（python-pptx）并列，不互相 import。

## 布局

```text
tools/web/
├── AGENTS.md
├── deck/              # WebDeck · KaTeX · Chart.js
├── serve.py           # 静态 HTTP 预览
├── examples/
│   └── minimal_deck.py
└── pipelines/
    └── deck.md
```

## 产物：文件夹，不是单个 HTML

Web deck 的交付单位是 **site 目录**（可 `serve` 的一整包），不是 lone `deck.html`：

```text
docs/progress/          ← 拷贝 / 下载 / 分享的是这一层
├── deck.html           ← 幻灯片
├── index.html          ← 可选：看板
├── data.json           ← 可选：图表数据
├── figures/            ← 幻灯片引用的图片
└── assets/             ← 可选：其它静态资源
```

- **相对路径图片**、页间链接（`deck.html` ↔ `index.html`）都依赖同一目录。
- 只有全部图片 `embed=True` 时才可以只要一个 HTML，但体积大，且 Chart.js/KaTeX 仍走 CDN。

打包 / 拷贝：

```bash
# 列出会带走哪些文件
python -m tools.web pack docs/progress --dry-run

# 拷贝整包到别处
python -m tools.web pack docs/progress /tmp/vec-progress

# 打成 tar.gz 发给别人
python -m tools.web pack docs/progress --archive vec-progress.tar.gz
```

解压后：`python -m tools.web serve vec-progress --open deck.html`

## 快速开始

```bash
# 最小 deck
python /root/autodl-tmp/lxm/tools/web/examples/minimal_deck.py

# 本地预览任意目录
python -m tools.web serve /path/to/site --port 8765 --open index.html
```

项目脚本中：

```python
import sys
sys.path.insert(0, "/root/autodl-tmp/lxm")

from tools.web.deck import WebDeck, bullets, tbl, takeaway

deck = WebDeck(document_title="My talk")
deck.cover('<div class="cover-inner"><h1>Title</h1></div>')
deck.slide("Overview", "Intro", bullets(["要点一", "要点二"]))
deck.save("docs/progress/deck.html")
```

## CLI

| 命令 | 说明 |
|------|------|
| `python -m tools.web serve [DIR]` | 启动静态文件服务（默认端口 8765） |
| `python -m tools.web pack SRC [DST]` | 拷贝 site 目录（html + figures/ + …） |
| `python -m tools.web pack SRC --archive FILE.tar.gz` | 打包为 tar.gz |
| `--open PATH` | 打印并可选 `--browser` 打开指定页面 |
| `--host 0.0.0.0` | 远程机器上供 AutoDL 端口映射访问 |

## 与 tools.ppt 关系

| 场景 | 工具 |
|------|------|
| 组会链接 / 分数刷新 | **tools.web.deck** |
| 归档 PDF / 正式 pptx | **tools.ppt** |

详见 [`pipelines/deck.md`](pipelines/deck.md)。

## 依赖

无 Python 第三方依赖（stdlib only）。浏览器端 CDN：KaTeX、Chart.js（deck 模板内嵌）。
