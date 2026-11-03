# tools/ppt · Agent Guide

本目录是共享 **python-pptx** 工具库。代理改版式、写 `generate_*.py`、或据 outline 出 PPT 时，以本文为准。

浏览器幻灯片见独立库 **[`tools/web/`](../web/)**（`tools.web.deck`），不与本目录混放。

远程：`git@github.com:965120527lxm-maker/ppt.git`（本目录可为独立 git 仓库）

**Web Deck**（浏览器幻灯片）：[`tools/web/`](../web/) · `from tools.web.deck import WebDeck, ...`

**后续方向**（根 `todo.md` §5，未开工）：用 TeX（如 Beamer）做幻灯/文档，与 `tools/pandoc-pdf` 共享字体与版式；本库在收敛前仍是默认 pptx 路径。

---

## 1. 设计风格：简约学术式

少装饰、多留白、信息优先；像组会/答辩学术幻灯，不像营销模板。  
`set_palette("defense")` 只换色相，不换疏密与装饰强度。

### 做什么

| 维度 | 约定                                                                  |
| ---- | --------------------------------------------------------------------- |
| 画布 | 16:9；安全边距约 0.6"                                                 |
| 色彩 | 深青/深蓝主色 + 一点橙色强调；灰白底；色块少而稳                      |
| 字体 | 中文衬线/仿宋系标题（如华文中宋）；字号统一走 `theme.FS_*`：标题 28、小节 20、正文 18、紧凑 16、底栏结论 15、注释 14；公式默认高约 0.78"、matplotlib 字号 26（长式 22，按字符数自动） |
| 结构 | 封面 / 章节页 / 内容页分工清楚；一页一事                              |
| 文字 | 短句、少层级；bullet 宜少不宜密                                       |
| 表格 | 表头底色即可；行数宜 ≤6                                               |
| 图   | 等比、不拉伸；自绘图 flat；caption 写**内容描述**，不写 Fig./Table 编号 |
| 页脚 | 轻量：汇报人 + 页码，不抢内容                                         |
| 文案 | 上屏禁路径/图号/DOI/命令；takeaway 可选且居中 — 见 [`copy_discipline.md`](copy_discipline.md) |

### 不做什么

- 渐变炫光、玻璃拟态、大圆角卡片墙、emoji 标题
- 无故加粗整段、多色强调词堆叠
- 为「好看」叠透明贴纸、浮动徽章
- 一页塞满多栏互抢的正文块（易重叠、难读）
- **上屏**写本地路径、`Fig.1` / `Table 5`、DOI、shell 命令（见 [`copy_discipline.md`](copy_discipline.md) §2）
- 正文已清楚仍堆底部 takeaway；或 takeaway 左对齐（应用 `add_highlight_block` 默认居中）
- slide 套话腔：值得注意的是、赋能、不是 A 而是 B、无数据「全面更好」（见 [`copy_discipline.md`](copy_discipline.md) §4）

### 与代码

- `theme.py`：色彩与字号（`FS_*` / `FORMULA_*`；改尺寸只改这里）
- `layout.py`：标题下划线、橙色细条、章节深色底——点缀有限
- `pages.py`：组合版式（双栏对比、表/图+结论、公式推导、背景/问题页、现有工作多栏）
- `slots.py`：图占位；**不搜图**。Agent 检索到合适本地图后，用注册工具 `fill_image_slots` 按 `{slot_id: path}` 填入
- `agent_tools.py`：给 Agent 注册的薄工具表（`get_agent_tools` / `call_agent_tool`）；无扫目录逻辑
- `flowchart.py`：原生方块 + 箭头流程图（`add_flow_box` / `add_flowchart_row` / `add_flowchart`）
- 文字重叠：目前靠固定坐标与间距约定；新增自动排布时以「留白优先」验收
- Palette：`academic`（默认）/ `defense`（更深蓝，仍简约学术）

### 组合版式（`pages`）

| 函数 | 用途 |
|------|------|
| `add_two_column_compare` | 双栏对比 |
| `add_table_with_conclusion` | 表格上 + 结论下 |
| `add_figure_with_conclusion` | 图片上 + 结论下（可先占位） |
| `add_formula_derivation` | 公式推导页（左公式 / 右要点） |
| `add_math_principle_page` | 数学书风格公式页（橘色标题 / 正文 / 居中公式 / 结论） |
| `add_theorem_formula_page` | 定理框风格公式页（标签 / 定理框 / 居中公式 / 解释） |
| `add_formula_with_annotation` | 公式 + 双栏注释（居中公式 / 左符号 / 右含义） |
| `add_three_line_table` | 通用三线表（居中 / 顶线+表头底线+底线） |
| `add_symbol_table` | 符号表版式（基于三线表 / 符号可渲染 LaTeX） |
| `add_background_page` | 背景说明页 |
| `add_problem_page` | 问题说明页 |
| `add_prior_work_grid` | 现有工作多栏（默认四栏，图先占位） |
| `fill_image_slots` | Agent 工具：显式 path map 填槽（不扫描） |
| `list_image_slots` | Agent 工具：列出 pptx 里已有 `slot:id` |
| `add_flow_box` / `add_flowchart` | PPT 原生方块流程图 |

示例：`examples/generate_diffusion_intro_ppt.py`（大纲 `examples/diffusion_outline.md`）

### 空白填充（渲染审查 + 按出处补内容）

出 draft 后必经一步：`export_pdf` → `pdftoppm` → `montage` 全页网格审查，
空白过半的页用**有出处的内容**填充。常用填充件速查：

| 填充件 | 适合填什么 |
|--------|-----------|
| `add_table` | 映射/角色表、实验矩阵、里程碑（≤6 行）；量少时可拉伸 `width`/`row_height_factor`、上调 `font_size_body` |
| `add_bullet_box` | 选型理由、QC 数字、预期假设等说明文字 |
| `add_two_column_compare` | 双栏对照（`vs_label=""` 去掉中间标） |
| `add_flowchart_row` | 流程图（原生方块，不用找图） |
| `add_highlight_block` | 页底 takeaway（**可选**；正文已清楚则省略；出现时**居中**） |
| `add_image_placeholder` | 图待产出时的占位（进 slot 清单） |

原则：不凑字、不塞无关图、不堆装饰。完整流程见
[`pipelines/agent_deck.md`](pipelines/agent_deck.md) Step ③。

### Agent 填图工具（已注册）

分工：**检索/选型在 Agent**；**库只负责按 map 落图**。

```bash
# 看有哪些槽
python -m tools.ppt list_image_slots --pptx path/to/deck.pptx

# 你选定路径后填充（JSON map，不自动找图）
python -m tools.ppt fill_image_slots --pptx path/to/deck.pptx \
  --paths '{"ddpm":"/abs/a.png","ddim":"/abs/b.png"}'

# 导出可挂到 MCP / harness 的 schema
python -m tools.ppt dump_registry
```

库内：`from tools.ppt import get_agent_tools, call_agent_tool`。

---

## 1.5 文案纪律（与视觉并列）

上屏文字、takeaway、语言风格的全文：**[`copy_discipline.md`](copy_discipline.md)**。摘要：

| 维度 | 纪律 |
|------|------|
| **分层** | 路径 / 图号 / 命令 → outline Part 1、脚本常量、填槽 map；**不进 slide 字符串** |
| **上屏禁入** | 本地路径、`Fig.*` / `Table *`、DOI、PDF 名、shell 命令 |
| **Takeaway** | 可选；正文已清楚则省略；出现时居中、一句一事 |
| **语言** | 与 [`tools/writing/SKILL.md`](../writing/SKILL.md) 同源：克制、短句、去套话；slide 压缩语域 |
| **事实** | 数字 / 指标名 / 实验编号须准；禁止编造 |

写 outline Part 2「正文要点」= 写即将上屏的短句，遵守上表。口播可略长，仍走 writing skill。

---

## 2. 参考 Pipeline（Agent 默认按此工作）

**完整检查清单**：[`pipelines/agent_deck.md`](pipelines/agent_deck.md)

```text
outline.md
    → generate_*.py（图先 placeholder slot）→ draft.pptx
    → list_image_slots（待填清单）
    → Agent 检索合适本地图 → {slot_id: path}
    → fill_image_slots → 最终 pptx
```

历史上 Week1 曾拆 `*_outline.md` + `*_design.md`；现统一为**一份** `outline.md` 两大部分。  
模板：`templates/outline.template.md`

### 2.1 读 / 写 `outline.md`

**Part 1 · 内容（讲什么）** — 不排版：对象、时长、主线、模块事实/数字/结论、材料路径、不确定点。

**Part 2 · 分页设计（怎么翻页）** — 按 slide：

| 字段           | 说明                                                           |
| -------------- | -------------------------------------------------------------- |
| Slide N · 标题 | 一页一事                                                       |
| 版式           | 封面 / 章节页 / 单栏 bullet / 双栏 / 表+注 / 图+注 / 公式+要点 |
| 正文要点       | 上屏短句（宜少）                                               |
| 图/表          | **slot_id** + 图意 + 路径或「待检索」                          |
| 口播（可选）   | 10–30 s                                                        |

### 2.2 写 `generate_*.py`（先占位）

- `sys.path` 含 `lxm/`；开头 `set_palette("academic"|"defense")`
- 用 `Deck` / `layout.*`；**禁止**复制一套主题与标题组件
- **图先占位**：`add_prior_work_grid` / `add_figure_with_conclusion(..., img_path=None)` / `add_image_placeholder`
- 公式：`set_formula_dir(...)`
- 命名建议：

```text
docs/ref/<topic>_outline.md
scripts/generate_<topic>_ppt.py
docs/ppt/<Topic>.pptx
```

### 2.3 列槽 → 检索 → 填槽

1. `python -m tools.ppt list_image_slots --pptx <draft.pptx>`
2. Agent 按 outline 图意检索，得到显式 `{slot_id: local_path}`（库不扫目录）
3. `python -m tools.ppt fill_image_slots --pptx ... --paths '{...}'`

### 2.4 验收

1. 页序与 Part 2 一致  
2. 数字与 Part 1 一致（路径只在 Part 1 / 脚本，**slide 上无路径**）  
3. 槽已填或有意保留占位；无明显文字重叠  
4. 仍是简约学术，不是营销模板  
5. **文案纪律**：逐页过 [`copy_discipline.md`](copy_discipline.md) §5 自检（禁路径/图号、takeaway、套话）

可选：`export_pdf(pptx, pdf)`

### 2.5 分工

| 产物            | 人             | AI / 脚本                         |
| --------------- | -------------- | --------------------------------- |
| Part 1 内容     | 定主线与事实   | 可协助整理素材                    |
| Part 2 分页     | 审阅疏密与强调 | 可据 Part 1 起草分页与 slot_id    |
| `generate_*.py` | 审接口         | 按 Part 2 填内容；图先占位        |
| 选图 / 填槽     | 可审最终图     | 检索 → `fill_image_slots`         |
| 版式/主题       | —              | 只通过 `tools.ppt`                |

---

## 3. 改库时注意

- 新组件默认符合 §1；缺口补进 `layout`/`theme`，不要在业务脚本里开旁路
- 同进程多项目：每个脚本显式 `set_palette`，避免颜色串台
- 人类可读总览仍见 `README.md`；脚本盘点见 `inventory.md`
