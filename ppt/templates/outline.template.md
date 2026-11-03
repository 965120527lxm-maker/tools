# \<主题\> PPT 大纲

> 汇报人：  
> 日期：  
> 对象：  
> 风格：简约学术式（见 `tools/ppt/AGENTS.md`）  
> 文案：上屏纪律见 `tools/ppt/copy_discipline.md`（禁路径/Fig./Table；takeaway 可选居中；语言同 `tools/writing/SKILL.md`）  
> 输出：`docs/ppt/<Topic>.pptx` · 脚本：`scripts/generate_<topic>_ppt.py`

---

# Part 1 · 内容（讲什么）

## 1.1 主线

用一两句话说明这次汇报要让听众带走什么。

## 1.2 模块与要点

### 模块 A · \<名称\>

- 背景 / 问题：
- 做了什么：
- 结果（含数字与路径）：
- 限制 / 不确定：

### 模块 B · \<名称\>

- …

## 1.3 材料索引

| 用途         | 路径或文献 |
| ------------ | ---------- |
| 主图         |            |
| 主表数字来源 |            |

---

# Part 2 · 分页设计（怎么翻页）

## 总表

| Part | 主题 | 约页数 | 备注 |
| ---- | ---- | ------ | ---- |
| 0    | 开场 |        |      |
| 1    |      |        |      |
| …    |      |        |      |

---

## Part 0 · 开场

### Slide 1 · 封面

- **版式**：封面
- **主标题**：
- **副标题**（可选）：
- **页脚**：汇报人 · 日期 · 场合

### Slide 2 · 目录 / 概要

- **版式**：左目录 + 右概要（或单栏）
- **要点**：
  1.
  2.

---

## Part 1 · \<章节名\>

### Slide 3 · Chapter 页

- **版式**：章节页
- **Chapter**：1
- **主标题**：
- **副标题**：

### Slide 4 · \<页标题\>

- **版式**：单栏 bullet / 双栏 / 表+注 / 图+注
- **要点**（= 上屏短句，遵守 `copy_discipline.md`；路径只写在下方「图/表」行）：
  - 
  - 
- **图/表**：
  - slot_id：
  - 图意：（Agent 检索对照）
  - 路径：待检索 / 已知路径
- **口播**（可选）：

### Slide 5 · …

---

## 末页 · 总结 / 下一步

- **版式**：
- **要点**：
- **下一步**（动词开头）：

---

## Agent 执行提醒

按 `tools/ppt/pipelines/agent_deck.md`；上屏文案按 `tools/ppt/copy_discipline.md`：

1. 本大纲 → `generate_*.py`（图用 placeholder）→ draft pptx  
2. `list_image_slots` → 检索 → `fill_image_slots` → 最终 pptx  
3. 出稿前过 `copy_discipline.md` §5 自检
