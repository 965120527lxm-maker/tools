# 去 AI 味 & 个人风格学习：调研报告

状态：初稿（基于公开 SKILL.md / README，2026-08）  
目的：弄清领域现有解法，再决定 AI 协作写作怎么更有效率。  
前置：`inventory-style.md`

---

## 0. 问题定义

我们要解决的不是「骗过 AI 检测器」，而是：

1. **减法**：去掉模型默认的套话、均匀节奏、假深刻结构  
2. **加法**：改写结果向**作者本人**靠拢，而不是变成另一种「通用人类文」  
3. **纪律**：数字、路径、实验结论不漂移；与已有 `Style.md` 一致  

验收标准：老师/合作者读起来像你们的周报与笔记，而不是像润色后的 ChatGPT。

---

## 1. 领域里常见的三层解法

市面上方案大多落在下面三层之一（或组合）。理解分层，比记住产品名更重要。

### 1.1 模式目录（Pattern catalog）

把「AI 味」拆成可检测条目：词汇、结构、框架、聊天残留、排版。

权威基线：[Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)（WikiProject AI Cleanup）。多数 skill 都从这里派生或交叉引用。

对中文还额外有：翻译腔、赋能/闭环/综上所述、口号式收束等。

**优点**：可共享、可对照、可写成 checklist。  
**局限**：只做减法；清干净后往往变成「没人味的中性文」。

### 1.2 多轮编辑流水线（Harness / pipeline）

不是一次 prompt 改完，而是固定步骤，例如：

```
发现声音 →（可选）注入个人声音 → 去 tell → 自检残留 → 意义核对
```

或：

```
频道/语域判定 → voice 校准 → 结构扫描优先于换词 → 严重度门控 → 改写 → 二次自审
```

**共识（多份 skill 独立强调）**：

- AI 味的主信号在**结构均匀**（句长、段形、连接词节奏），不在个别词  
- 换词式 humanizer 容易留下「新的均匀指纹」  
- 二次自审（"还剩什么一眼像 AI？"）比单次改写更稳  
- 过检测器不是目标；过度抛光反而更像机器

### 1.3 个人声音：两种主流 UX（比「有没有 STYLE.md」更关键）

观察：多数 humanizer 仓库看起来像「一堆 Markdown 规则」；但高星工具里，**个人风格**通常还有另一条更轻的入口——**当场贴一段本人文本，让模型当场学，再改待改稿**。

这两条路径不要混为一谈：

| UX | 做法 | 代表 | 优点 | 局限 |
|----|------|------|------|------|
| **A. 持久规则/档案文档** | 仓库里放 `Style.md` / `VOICE.md` / house-rules，skill 自动发现并加载 | 多数项目的默认形态；hannsxpeter 的 VOICE schema；我们已有 Style.md | 可版本管理、可跨会话复用、可挂 AGENTS | 冷启动要写/维护文件；档案过时会「学旧习惯」 |
| **B. 会话内贴样本（in-session sample）** | 同一轮对话里先贴 2–3 段本人真文，再贴待改稿；模型当场抽取节奏再改写 | **[blader/humanizer](https://github.com/blader/humanizer)**（~32k★）文档写得很直白；hannsxpeter / humanize-text-skill / Shirhussain 也支持「贴样本优先」 | **零配置就能试**；活样本优先于过时档案；适合周报场景「翻出上周终稿当样本」 | 每轮要带样本（或靠对话记忆）；不沉淀则下次从零；样本选差会污染当次改写 |

高星项目里还有第三种，**不要当成个人学习**：

| UX | 做法 | 代表 | 说明 |
|----|------|------|------|
| **C. 预设 voice 档位** | `--voice casual/professional/technical/warm/blunt` | Aboudjem/humanizer-skill 等 | 这是**类型腔**，不是「像你」。去 AI 味有用，学个人习惯不够 |

优先级（多份 skill 一致，尤其 blader / hannsxpeter）：

```
本轮粘贴的本人样本  >  项目内 VOICE.md / Style 档案  >  预设 voice 档位  >  通用去味
```

对你们的含义：

- 已有 `Style.md` = 路径 A 的 **house style**（项目规范），不是完整个人声音  
- 高星工具证明路径 B **已经是成熟主流用法**，不必先写完美 VOICE 才能开始试  
- 中长期仍建议 A+B：会话里贴样本做改写；满意后把抽取结果落成 `VOICE.md`，减少每次粘贴

抽取维度（无论 A 还是 B，模型实际在学这些）：

| 维度 | 含义 |
|------|------|
| Cadence | 句长分布、是否用碎片句 |
| Diction / register | 用词高度、术语容忍度 |
| Signature moves | 爱用的起承、设问、短段落收束 |
| Punctuation | 破折号、分号、括号习惯 |
| Stance | 犹豫怎么写、是否敢写负面结果 |
| Avoid | 作者从不做的事 |
| Sample paragraph | 一段真文，比抽象描述更管用 |

冲突规则：

> **作者真实习惯 > 通用去 AI 规则 > 中性默认**

---

## 2. 候选 Skills 深读（按我们需求排序）

评价轴：中文、个人声音学习、与 Style.md 可叠加、事实保护、Cursor/Claude 可挂载、维护清晰度。

### A. 个人声音学习能力强（优先深挖）

#### A1. [hannsxpeter/humanizer](https://github.com/hannsxpeter/humanizer)

- **类型**：pure-prompt skill（SKILL.md + references）  
- **流水线**：Step0 发现声音 → Pass1 先注入 voice → Pass2 去 tell（32 patterns）→ Pass3 自检（可否决前两轮）  
- **声音学习**：自动搜 `VOICE.md` / `STYLE-GUIDE.md`；也可贴样本或点名作者；有完整 `voice-matching.md` schema  
- **纪律**：默认不编造细节；stance 模式需显式开启；意义核对强制输出  
- **与我们的契合**：分层清晰——可用 Style 当 house rules，VOICE 当个人档案；「density 低则少改」适合手稿终检  
- **缺口**：英文模式目录为主；中文套话需我们自己补进 house rules / Style

#### A2. [milock/humanizer](https://github.com/milock/humanizer)

- **类型**：portable skill + guided setup  
- **流水线**：6 步；**结构扫描优先于词汇**；full rewrite vs patch 门控；`[HOLLOW]` 空心稿标记  
- **声音学习**：`humanizer setup` 访谈（样本、quirks、hard nos、标点）→ 生成 author-voice 文件；支持 brand voice  
- **与我们的契合**：setup 流程可把周报终稿变成可维护档案；stet 协议（作者说保留则保留）适合科研表述  
- **缺口**：频道矩阵偏邮件/LinkedIn/blog；周报/实验笔记需自定义 channel；中文非一等公民

#### A3. [Shirhussain/humanize](https://github.com/Shirhussain/humanize)

- **类型**：skill + 可选 Python linter（可进 CI）  
- **双模式**：生成时约束 / 事后 rewrite  
- **声音学习**：2–3 段样本 → `voice-profile.md`；用户纠正时就地更新  
- **与我们的契合**：「干净中性 ≠ 有声音」说得很透；register（formal/report）贴近周报  
- **缺口**：中文深度一般；linter 规则偏英文 Wikipedia 系

#### A4. [fendouai/humanize-text-skill](https://github.com/fendouai/humanize-text-skill)

- **类型**：skill + **可执行 detector**（Node）+ voice.drift  
- **中英双语**：中文黑话（值得注意的是/赋能/闭环/综上所述）有现成条目  
- **声音**：`voiceMode: custom` + 样本；score 与 voice.drift 分轨  
- **保护**：path、数字、命令、引用等 span 保护，对科研周报极重要  
- **与我们的契合**：可做「客观分数」辅助，不全靠模型自觉；场景包含 docs  
- **缺口**：voice 目标常见 casual/professional/technical，**个性化深度**弱于 A1/A2 的 VOICE.md 体系；更像「拉向某类声音」而非完整作者档案

### B. 中文去味强、个人声音为辅

#### B1. [op7418/humanizer-zh](https://github.com/op7418/humanizer-zh)（及衍生如 ai-zixun 版）

- **类型**：中文 skill，安装量大  
- **能力**：24 类中文 AI 模式；翻译腔/营销通稿；质量量表  
- **声音**：部分衍生版带 `references/voices/`（模仿公开作者）或「若项目有样例则优先」——**默认不是学你本人**  
- **与我们的契合**：中文减法清单可直接对照补强 Style 第 3–4 节  
- **缺口**：个人风格学习不是一等公民；「注入灵魂」若无 VOICE 约束，可能换上另一种通用腔

### C. 规则包 / Cursor 规则（减法为主）

#### C1. [daniel-bogale/anti-ai-writing-humanizer](https://github.com/daniel-bogale/anti-ai-writing-humanizer)

- house-rules 可编辑；Cursor `.mdc` 友好  
- 适合当「禁词与结构」承载层；个人声音需自建 VOICE 叠加

#### C2. [avikbal-dm/anti-ai-writing-claude-skill](https://github.com/avikbal-dm/anti-ai-writing-claude-skill)

- 强调不编造、缺信息就问作者  
- 对科研事实纪律有启发；声音学习一般

### D. SaaS Humanizer / 检测器（对照，不默认采用）

WalterWrites、各类 AI Humanizer、Turnitin/Pangram 类检测器等。

**共同局限**（与多份 skill 作者观点一致）：

- 多为换词与句长扰动，难对齐项目术语  
- 学不会你们的周报声音  
- 容易引入新指纹；且我们**不以过检测为验收**

---

## 3. 对照总表

| 方案 | 中文 | 去 AI 模式库 | 个人声音学习 | 事实/路径保护 | Harness 成熟度 | 建议角色 |
|------|------|--------------|--------------|---------------|----------------|----------|
| hannsxpeter/humanizer | 弱（可外挂） | 强（32） | **很强**（VOICE 优先） | 强（意义核对） | 很高 | **主改写引擎候选** |
| milock/humanizer | 弱 | 强（结构优先） | **很强**（setup） | 中强（不编造） | 很高 | **VOICE 冷启动候选** |
| Shirhussain/humanize | 中弱 | 强 | 强（profile 文件） | 强 | 高 + 可选 lint | 生成时约束 / CI 辅助 |
| humanize-text-skill | **强** | 强（双语可执行） | 中（custom sample） | **很强** | 高 | **中文检测 + 保护层** |
| humanizer-zh | **很强** | 强（中文 24） | 弱–中 | 中 | 中 | **中文减法清单来源** |
| anti-ai-writing-humanizer | 中 | 强 | 中（house-rules） | 中 | 中 | Cursor 规则承载 |
| SaaS humanizer | 不一 | 黑盒 | 基本无 | 弱 | 产品化 | 不采用 |

---

## 4. 与现有 Style.md 如何咬合

你们已经有一半「去 AI 味」：

| Style 已有 | 对应领域概念 |
|------------|----------------|
| 少加粗/少括号/少冒号长解释 | Formatting tells |
| 「不是 A 而是 B」禁用 | Negative parallelism |
| 空泛连接词与夸张判断 | Vocabulary + significance inflation |
| 背景→过程→限制→下一步 | 反 listicle / 反假总结结构 |
| 数字须锚定路径 | Fidelity / protected spans |

仍缺的一半是领域标准解法里的 **VOICE 层** 与 **多轮 harness**。

推荐心智模型：

```
输入草稿
  → 加载 Style.md（项目规范 + 术语）
  → 加载 VOICE.md（从周报终稿学习的个人习惯）
  → Pass: 中文 AI 模式检测（可借鉴 humanizer-zh / humanize-text-skill）
  → Pass: 按个人声音改写（hannsxpeter / milock 思路）
  → Pass: 意义与数字核对
  → 人工终检
  →（可选）终稿差异回写 VOICE
```

不要把 Style 与 VOICE 揉成一份无法维护的大文件。

---

## 5. 个人风格学习：可行做法（领域共识）

不依赖某一产品，当前靠谱做法是：

1. **语料**：只收「真人手写或手改充分」的终稿（如已交周报），排除纯 AI 草稿  
2. **体量**：冷启动约 2–3 段、合计 ≥150–300 字可出低置信档案；更好是 1–3 篇完整周报  
3. **抽取**：按 cadence / diction / moves / punctuation / stance / avoid 填 `VOICE.md`，并附一段原文 Sample  
4. **冲突**：作者习惯覆盖通用禁则  
5. **迭代**：作者说「我不会这么写」→ 立刻改 VOICE，而不是只改当次输出  
6. **禁止**：用别人的文风样本、用著名作者腔、用营销号 voices/ 目录污染个人档案  

对你们：`weekly_reports/` 下已交周报是现成金矿；`Style.md` 第 8 节已点名其中一篇作语气参考——说明方向早就对了，只是还没结构化成 VOICE。

---

## 6. 商业 Tools 与 Agent Skills 的取舍

| 路径 | 何时有意义 | 对我们 |
|------|------------|--------|
| Agent Skill（SKILL.md） | 写作在 Cursor/Claude 内完成 | **主路径**：可加载仓库内 Style/VOICE |
| Cursor Rule（.mdc） | 希望默认提醒、少记命令 | 可把触发词与文件路径写死 |
| 可执行 linter/detector | 想要客观分数、CI | 作辅助，不作唯一裁判 |
| SaaS 粘贴 humanizer | 偶发英文营销文 | 不适合科研周报与术语 |

---

## 7. 现阶段结论（决策，不是实现）

### 7.1 领域结论（我们认为成立的）

1. 去 AI 味的主流解法 = **模式目录 + 多轮 harness +（可选）可执行检测**  
2. 「像人」≠「像你」；没有 VOICE/样本学习，最终会停在中性腔  
3. 结构方差 > 换词；二次自审几乎是标配  
4. 科研场景必须把 **事实保护** 和 **术语表** 放进流水线，不能只用通用 humanizer  

### 7.2 对我们仓库的选型倾向（待小试验证）

| 角色 | 倾向 |
|------|------|
| 个人声音主引擎 | hannsxpeter（VOICE.md 最完整）或 milock（setup 体验好） |
| 中文减法补强 | humanizer-zh 模式清单 → 吸收进 Style/附录，不必整包依赖 |
| 检测与 span 保护 | humanize-text-skill 的思路（尤其 path/数字） |
| 规范承载 | 现有 Style.md 继续做 house style；另建 VOICE.md |

**不建议**：以 SaaS humanizer 或「过检测」作为主验收。

### 7.3 对「之后让 AI 写作如何更有效率」的建议

效率不来自「一次生成完美终稿」，而来自**分工**：

| 步骤 | 谁做 | 要点 |
|------|------|------|
| 1. 骨架与事实 | 人 或 AI 填表 | 先给：本期做了什么、数字、路径、不确定点（可模板化） |
| 2. 起草 | AI | 强制加载 Style + 术语；要求按周报七段骨架 |
| 3. 去味 + 靠拢声音 | AI（skill harness） | 加载 VOICE；结构优先；禁止编造 |
| 4. 终检 | 人 | 读「目前的认识」与数字是否仍是自己的判断 |
| 5. 回灌 | 人触发 AI | 终稿与草稿差异 → 更新 VOICE |

关键杠杆：**把时间从「逐句改 AI 腔」挪到「维护 Style/VOICE + 提供事实卡片」**。  
草稿可以脏，档案必须真。

---

## 8. 建议的下一步（仍属调研收尾，小步验证）

按优先级：

1. **冻结规范源**：以 `nichespate/docs/Style.md` 为规范主源；fudan 标明副本或改指向  
2. **手工试抽一份 VOICE 草稿**：从 1–2 篇已交周报抽出 cadence/stance/sample（先人工，不装 skill）  
3. **小对照实验**（同一段 AI 草稿，三路改写）：  
   - 仅 Style  
   - Style + 通用 humanizer-zh 思路  
   - Style + VOICE（按 hannsxpeter 维度）  
   人工盲评哪路最像本人  
4. **再决定**安装哪个 skill / 是否写 Cursor rule——用实验数据拍板，而不是用 star 数

---

## 9. 参考链接

- Wikipedia [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)  
- [hannsxpeter/humanizer](https://github.com/hannsxpeter/humanizer) + `references/voice-matching.md`  
- [milock/humanizer](https://github.com/milock/humanizer)  
- [Shirhussain/humanize](https://github.com/Shirhussain/humanize)  
- [fendouai/humanize-text-skill](https://github.com/fendouai/humanize-text-skill)  
- [op7418/humanizer-zh](https://github.com/op7418/humanizer-zh)  
- 内部：`nichespate/docs/Style.md`，`inventory-style.md`
