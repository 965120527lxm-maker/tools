# 文档写作风格优化

## 目标

从已有 `Style.md` 出发，调研去 AI 味与个人风格学习方案，融汇高星 skills，形成可调用的写作 skill；再让 AI 协助写作更有效率。

## 主入口

| 文件 | 内容 |
|------|------|
| **`SKILL.md`** | 融汇版 skill（`lxm-writing`）：去 AI 味 + Style + 个人样本/VOICE |
| **`lxm-general-writing/SKILL.md`** | 非报告场景通用写作；英文直用 blader-humanizer，中文学术写作按正规教材校准 |
| `scripts/deploy.sh` | 将通用 skill 一键部署到 `~/.kimi/skills` 与 `~/.cursor/skills` |
| `scripts/fetch-zh-academic-corpus.sh` | 从正规来源重建中文学术写作校准语料 |
| `corpus/zh-academic/SOURCES.md` | 中文教材样章、开放教材与版权边界 |
| `SOURCES.md` | 各家借入点与有意未采纳项 |
| `inventory-style.md` | 现有 Style.md 盘点 |
| `research-deai.md` | 调研报告 |
| `skills-catalog/` | 上游 `SKILL.md` 原文 |
| `README.md` | 本文件 |

## 怎么用（最短）

```text
用 lxm-writing / 读取 tools/writing/SKILL.md。

这是我本人的写作样本：
（贴 2–3 段已交周报）

请按我的声音去 AI 味改写：
（贴草稿）
```

也可只加载 `nichespate/docs/Style.md` 做项目规范去味。

普通邮件、消息、回复、解释、介绍文字，以及非报告型中英文学术说明，使用 `lxm-general-writing`：

```text
用 lxm-general-writing，把下面这段改成可以直接发给对方的版本。
```

部署到本机 Kimi 与 Cursor：

```bash
tools/writing/scripts/deploy.sh
```

先看目标路径但不写文件：`tools/writing/scripts/deploy.sh --dry-run`。

重建中文学术写作校准语料：

```bash
tools/writing/scripts/fetch-zh-academic-corpus.sh
```

部署脚本会同时安装 skill 所需的 blader-humanizer 原文和中文学术写作基线，不会复制教材 PDF。

## 上游规范

- `nichespate/docs/Style.md`（规范主源）
- `fudan/docs/Style.md`（副本，术语可能滞后）

## 下一步

1. 从已交周报手工/半自动抽出 `VOICE.md`
2. 三路对照实验后修订 `SKILL.md` 0.2
3. 挂到 Cursor rule / Claude skills 目录（验证后再装）
