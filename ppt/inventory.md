# PPT 脚本盘点

日期：2026-08（整合后）

## 项目内生成脚本

| 脚本                                                    | 版式来源                      | 主题 palette | 状态                               |
| ------------------------------------------------------- | ----------------------------- | ------------ | ---------------------------------- |
| `fudan/scripts/generate_spatial_transcriptomics_ppt.py` | `tools.ppt`                   | `academic`   | 已整合；内容页仍在项目侧           |
| `fudan/scripts/generate_week1_ppt.py`                   | `tools.ppt`                   | `academic`   | 已整合                             |
| `fudan/scripts/generate_week2_ppt.py`                   | `tools.ppt`                   | `academic`   | 已整合                             |
| `fudan/scripts/generate_xenium_merfish_workflow_ppt.py` | 经 spatial 脚本 → `tools.ppt` | `academic`   | 已整合                             |
| `SpatialEx/scripts/generate_defense_ppt.py`             | `tools.ppt`                   | `defense`    | 已整合；保留本地插图/诊断图 helper |
| `fudan/scripts/pptx_svg_helper.py`                      | shim → `tools.ppt.svg`        | —            | 已收敛                             |
| `SpatialEx/scripts/pptx_svg_helper.py`                  | shim → `tools.ppt.svg`        | —            | 已收敛                             |

## 归档

`fudan/scripts/archive/generate_spatial_transcriptomics_ppt.py.bak*`

## 设计文档（非 python-pptx）

| 路径                                  | 说明                          |
| ------------------------------------- | ----------------------------- |
| `fudan/docs/ref/week1_ppt_design.md`  | Week1 逐页设计                |
| `fudan/docs/ref/week1_ppt_outline.md` | Week1 大纲                    |
| `fudan/spatial-banana/docs/slides/`   | HTML slides（另一套视觉体系） |

## 公共库能力（`tools/ppt`）

- 双 palette：`academic` / `defense`（`set_palette`）
- 封面、章节页、defense 分区卡、标题、bullet、表格、页脚、分隔线
- 图片等比插入、LaTeX→SVG、SVG 补丁、PDF 导出
- `Deck` 工厂

## 仍留在项目脚本的内容

- 各页文案、实验图路径、matplotlib 概念图 / 诊断图
- defense：`diag_fig` / `add_figure_on_slide(fig_stem)` / 各类 `render_*` 图
