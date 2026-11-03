---
title: Pandoc academic/default 样例
author: tools/pandoc-pdf
date: 2026-08-02
---

# 摘要

这是 `academic/default` 风格的最短样例：中英混排、公式、引用块与代码。

# 正文

空间转录组学（spatial transcriptomics）需要在组织学图像上对齐分子读数。  
The forward process of a diffusion model gradually adds Gaussian noise.

行内公式 $x_t = \sqrt{\bar\alpha_t}\,x_0 + \sqrt{1-\bar\alpha_t}\,\epsilon$，以及块级：

$$
\mathcal{L} = \mathbb{E}\big\| \epsilon - \epsilon_\theta(x_t, t) \big\|^2
$$

> 引用块应带浅色左边框，便于在周报里强调结论。

## 列表

1. 部署：`./scripts/deploy.sh`
2. 编译：`pandoc note.md -o note.pdf --defaults=academic/default`

## 代码

```python
def greet(name: str) -> str:
    return f"hello, {name}"
```

## 小表

| 项 | 值 |
|----|----|
| pdf-engine | xelatex |
| 中文字体 | Noto Serif CJK SC |
