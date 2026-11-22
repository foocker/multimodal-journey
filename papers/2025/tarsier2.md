---
status: draft
updated: 2026-11-22
source_ids: ["tarsier2", "seedance-1.0"]
topic_ids: ["video-generation"]
---

# Tarsier2：原始训练与 Seedance caption 适配分开看

正式标题：Tarsier2: Advancing Large Vision-Language Models from Detailed Video Description to Comprehensive Video Understanding。阅读版 [`2501.07888v1`](https://arxiv.org/pdf/2501.07888v1)，46 页；本轮读 pp.6–11、p.36 Table 12。

## 已核对的训练事实

| 定位 | 原文范围 |
|---|---|
| p.6 §3 | 从 Qwen2-VL 权重初始化，三阶段训练 |
| pp.7–8 | 40M 预训练，约 20M public＋20M in-house；正文写 16–128 帧，全组件可训练 |
| pp.8–9 | 150K 时间 grounding 描述；SFT-2 为 50K 多样指令与 150K 配对，不是仅 50K 配对 |
| pp.10–11 | 扰动视频生成 rejected 描述，经 AutoDQ 过滤；标准 DPO 在原始输入 x 上比较 chosen/rejected |
| p.11 | 20K 偏好对、16 帧、全参、1000 步、64 H100、global batch 64 |
| p.36 Table 12 | init 为 Qwen2-VL-7B；预训练 Frames 一栏为 [8,128]，与正文的下界有差异，原样记录 |

这些是作者的规模与硬件，本仓库没有重训或拥有该数据。不能将旧 Tarsier 的 SigLIP/逐帧 MLP 描述直接套给此版 Tarsier2。

Seedance 1.0 v2 p.7 说自己的 caption 模型基于 Tarsier2，冻结 visual encoder、全参微调 language model；这是**下游适配**，不与本篇原始全组件训练混淆。

## 方法可借鉴与边界

时间 grounding 有助于减少事件遗漏；扰动视频可制造时序错误/信息缺失，但低运动样本不一定真构成负偏好，必须过滤并人工抽检。论文中的 GPT 对照数字是作者基准结果，不代表本地 caption 效果。

当前数据方案见 [M11](../../datasets/recipes/audio-video-production/README.md)，DPO 公式与训练对象见 [M09](../../algorithms/post-training/README.md)。尚缺真实视频抽样、事实准确率与关键事件 recall 测试。
