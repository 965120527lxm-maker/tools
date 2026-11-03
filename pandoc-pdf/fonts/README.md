# Fonts

本工具**不**在 git 中打包字体二进制。`academic/default` 依赖系统 / TeX 字体。

## 推荐（Ubuntu / Debian）

```bash
sudo apt update
sudo apt install -y \
  pandoc \
  texlive-xetex \
  texlive-lang-chinese \
  texlive-fonts-recommended \
  texlive-latex-extra \
  fonts-noto-cjk \
  fonts-noto-mono
```

| 角色     | 字体名            | 来源                        |
| -------- | ----------------- | --------------------------- |
| 中文正文 | Noto Serif CJK SC | `fonts-noto-cjk`            |
| 西文正文 | TeX Gyre Termes   | `texlive-fonts-recommended` |
| 等宽     | Noto Sans Mono    | `fonts-noto-mono`           |

## 与旧周报 header 对齐（可选）

`nichespate` 周报曾用 `AR PL SungtiL GB` + `Times New Roman`：

```bash
sudo apt install -y fonts-arphic-gbsn00lp ttf-mscorefonts-installer
```

若要做成第二套 defaults（如 `academic/weekly`），可在 `defaults/academic/weekly.yaml` 中改 `CJKmainfont` / `mainfont`。

## 授权

使用发行版字体包时遵循其许可证（Noto：OFL；AR PL：Arphic Public License；TeX Gyre：GUST Font License）。勿将未授权字体提交进本仓库。
