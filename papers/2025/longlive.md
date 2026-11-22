---
status: draft
updated: 2026-11-22
source_ids: ["longlive"]
topic_ids: ["video-generation"]
---

# LongLive：流式长视频的独立工程参照

正式标题：LongLive: Real-time Interactive Long Video Generation。阅读版 [`2509.22622v2`](https://arxiv.org/pdf/2509.22622v2)，21 页；重点摘要、PDF pp.4–6 §3，未复现。

## 方法的三个边界

KV-recache 用历史视频与新 prompt 重算条件化缓存，处理换提示后的遵循与连续性；streaming long tuning 在自生成历史上滚动监督当前片段并截断历史梯度；短窗口与 frame sink 控制成本并保留早期锚点。

cache 的有效性来自明确的因果模型、固定历史与对应训练，不是给任意双向 diffusion checkpoint 加一个字典就能获得。

## 作者结果及适用范围

摘要报告 1.3B 微调 32 GPU-days、单 H100 20.7 FPS、支持 240 秒；p.6 报短窗口/sink 配置下端到端时间减少 28%、峰值显存减少 17%。这些数字保留模型、硬件和对照条件，不等于本仓库实测，也不能移植给 50 路音视频参考系统。

不是 Seedance 官方内部来源证明。它可用于设计训练/推理一致性、换 prompt 和长 rollout 的对照实验。

当前依赖与复杂度说明见 [M06](../../algorithms/long-video/README.md)。下一步需固定官方源码/checkpoint 版本、缓存等价验证与长视频分段评分，未执行。
