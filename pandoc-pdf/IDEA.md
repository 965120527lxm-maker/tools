# IDEA.md

> 对应根目录 `idea.md` 第 3 项。发起意图如下；细节演进见 `todo.md` / `docs/work_notes/`。

## 意图

在 `tools/pandoc-pdf` 下一键部署 Pandoc 写 PDF 所需的 **defaults + header + 字体约定**，使大家可以用：

```bash
pandoc xxx.md -o xxx.pdf --defaults=academic/default
```

一般而言, 要完成pandoc的一键部署, 需要在~/.local/share/pandoc 下编写 xxx.yaml. 本项目一键为用户部署yaml, 配套相关tex模板, 如quote.tex, layout.tex, codeblock.tex.

得到稳定的中英文学术风格（周报 / 短报告），而不必每个项目复制一份 tex。

## 范围

- **做**：风格模板（`academic/default`）、deploy 到 Pandoc data-dir、依赖检查、最少样例
- **不做**：替代各项目内容写作；不强制捆绑私有字体二进制进 git（优先系统字体包）

## 已知 / 未知

- 已知：本机已有 pandoc 2.9 + xelatex + Noto CJK；`~/.local/share/pandoc` 曾有扁平 `academic.yaml`
- 未知：多人机器上字体名是否一致 → deploy 需校验并给出 apt 提示
