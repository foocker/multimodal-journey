---
status: draft
updated: 2026-11-22
source_ids: ["rope"]
topic_ids: ["video-generation"]
---

# RoFormer / RoPE

正式标题：RoFormer: Enhanced Transformer with Rotary Position Embedding。固定阅读版 [`2104.09864v1`](https://arxiv.org/pdf/2104.09864v1)，12 页；本轮读 §3.2 原理，未复现模型训练。

## 要解决的问题

让 Q/K 中的绝对位置旋转在点积中表现为相对位移。二维旋转满足 `R(m)ᵀR(n)=R(n−m)`；对每对通道配不同频率，保持原 feature 维数。

同一 q/k 内容同时平移位置时点积不变，不说明上下文模型的全部分数只依赖相对位置。标准实现对 Q/K 旋转，不需要给 V 同样旋转。

本篇不是 3D MM-RoPE 的 Seedance 配方来源；具体轴分段、频率分配、镜头 offset、文本布局需各模型分别核对。它也不能提供视频长序列收敛提升的定量证据。

数学性质、布局风险与坐标测试见 [M04](../../algorithms/multimodal-position/README.md)。已做的仅是标准库二维旋转数值演示，尚未验证低精度 attention kernel 或长视频质量。
