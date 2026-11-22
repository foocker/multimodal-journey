---
status: draft
updated: 2026-11-22
source_ids: ["seedance-1.5-pro"]
topic_ids: ["video-generation"]
---

# Seedance 1.5 Pro

**正式标题：** Seedance 1.5 pro: A Native Audio-Visual Joint Generation Foundation Model

| 项目 | 记录 |
|---|---|
| 来源 ID | `seedance-1.5-pro` |
| 首次公开 / 阅读版本 | 2025 / `2512.13507v3` |
| 实际保存版本 | arXiv 2512.13507v3 |
| 链接 | [来源页](https://arxiv.org/abs/2512.13507v3) · [PDF URL](https://arxiv.org/pdf/2512.13507v3) · [arXiv 固定版本](https://arxiv.org/abs/2512.13507v3) |
| 页数 / 阅读位置 | 11 页；第 1–2 页；其余按评测需要查阅 |
| 阅读进度 | 初步阅读；已核对部分原文，尚未完成全文精读和独立复现 |

## 要解决的问题与主要方法

音视频联合生成的直接官方材料：双分支 DiT、跨模态交互、音画数据管线、SFT/RLHF 与超过 10 倍的推理加速概述；首页也说明火山引擎可访问。

## 放在技术演进中怎样理解

主线必读。与其他工作的关系见 [视频生成专题](../../topics/video-generation/README.md)；涉及产品或组织的说法需同时查看 [结论与证据](../../topics/video-generation/claims.json)。

## 能支持的说明与局限

双分支 DiT 在这一代已经公开。报告对部分训练细节着墨较少，不宜补写成完整的内部训练配方。

实验数据来自论文作者的设置，本仓库本轮没有重新训练或复测。对于闭源产品，没有披露的实现不能用相邻论文补齐为既定事实。

## 2026-11-22 定点核查：避免超出披露范围

v3 PDF p.1 摘要确认 dual-branch DiT 与 cross-modal joint module；p.2 Figure 2 仅画整体 pretrain/SFT/RLHF 和 PE→text encoder→joint DiT→joint refiner 流程。当前材料不足以确认指定层号、双向 cross-attention 具体公式、模态 embedding 注入位置、音频 codec/token rate 或全部 loss 权重。

本轮已渲染核查该图。此前用户摘录中的细层结构改记为可行候选，见 [M05](../../algorithms/audio-video-joint/README.md)。这不否定真实系统可能采用类似方法，只收缩公开证据支持范围。

## 下一次阅读

- 精读上面标出的章节，补充方法输入/输出、训练数据、损失函数、基线和消融条件。
- 如需实现，先确定可获得的代码、权重、数据权限与计算资源，再建立独立实验目录。
- 新证据改变当前理解时，更新本页，并在 [研究纠错记录](../../research/2026-11-19-seedance/corrections.md) 说明影响。
