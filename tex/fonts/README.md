# Fonts（与 pandoc-pdf 对齐）

不入库字体二进制。`lxm-academic` 与 `pandoc-pdf` 的 `academic/default` 使用同一套名字：

| 角色 | 字体 |
|------|------|
| 西文 | TeX Gyre Termes / Heros |
| 中文 | Noto Serif CJK SC / Noto Sans CJK SC |
| 等宽 | Noto Sans Mono（文档中按需） |

```bash
sudo apt install -y fonts-noto-cjk fonts-noto-mono texlive-fonts-recommended
```

详见 `tools/pandoc-pdf/fonts/README.md`。
