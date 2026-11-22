---
status: draft
updated: 2026-11-22
source_ids: ["wan-2.1"]
topic_ids: ["video-generation"]
---

# Wan：候选开放研究基座

正式标题：Wan: Open and Advanced Large-Scale Video Generative Models。固定阅读版 [`2503.20314v2`](https://arxiv.org/pdf/2503.20314v2)，60 页；本轮定点读 pp.10–14，摘要中的推理资源为作者报告。

## 与 Seedance 不同的接口

- p.10 Figure 5、§4.1：VAE `(4,8,8)`、16 通道，首帧单独处理。
- p.11：RMSNorm 与 causal feature cache，编码/解码分块；也公开 VAE 分阶段训练与部分 loss 权重。
- p.14 Figure 10：DiT patch `(1,2,2)`、视觉 self-attention、独立文本 cross-attention，umT5 text encoder。
- p.14 流匹配记号 t=0 噪声、t=1 数据，速度方向与本仓库教学惯例相反；实现沿用基座 scheduler。

原文摘要给 1.3B/14B 规模与 1.3B 推理显存描述，但低推理显存不能当作全参训练资源需求。T2V checkpoint 也不能直接当作原生图片参考或区域编辑 checkpoint。

## 本仓库怎样使用它

仅作为 [M12 架构](../../topics/video-generation/seedance-2.5/architecture.md) 的候选短视频基座，保留原接口、增量研究 adapter；这不等于 Seedance 复现。尚未完成源码 commit/checkpoint hash/许可证准入与实际推理。

准入后先做原版基准、VAE 重建和小数据过拟合；参考、编辑、长上下文和联合音频分别设实验门槛。当前没有导入第三方实现或权重。
