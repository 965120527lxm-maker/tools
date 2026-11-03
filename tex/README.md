# tex

TeX **环境部署**与将来共用学术样式（文档 / Beamer）。  
**各工具在 pipeline 上分管什么** → 必读 [`../PIPELINE.md`](../PIPELINE.md)。

意图 [`IDEA.md`](IDEA.md) · 进度 [`todo.md`](todo.md)

## 最短路径

```bash
cd /root/autodl-tmp/lxm/tools/tex
chmod +x scripts/*.sh
./scripts/deploy.sh          # 安装 lxm sty 到 ~/texmf，并检查引擎/字体
./scripts/check.sh           # 含编译 examples/hello-academic.tex
# 缺系统包时：
./scripts/deploy.sh --apt    # 打印 apt 清单
# ./scripts/deploy.sh --apt-install   # 需 sudo，真正安装
```

## 布局

```text
tools/tex/
├── scripts/deploy.sh      # 部署 sty + 环境检查
├── scripts/check.sh
├── packages/lxm-academic/ # TDS：tex/latex/lxm-academic/*.sty
├── examples/
├── fonts/README.md
└── docs/work_notes/
```

## 与其它工具

| 场景                              | 用谁               |
| --------------------------------- | ------------------ |
| 改文风                            | `tools/writing`    |
| 组会 pptx 流水线                  | `tools/ppt`        |
| md 快速出 PDF                     | `tools/pandoc-pdf` |
| TeX 引擎 / 共用 sty / 将来 Beamer | **本目录**         |

本阶段 sty 仅为占位（字体+版心+色板）；Beamer 主题与长文 class 后续再加。
