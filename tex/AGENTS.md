# tex · Agent Guide

## 先读

1. [`../PIPELINE.md`](../PIPELINE.md) — 与 writing / ppt / pandoc-pdf 的分工  
2. [`IDEA.md`](IDEA.md) — 本目录意图（默认不改写）  
3. [`todo.md`](todo.md) — 当前进度  

## 部署

```bash
./scripts/deploy.sh           # sty → $TEXMFHOME（默认 ~/texmf）
./scripts/check.sh            # kpsewhich + 样例 PDF
./scripts/deploy.sh --apt     # 缺包时打印 apt 行
```

改样式：编辑 `packages/lxm-academic/.../lxm-academic.sty` 后重新 `deploy.sh`。

## 红线

- 不把字体二进制提交进仓库  
- 不在未调研前用本目录强行替换 `tools/ppt` 工作流  
- 文风问题转 `tools/writing`，不要用 TeX 模板「润色」中文  
