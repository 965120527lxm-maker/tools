# PPT 文案纪律

Agent 写 outline Part 2「上屏短句」、`generate_*.py` 里的标题 / bullet / caption / takeaway 时，以本文为准。  
视觉版式见 [`AGENTS.md`](AGENTS.md) §1；流程见 [`pipelines/agent_deck.md`](pipelines/agent_deck.md)。

**语言风格**与 [`tools/writing/SKILL.md`](../../writing/SKILL.md) 同源，但幻灯是**压缩语域**：短句、少层级、一页一事。  
项目 house style 全文见各仓库 `Style.md`（若有）；冲突时：**上屏纪律 > 长文 prose 习惯**（例如长文可写路径，slide 不行）。

---

## 1. 上屏 vs 幕后（分层）

| 层级 | 放什么 | 不放什么 |
|------|--------|----------|
| **Slide 上屏** | 内容描述、指标名、数字、方法名、一句因果 | 本地路径、图号、表号、DOI、文件名、shell 命令 |
| **outline Part 1** | 事实、数字、**材料路径**、不确定点 | — |
| **outline Part 2 · 图/表** | slot_id、图意、路径或「待检索」 | 路径不要抄进「正文要点」 |
| **`generate_*.py`** | 常量里可写 `FIG = .../ctc_p6-06.png` | 字符串传入 slide 的 title/caption/bullet 不得含路径 |

口诀：**路径与图号给 Agent 找图用；听众只看内容描述。**

---

## 2. 上屏禁入清单（硬纪律）

下列内容**不得出现在** slide 标题、bullet、表格单元格、图注 caption、takeaway 中：

- 仓库 / 磁盘路径：`docs/ref/...`、`ppt_figures/...`、`/root/...`
- 论文图号式引用：`Fig.1`、`Figure 2`、`Table 5`、`Extended Data Fig.3`
- 文献定位式 caption：`Ma et al. Fig.4 · ...`（改成功能描述，如「Holdout F1 分布」）
- DOI、arXiv id、PDF 文件名
- 命令行：`uv run ...`、`python scripts/...`（口播或 Part 1 可写；上屏改为「本地 veckit 打分」）
- 占位说明里的内部文件名：`figure1.png`、`neurips_Fig3.png`

**允许**：期刊 + 年份（`Nat Methods 2023`）、Challenge 名、指标符号、实验编号（exp004）、公开 URL（注册页、portal）。

**改写示例**

| 不要 | 改为 |
|------|------|
| `docs/ref/RegisteredReport_FrancoBarranco.pdf` | `Registered Report · eLife` |
| `Ma et al. Fig.3 · 28 算法 F1` | `28 算法 holdout F1 分布` |
| `Survey Table 5 节选` | `方法对照表（Arch / Loss / Dataset / Dice / AP）` |
| `uv run veckit` | `本地 veckit 打分` |

---

## 3. Takeaway 纪律

- **可选**：本页 bullet / 表 / 图注已说清，则**不要**底部 takeaway。
- **出现时**：用 `add_highlight_block` 或 `add_*_with_conclusion(conclusion=...)`；库默认**水平 + 垂直居中**。
- **一句一事**：收束本页增量信息，不复读全文 bullet。
- **仍遵守 §2**：takeaway 里同样禁路径、图号。

---

## 4. 语言风格（幻灯压缩版）

摘自 `tools/writing` + 项目 `Style.md`，按 slide 裁剪。

### 4.1 语气

- 组会 / 答辩语域：**克制、有因果、敢写局限**；不夸大、不渲染危机或胜利。
- 术语**首次**可在 caption 或第一条 bullet 用半句解释，后文统一叫法，不玩同义词花样。
- 探索性结果标清楚；不把 pilot 写成 SOTA。

### 4.2 句式与篇幅

- 一页一事；bullet **宜少不宜密**（通常 ≤5 条；表格 ≤6 行）。
- **短句优先**；一条 bullet 一行说清，避免从句套从句。
- 正文 slide **不加粗**、无 emoji 标题（与视觉规范一致）。

### 4.3 建议少用（去 AI 味 / 套话）

**中文套话**：值得注意的是、综上所述、不难发现、在某种意义上、赋能、闭环、抓手、对齐（非技术义）、落地（空泛）、助力、开启新篇章、提供了有益借鉴。

**结构腔**：不是 A 而是 B、与其说 A 不如说 B、一句话总结、归根结底、首先/其次/最后连环、挑战与展望式空收束。

**无数据拔高**：颠覆、革命性、全面更好、机制已建立、完胜。

**空泛连接**：口径、范式、话语、挂到、承接（无指代时）。

有具体数字或对比时，**直接写事实**，不用套话框。

### 4.4 保留区（上屏也要准）

- 指标名、方法名、实验编号（与 frozen protocol 一致）
- 数字与单位；对比须同 protocol
- 引用的 Challenge / 数据集**标准名称**

**禁止编造**：源材料没有的数字、因果、引用。缺信息时写短、写朴素，或 Part 1 标 `[待补]`，不要用假细节填 slide。

### 4.5 口播（outline 可选字段）

口播可略长、可带路径与图号，便于讲解；**仍不要** chatbot 残留（「好问题！」「希望有帮助」）。  
起草口播时可走完整 [`tools/writing/SKILL.md`](../../writing/SKILL.md) 流水线。

---

## 5. 写稿自检（Pass C · slide 版）

出 draft 前逐页问：

1. 标题 / caption 里是否还有路径、Fig./Table、DOI、命令？
2. 底部 takeaway 是否冗余？若保留，是否居中且只有一句？
3. 是否出现无数据的「全面更好 / 机制已建立」？
4. 数字、指标名是否与 outline Part 1 / 冻结文档一致？
5. 冷读是否还有一眼像模型腔的套话？

---

## 6. 与代码的对应

| 纪律 | 实现 |
|------|------|
| takeaway 可选 + 居中 | `add_highlight_block`；`conclusion=None` |
| 上屏文案 | `generate_*.py` 传入 `deck.content()` / `add_bullet_box` / `add_caption` 的字符串 |
| 图路径 | 仅 `img_path=`、常量、`fill_image_slots` map |

脚本头部建议引用本文：

```python
# Copy discipline: tools/ppt/copy_discipline.md
```

---

## 7. 延伸阅读

| 需要 | 打开 |
|------|------|
| 视觉简约学术式 | `AGENTS.md` §1 |
| Agent 全流程 | `pipelines/agent_deck.md` |
| 长文去 AI 味 + 个人声音 | `tools/writing/SKILL.md` |
| 项目 house style 全文 | 各仓库 `docs/Style.md` |
