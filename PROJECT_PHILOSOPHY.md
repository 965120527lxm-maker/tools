# 项目设计哲学

`idea.md` / `IDEA.md` 是发起人认知接口；AI 不得创建，也不得改写其内容。 本文件与模板可由人机共同维护。


## 1. 管理方式

These
| axis    | aim                                      | on what                 |
| ------- | ---------------------------------------- | ----------------------- |
| time    | 每天做了什么、用了什么知识、认知如何推进 | `docs/work_notes/`      |
| content | 这个目录做到哪、对外如何说明             | `todo.md` / `README.md` |

work_note is only created by human. and todo.md, Readme.md can be created by agent when neccesary.

**robot_notes**：AI 可以在 `docs/robot_notes/YYYY-MM-DD.md` 自己记录当日工作与知识（robot 视角的日志）。
人类可以在 robot_notes 上批注、修正，但不替 robot 写。人类自己的笔记放 `docs/work_notes/`，robot 不创建、不修改。

## 2. 轻量两件套（内容轴）

目录有独立意图、且确实需要时才放下面两件；**不强制每个目录都建**：

```text
todo.md     ① 推进：清单、进度、前期反馈、阻塞（人机共维）
README.md   ② 收束：别人（或未来的自己）如何理解与使用现状
```

「必要时」的判据：

- `todo.md`：有持续推进的多条任务、需要记录阻塞与决策时。
- `README.md`：阶段收束、需要对外或对己说明结构与用法时；未收束前可以很短，指向 todo 即可。

### 2.1 关于 `IDEA.md / idea.md`

- AI **不创建、不改写**任何 `IDEA.md / idea.md`。
- 目录中若已存在发起人亲笔的 `idea.md`（如根目录、`fudan/visualization/`），它是**最高优先级的只读意图输入**（见 §5）。
- 发起人想为新目录立意图时自行书写；`docs/templates/IDEA.template.md` 仅供其自发使用，非约定要求。

### 2.2 `todo.md`（监控）

- 总体进度、勾选状态、前期反馈与决策记录。
- 可引用 `docs/work_notes/YYYY-MM-DD.md` 作为某日细节。
- AI 可协助更新勾选与拆条，但不得虚构已完成项。

### 2.3 `README.md`（收束）

- 在阶段可对外（或对内稳定）使用时维护：结构、如何运行。
- 未收束前可以很短，但应指向 todo，避免空目录无入口。


## 3. 推荐项目骨架

```text
<project>/
├── src/<pkg>/       # 自有库代码，按一般标准 Python 包样式（无库代码则不建）
├── exp/             # 按实验编号组织：exp{三位编号}_{简短描述}/{scripts,configs,outputs}，详见下文
├── data/  configs/  external/  tests/
├── docs/
│   ├── work_notes/  # 人类自己写,机器人不负责创建. 这里是人类自己梳理每天想法的地方
│   └── robot_notes/ # AI 自己写的工作/知识日志;人类可以在上面批注
├── AGENTS.md        # 可选：给代理的操作约束（可链到本哲学）
├── todo.md          # 必要时
└── README.md        # 必要时
```

- **`exp/` 按实验编号组织**，每个实验一个目录，`scripts/` 与 `outputs/` 收进实验内部；可复用的库代码只进 `src/`：

  ```text
  exp/
  ├── README.md
  ├── exp{三位编号}_{简短描述}/
  │   ├── scripts/      # 入口脚本：只调用 src 中的库，保持纤薄（原则上 ≤50 行）
  │   ├── configs/      # YAML 实验配置
  │   └── outputs/      # 产物，按时间分子目录，gitignored；可含 summary.md、*.csv 等
  ├── exp_test/         # 测试即实验
  ├── exp_other/        # 其他实验：如输出 PPT、周报的脚本
  └── exp_preprocess/   # 预处理即实验
  ```

  每个 `expXXX/` 自包含该次实验探索的入口、配置与产物；实验之间的共享逻辑必须抽到 `src/`，不得在实验间相互 import。

- 既有目录（如 `fudan/`）可缓迁移；`exp/` 结构自新实验 / 新项目起生效。
- 子目录若形成独立意图（如 `tools/ppt/`），可按需再放自己的 todo/README；不必每一层都建满。


## 4. 模板

约定模板见 [`docs_templates/templates/`](docs_templates/templates/)：`todo.template.md`、`README.template.md`、`work_note.template.md`。  
`IDEA.template.md` 仅供发起人自发使用，非约定要求。

