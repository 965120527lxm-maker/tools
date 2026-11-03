# pandoc-pdf · Agent Guide

## 目标命令

```bash
pandoc xxx.md -o xxx.pdf --defaults=academic/default
```

改风格时优先改 `defaults/academic/default.yaml` 与 `headers/academic/*.tex`，再 `./scripts/deploy.sh`。

## 约束

- 不把字体二进制提交进仓库；字体约定写在 `fonts/README.md`
- 不改写 [`IDEA.md`](IDEA.md)（发起人意图）
- 路径：defaults 里的 `headers/...` 相对 **Pandoc data-dir**，故必须先 deploy 或 `build.sh`（会设 `--data-dir`）

## 自检

```bash
./scripts/check.sh
./scripts/build.sh examples/sample.md /tmp/pandoc-pdf-sample.pdf
```
