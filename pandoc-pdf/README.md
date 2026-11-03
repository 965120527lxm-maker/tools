# pandoc-pdf

一键部署 Pandoc PDF **风格模板**，支持：

```bash
pandoc xxx.md -o xxx.pdf --defaults=academic/default
# 等价短选项：-d academic/default
```

注意：不要写成单横线 `-defaults=`——在 Pandoc 2.x 里会被拆成 `-d` + 错误文件名 `efaults=...`。

意图见 [`IDEA.md`](IDEA.md)；进度见 [`todo.md`](todo.md)。  
与 ppt / tex / writing 的分工见 [`../PIPELINE.md`](../PIPELINE.md)。

## 最短路径

```bash
cd /root/autodl-tmp/lxm/tools/pandoc-pdf
chmod +x scripts/*.sh
./scripts/deploy.sh          # 安装到 ~/.local/share/pandoc
./scripts/check.sh
./scripts/build.sh examples/sample.md /tmp/sample.pdf
# 或：
pandoc examples/sample.md -o /tmp/sample.pdf --defaults=academic/default
```

## 布局

```text
tools/pandoc-pdf/
├── defaults/academic/default.yaml   # --defaults=academic/default
├── headers/academic/                # layout / quote / codeblock
├── fonts/                           # 字体说明（无二进制）
├── scripts/deploy.sh                # 一键部署到 Pandoc data-dir
├── scripts/build.sh                 # 带 data-dir 的编译封装
├── scripts/check.sh                 # 依赖与模板自检
└── examples/sample.md
```

部署后 data-dir 中会出现：

```text
~/.local/share/pandoc/
├── defaults/academic/default.yaml
├── defaults/academic.yaml           # 兼容 --defaults=academic
└── headers/academic/*.tex
```

## 风格说明（academic/default）

- 引擎：`xelatex`，A4，边距 2.2cm，1.35 倍行距  
- 中文：Noto Serif CJK SC；西文：TeX Gyre Termes  
- 引用块 / 代码块：浅色 tcolorbox  
- 字体安装见 [`fonts/README.md`](fonts/README.md)

## 自定义 data-dir

```bash
./scripts/deploy.sh /path/to/pandoc-data
pandoc note.md -o note.pdf --data-dir=/path/to/pandoc-data --defaults=academic/default
```
