---
status: draft
updated: 2026-11-22
source_ids: ["magvit-v2", "seedance-1.0"]
topic_ids: ["video-generation"]
---

# MAGVIT-v2：因果 tokenizer 与 Seedance VAE 的关系

正式标题：Language Model Beats Diffusion — Tokenizer is Key to Visual Generation。阅读版 [`2310.05737v3`](https://arxiv.org/pdf/2310.05737v3)，19 页；本轮定点读 PDF p.5 §3.2 / Figure 2，未复现。

原任务是学习图像/视频共用的离散 tokenizer，并把视觉 token 交给语言生成模型；LFQ 与 Seedance 1.0 的连续 latent VAE 不是同一个东西。

## 定位证据

- Figure 2 比较 C-ViViT、混合结构、causal 3D CNN；图注说明 decoder 对称，详细图在附录。
- p.5 时间左侧补 k_t−1、不补右侧；stride=s 将 `1+st` 帧映射为 `1+t`。
- p.5 上采样后丢开头 s−1 个输出；架构修改还包含 depth-to-space。不能改述为“转置卷积统一裁尾 k_t−1”。
- Seedance 1.0 v2 p.4 的引用 [31] 实际标题与本篇一致，因此虽然正文简称 MAGVIT，引用指向 MAGVIT-v2 工作。

## 支持范围与下一步

支持因果时空压缩的设计来源，不证明 48 通道 VAE 的完整网络/损失权重来自本篇。实现需检查归一化归约轴、上采样对齐、chunk 缓存和首帧行为。

当前原理与检查题维护在 [M01](../../algorithms/causal-video-vae/README.md)。待做真实模型未来扰动与整段/chunk 对照，本页保持 draft。
