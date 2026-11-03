# Diffusion Model 介绍 PPT 大纲

> 汇报人：tools/ppt 示例  
> 对象：版式函数演示  
> 风格：简约学术式（见 `AGENTS.md`）  
> 输出：`examples/diffusion_intro.pptx`  
> 脚本：`examples/generate_diffusion_intro_ppt.py`  
> Agent 流程：`pipelines/agent_deck.md`（占位 → 列槽 → 检索 → 填槽）

---

# Part 1 · 内容（讲什么）

## 1.1 主线

用一页讲清：扩散模型把数据逐步加噪再学习去噪，从而从噪声生成样本。

## 1.2 模块

- 背景：生成模型谱系中的位置  
- 问题：如何把复杂数据分布变成可采样的高斯  
- 公式：前向加噪与反向去噪  
- 对比：与 GAN / VAE 的差异  
- 现有工作：DDPM、DDIM、Score SDE、Latent Diffusion 四栏  
- 一表总结关键要点与结论  

---

# Part 2 · 分页设计

| Part | 主题 | 页 |
|------|------|----|
| 0 | 封面 | 1 |
| 1 | 背景 / 问题 | 2 |
| 2 | 公式 / 对比 / 现有工作 / 表+结论 / 图+结论 | 5 |

### Slide 1 · 封面
- 版式：封面
- 主标题：Diffusion Model 简介

### Slide 2 · 背景：为何需要扩散模型
- 版式：背景说明页

### Slide 3 · 问题：从数据分布到可采样噪声
- 版式：问题说明页

### Slide 4 · 前向与反向过程
- 版式：公式推导页

### Slide 5 · 与 GAN / VAE 对比
- 版式：双栏对比

### Slide 6 · 代表性工作
- 版式：现有工作四栏（先占位再填图）
- 图：slot_id = `ddpm` / `ddim` / `score` / `ldm`；图意=各方法示意；路径=待检索

### Slide 7 · 训练目标一览
- 版式：表格上 + 结论下

### Slide 8 · 生成示意
- 版式：图片上 + 结论下
- 图：slot_id = `pipeline`；图意=noise→data；路径=待检索
