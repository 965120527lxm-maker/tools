# IDEA.md

> 对应根 `idea.md`：引入 TeX 做 PPT / 文档，PDF 更方便渲染。  
> AI 默认不改写本文件的意图表述。

## 意图

先提供 **TeX 环境一键部署与自检**，并写清与 `writing` / `ppt` / `pandoc-pdf` 在 pipeline 上的分工；再逐步放下共用 sty / Beamer，而不是一上来替换现有工具。

## 范围

- **做**：deploy / check；本地 texmf 安装点；pipeline 说明；日后 academic sty 与样例
- **不做**：文风改写；不强制立刻淘汰 python-pptx 与 pandoc defaults

## 关系

- 分工总表：[`../PIPELINE.md`](../PIPELINE.md)
- PDF 快路径仍用：`../pandoc-pdf/`
- 幻灯现状仍用：`../ppt/`
