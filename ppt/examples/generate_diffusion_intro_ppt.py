#!/usr/bin/env python3
"""Diffusion Model intro — reference for the agent PPT pipeline.

Pipeline (see tools/ppt/pipelines/agent_deck.md):
  diffusion_outline.md
    → this script (placeholders first) → draft pptx
    → list_image_slots / fill_image_slots → final pptx

  # draft only（槽空着，模拟 Agent 生成阶段）
  python tools/ppt/examples/generate_diffusion_intro_ppt.py --placeholders-only

  # 完整演示：生成占位后再用 agent 工具填图（示例图由本脚本绘制）
  python tools/ppt/examples/generate_diffusion_intro_ppt.py
"""

from __future__ import annotations

import argparse
import json
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

EX_DIR = os.path.dirname(os.path.abspath(__file__))
LXM_ROOT = os.path.abspath(os.path.join(EX_DIR, "..", "..", ".."))
sys.path.insert(0, LXM_ROOT)

from pptx.util import Inches  # noqa: E402

from tools.ppt import (  # noqa: E402
    Deck,
    add_background_page,
    add_figure_with_conclusion,
    add_flowchart,
    add_formula_derivation,
    add_prior_work_grid,
    add_problem_page,
    add_table_with_conclusion,
    add_two_column_compare,
    call_agent_tool,
    set_formula_dir,
    set_palette,
)

set_palette("academic")
set_formula_dir(os.path.join(EX_DIR, "formula_cache"))

OUT = os.path.join(EX_DIR, "diffusion_intro.pptx")
FIG_DIR = os.path.join(EX_DIR, "diffusion_figs")


def _save_fig(name: str):
    os.makedirs(FIG_DIR, exist_ok=True)
    path = os.path.join(FIG_DIR, name)
    plt.tight_layout()
    plt.savefig(path, dpi=140, bbox_inches="tight", facecolor="white")
    plt.close()
    return path


def make_demo_figures():
    """Stand-in for 'Agent retrieved suitable images' — flat schematics only."""
    paths = {}

    fig, ax = plt.subplots(figsize=(8, 2.2))
    xs = np.linspace(0, 1, 200)
    ax.fill_between(xs, 0, 0.35 + 0.15 * np.sin(8 * xs), color="#1e3a5f", alpha=0.35)
    ax.fill_between(xs, 0, 0.2 * np.random.RandomState(0).rand(200), color="#e67e22", alpha=0.5)
    ax.text(0.08, 0.75, "noise", fontsize=12, color="#666")
    ax.text(0.78, 0.75, "data", fontsize=12, color="#1e3a5f", fontweight="bold")
    ax.annotate("", xy=(0.85, 0.4), xytext=(0.15, 0.4),
                arrowprops=dict(arrowstyle="->", color="#e67e22", lw=2))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_title("reverse denoising (schematic)", fontsize=11)
    paths["pipeline"] = _save_fig("pipeline.png")

    labels = ["DDPM", "DDIM", "Score SDE", "LDM"]
    colors = ["#1e3a5f", "#2c4a6e", "#e67e22", "#c96a1a"]
    keys = ["ddpm", "ddim", "score", "ldm"]
    for lab, c, key in zip(labels, colors, keys):
        fig, ax = plt.subplots(figsize=(2.4, 2.0))
        ax.set_facecolor("#e8eef5")
        ax.add_patch(plt.Rectangle((0.15, 0.2), 0.7, 0.55, fill=True, color=c, alpha=0.85))
        ax.text(0.5, 0.48, lab, ha="center", va="center", color="white", fontsize=13, fontweight="bold")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        paths[key] = _save_fig(f"{key}.png")
    return paths


def build_draft() -> str:
    """Step ②: content + layouts; all figures are placeholder slots."""
    deck = Deck(author="tools/ppt · example", total=10)

    deck.cover(
        "Diffusion Model 简介",
        footer_line="版式函数示例 · 简约学术式",
        date_line="2026-08",
    )
    deck.chapter(1, "背景与问题", "从生成模型到可采样噪声")

    s = deck.content("背景：为何需要扩散模型")
    add_background_page(
        s,
        "生成模型要学习复杂数据分布，并稳定地从噪声画出样本。",
        [
            "GAN：对抗训练，样本清晰但训练不稳、模式崩塌风险高。",
            "VAE：变分下界可解，但重建常偏模糊。",
            "扩散模型：把分布变换拆成多步小高斯扰动，训练目标更平滑。",
            "代价是采样步数多；后续工作用蒸馏、跳步、隐空间加速。",
        ],
        note="本页用 add_background_page：导语 + 要点 + 底栏结论。",
    )

    s = deck.content("问题：如何把数据变成可采样噪声")
    add_problem_page(
        s,
        "核心问题：能否用一条可逆的噪声过程连接数据分布与标准高斯？",
        [
            "前向：逐步加噪，终态逼近各向同性高斯，便于采样。",
            "反向：学习每一步去噪（或得分），从噪声走回数据。",
            "训练：常用噪声预测 MSE，与变分界在一定参数化下等价。",
            "推理：迭代去噪；步数与质量需要权衡。",
        ],
        goal="目标：稳定训练 + 可控采样，而不是一次网络直接对抗出图。",
    )

    s = deck.content("前向与反向过程")
    add_formula_derivation(
        s,
        formulas=[
            {"label": "前向", "latex": r"q(x_t\mid x_{t-1})=\mathcal{N}(\sqrt{1-\beta_t}\,x_{t-1},\beta_t I)"},
            {"label": "闭式", "latex": r"x_t=\sqrt{\bar\alpha_t}\,x_0+\sqrt{1-\bar\alpha_t}\,\epsilon"},
            {"label": "训练", "latex": r"\mathcal{L}=\mathbb{E}\|\epsilon-\epsilon_\theta(x_t,t)\|^2"},
        ],
        bullets=[
            "β_t 为噪声日程；ᾱ_t 为累积保留系数。",
            "网络 ε_θ 预测噪声，比直接预测 x_0 更稳。",
            "采样时从 x_T∼N(0,I) 逐步去噪到 x_0。",
        ],
        note="本页用 add_formula_derivation：左公式栈、右要点。",
    )

    s = deck.content("流程：前向加噪 → 反向去噪")
    add_flowchart(
        s,
        [
            [
                {"text": "数据 x₀", "style": "primary"},
                {"text": "加噪 q", "style": "muted"},
                {"text": "x_t", "style": "soft"},
                {"text": "噪声 x_T", "style": "accent"},
            ],
            [
                {"text": "采样 x_T", "style": "accent"},
                {"text": "去噪 ε_θ", "style": "muted"},
                {"text": "x_{t-1}", "style": "soft"},
                {"text": "样本 x₀", "style": "primary"},
            ],
        ],
        row_label=["前向", "反向"],
        box_width=Inches(2.15),
        box_height=Inches(0.85),
        h_gap=Inches(0.38),
        v_gap=Inches(0.7),
        top=Inches(1.55),
        left=Inches(0.45),
        note="本页用 add_flowchart：PPT 原生圆角方块 + 箭头（非外挂图）。",
    )

    s = deck.content("与 GAN / VAE 对比")
    add_two_column_compare(
        s,
        "GAN",
        [
            "对抗目标，判别器与生成器博弈",
            "单步（或少步）生成，速度快",
            "训练敏感，易模式崩塌",
        ],
        "Diffusion",
        [
            "多步似然/去噪目标，训练更平滑",
            "采样需多步迭代，可加速",
            "覆盖模式通常更好，易控条件",
        ],
        note="本页用 add_two_column_compare。VAE 略：有显式 ELBO，但细节常弱于扩散。",
    )

    # --- figures: placeholders only (Step ②) ---
    s = deck.content("代表性工作")
    add_prior_work_grid(
        s,
        [
            {"title": "DDPM", "caption": "离散时间去噪扩散", "slot": "ddpm"},
            {"title": "DDIM", "caption": "非马尔可夫加速采样", "slot": "ddim"},
            {"title": "Score SDE", "caption": "连续时间得分匹配", "slot": "score"},
            {"title": "LDM", "caption": "隐空间扩散，降算力", "slot": "ldm"},
        ],
        note="先占位；填图走 list_image_slots → 检索 → fill_image_slots。",
    )

    s = deck.content("训练与采样一览")
    add_table_with_conclusion(
        s,
        ["环节", "典型做法", "备注"],
        [
            ["前向", "固定高斯日程", "无需网络"],
            ["训练", "预测 ε 或 v", "MSE / 加权变体"],
            ["采样", "DDPM / DDIM / 蒸馏", "步数↔质量"],
            ["条件", "拼条件 / CFG", "文生图常用"],
        ],
        conclusion="结论：扩散把难分布拆成多步小噪声；工程重点在日程、参数化与采样加速。",
    )

    s = deck.content("生成过程示意")
    add_figure_with_conclusion(
        s,
        img_path=None,
        slot_id="pipeline",
        conclusion="从纯噪声沿反向过程逐步去噪，得到数据流形上的样本。",
        caption="示意：noise → data（待填图）",
    )

    path = deck.save(OUT)
    print(f"draft saved (placeholders): {path}")
    return path


def fill_from_retrieved(paths: dict[str, str]) -> dict:
    """Steps ③–⑤: list slots, then fill with an explicit map (no directory scan)."""
    pending = call_agent_tool("list_image_slots", pptx_path=OUT)
    print("pending slots:", json.dumps(pending, ensure_ascii=False, indent=2))
    result = call_agent_tool("fill_image_slots", pptx_path=OUT, paths=paths)
    print("fill result:", json.dumps(result, ensure_ascii=False, indent=2))
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--placeholders-only",
        action="store_true",
        help="Stop after draft pptx with empty image slots (agent Step ②).",
    )
    args = ap.parse_args()

    build_draft()
    if args.placeholders_only:
        return

    # Demo stand-in for Agent retrieval (Step ④)
    figs = make_demo_figures()
    fill_from_retrieved(figs)
    print(f"final: {OUT}")


if __name__ == "__main__":
    main()
