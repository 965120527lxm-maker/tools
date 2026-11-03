# 参考 Pipeline：Agent 出一副学术 PPT

Agent 默认按本流程工作。规范细节见上级 [`AGENTS.md`](../AGENTS.md)。  
**文案纪律**（上屏禁路径/图号、takeaway、语言风格）：[`copy_discipline.md`](../copy_discipline.md)。  
**检索/选型由 Agent 完成**；库只提供占位与按 map 填槽，不扫目录找图。

```text
① outline.md
      │  读 Part 1（事实）+ Part 2（分页 / slot 需求）
      ▼
② generate_<topic>_ppt.py
      │  版式走 tools.ppt；图一律 placeholder slot
      │  → 先产出 draft pptx（可有空槽）
      ▼
③ 渲染审查 + 空白填充
      │  export_pdf → pdftoppm → montage 全页网格
      │  空白页用「有出处的内容」填充 → 重跑 ②
      ▼
④ list_image_slots
      │  列出待填 slot_id + 所在页
      ▼
⑤ Agent 检索
      │  按 outline / 槽标签找合适本地图（论文图、项目 docs、自绘…）
      │  得到显式 map：{slot_id: path}
      ▼
⑥ fill_image_slots
      │  只吃上一步的 map，写入 pptx
      ▼
⑦ 验收 → 最终 pptx（可选 export_pdf）
```

---

## Step ① 读 / 写 `outline.md`

- 模板：`templates/outline.template.md`
- Part 1：主线、事实、数字、材料索引（**可含路径**；不排版）
- Part 2：按 slide 写版式；**「正文要点」= 上屏短句**，遵守 [`copy_discipline.md`](../copy_discipline.md)（禁路径、Fig./Table、套话）
- Part 2 图/表字段：凡需要图的页写清：
  - **slot_id**（稳定短名，如 `ddpm`、`pipeline`）
  - **图意**（Agent 检索时对照）
  - **路径**（已知则填；未知写「待检索」）

不要在 outline 里发明未存在的实验数字。

---

## Step ② 写并运行 `generate_*.py`（先占位）

约定：

- `sys.path` 含 `lxm/`；开头 `set_palette("academic"|"defense")`
- 只用 `tools.ppt` 版式，禁止复制主题组件
- **有图的页先占位**，生成阶段不要假设图已齐：
  - `add_prior_work_grid(...)`（默认占位）
  - `add_figure_with_conclusion(slide, img_path=None, slot_id=...)`
  - 或 `add_image_placeholder(..., slot_id=...)`
- 脚本保存 draft：`docs/ppt/<Topic>.pptx`（或项目约定路径）

参考实现：`examples/generate_diffusion_intro_ppt.py`（`--placeholders-only` 停在 draft）。

```bash
python scripts/generate_<topic>_ppt.py --placeholders-only
# → docs/ppt/<Topic>.pptx   （槽仍空）
```

---

## Step ③ 渲染审查 + 空白填充

**先渲染全页、再谈排版。** 不要凭想象判断版面——生成 draft 后立刻出图检查。

### 审查工具

```bash
export_pdf(...)                       # pptx → pdf（tools.ppt.export_pdf）
pdftoppm -png -r 40 deck.pdf /tmp/pg  # pdf → 全页 png
montage /tmp/pg-*.png -tile 2x3 -geometry +4+4 /tmp/grid.png
```

逐页（或逐网格）看三类问题：

1. **空白过半**：bullets/表格只占了上半页，下半页全空；
2. **重叠溢出**：文字压图、长句出界；
3. **图被挤小**：宽高比不合的图被高度限制缩成一团（解法：拆成「文字页 + 整图页」两页）。

### 空白填充参考思路（按内容出处选工具）

原则：**只填有出处的内容**（实测数字、设计文档、论文结论、明确的假设），不凑字。填完还是填不满的页，考虑与邻页合并。

| 填充思路 | 适用场景 | 工具 |
| --- | --- | --- |
| 映射/角色表 | 概念×工作线、方法×角色（基线/对照/本组） | `add_table`（≤6 行） |
| 表格拉伸与字号 | 内容真实但量少：加大列宽/行高、上调表体字号 | `add_table` 的 `width` / `row_height_factor` / `font_size_body` 参数 |
| 详细说明文字 | 选型理由、QC 数字、预期假设、判据 | `add_bullet_box`（无序列表文本框） |
| 双栏对照 | 内部指标 vs 外部证据、路线 A vs 路线 B | `add_two_column_compare`（不要中间标就 `vs_label=""`） |
| 实验矩阵 | 维度×水平×样本量贡献 | `add_table` |
| 里程碑/验收表 | 任务×交付物×验收标准 | `add_table` |
| 流程图 | 验证流程、pipeline | `add_flowchart_row`（原生方块，无需图片） |
| 底部 takeaway | 可选；正文已清楚则省略；出现时居中 | `add_highlight_block` / `add_*_with_conclusion(conclusion=None)` |
| 图占位 | 确定要图但暂未产出 | `add_image_placeholder` / `add_figure_with_conclusion(img_path=None, slot_id=...)`（进 ④ 的槽清单） |

反面：为填满而堆装饰元素、塞无关图——都不做；表格拉伸与字号上调可以用，但前提是内容真实，没内容时靠放大字号假装充实不做。

居中约定（库默认）：`add_figure_on_slide` 的图在给定盒内**水平 + 垂直居中**；
`add_flowchart_row` 不显式给 `left` 时整行**水平居中**；表格单元格文字垂直居中；
`add_highlight_block` 文字**水平 + 垂直居中**。
发现某页图/行偏左时，先确认是不是绕过了这两个函数。

**文案**：上屏禁路径 / 图号 / DOI / 命令；takeaway 可选且居中；语言风格见 [`copy_discipline.md`](../copy_discipline.md) §2–§4（与 `tools/writing/SKILL.md` 同源）。

---

## Step ④ 检查待填充图

```bash
python -m tools.ppt list_image_slots --pptx docs/ppt/<Topic>.pptx
```

或：

```python
from tools.ppt import call_agent_tool
slots = call_agent_tool("list_image_slots", pptx_path="docs/ppt/Topic.pptx")
# → [{slot_id, slide_index, ...}, ...]
```

对照 outline Part 2 的「图意」，列出还缺哪些 `slot_id`。

---

## Step ⑤ 检索可填充的图

由 **Agent** 完成（本库不注册搜图工具）：

- 先查 outline「材料索引」与项目 `docs/`、论文附图
- 不够再检索/自绘；落到**本地路径**
- 输出显式 map，例如：

```json
{
  "ddpm": "/abs/path/ddpm_schematic.png",
  "pipeline": "/abs/path/noise_to_data.png"
}
```

未找到的槽：宁可留占位，不要硬塞无关图。

---

## Step ⑥ 填槽

```bash
python -m tools.ppt fill_image_slots --pptx docs/ppt/<Topic>.pptx \
  --paths '{"ddpm":"/abs/a.png","pipeline":"/abs/b.png"}'
```

或：

```python
call_agent_tool(
    "fill_image_slots",
    pptx_path="docs/ppt/Topic.pptx",
    paths={"ddpm": "/abs/a.png", "pipeline": "/abs/b.png"},
)
```

只传已确认的键；缺文件的 id 会被 skip，占位保留。

---

## Step ⑦ 验收与输出

核对：

1. 页序 / 标题与 outline Part 2 一致  
2. 数字与 Part 1 一致  
3. 待填槽已填或有意保留占位  
4. 无文字重叠；空白页已按 Step ③ 填充或合并；仍是简约学术式  
5. **文案纪律**：[`copy_discipline.md`](../copy_discipline.md) §5 自检 — slide 无路径/图号/命令；takeaway 不冗余；无套话腔

最终产物：`docs/ppt/<Topic>.pptx`。可选：`export_pdf(...)`。

---

## 一页清单（可贴进任务提示）

```
[ ] 读 outline.md（Part1 事实 + Part2 分页/slot）
[ ] 写 generate_*.py：图用 placeholder slot
[ ] 跑脚本得到 draft pptx
[ ] export_pdf + pdftoppm + montage → 渲染审查
[ ] 空白页按出处填充（表/说明文字/双栏/流程图/图槽）→ 重跑脚本
[ ] list_image_slots → 待填清单
[ ] 检索/选型 → {slot_id: local_path}
[ ] fill_image_slots
[ ] 验收页序、数字、留白、视觉风格
[ ] 文案纪律：上屏无路径/Fig./Table/命令；takeaway 可选居中；去套话（copy_discipline.md §5）
```

---

## 反例（不要做）

- 在 `fill_image_slots` 里写死「扫描某目录自动配对」
- 生成阶段找不到图就跳过整页或伪造路径
- 不读 outline 直接堆版式
- 复制一份 theme/layout 到业务脚本
- 为填满空白而堆装饰、塞无关图、放大字号假装充实
- 把 Part 1 路径或 `Fig.3` 抄进 slide 标题 / bullet / caption（见 [`copy_discipline.md`](../copy_discipline.md)）
- slide 用「值得注意的是 / 赋能 / 不是 A 而是 B」等套话（见 `copy_discipline.md` §4）
