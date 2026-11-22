---
status: draft
updated: 2026-11-22
source_ids: ["rayflow", "seedance-1.0"]
topic_ids: ["video-generation"]
---

# RayFlow

**正式标题：** RayFlow: Instance-Aware Diffusion Acceleration via Adaptive Flow Trajectories

| 项目 | 记录 |
|---|---|
| 来源 ID | `rayflow` |
| 首次公开 / 阅读版本 | 2025 / `2503.07699v2` |
| 实际保存版本 | arXiv 2503.07699v2 |
| 链接 | [来源页](https://arxiv.org/abs/2503.07699v2) · [PDF URL](https://arxiv.org/pdf/2503.07699v2) · [arXiv 固定版本](https://arxiv.org/abs/2503.07699v2) |
| 页数 / 阅读位置 | 23 页；第 1、3–7 页 |
| 阅读进度 | 初步阅读；已核对部分原文，尚未完成全文精读和独立复现 |

## 要解决的问题与主要方法

Instance-Aware Diffusion Acceleration via Adaptive Flow Trajectories：解释低步数生成时的轨迹与蒸馏。Seedance 1.0 第 12 页明确写采用 RayFlow 的 Score Distillation；1.5 Pro 也引用它。

## 放在技术演进中怎样理解

工程选读。与其他工作的关系见 [视频生成专题](../../topics/video-generation/README.md)；涉及产品或组织的说法需同时查看 [结论与证据](../../topics/video-generation/claims.json)。

## 能支持的说明与局限

原论文主要做图像实验。和 Seedance 官方报告一起读，才能区分原方法的实验与视频系统对它的使用。

实验数据来自论文作者的设置，本仓库本轮没有重新训练或复测。对于闭源产品，没有披露的实现不能用相邻论文补齐为既定事实。

## 2026-11-22 核查使用关系

Seedance 1.0 v2 PDF p.12 §5.1 直接写采用 RayFlow score distillation，是明确技术使用证据；同节还包括 TSCD 和 APT 扩展，不能把其总加速全部归给 RayFlow。2.5 是否使用该版本/后继方法未确认。

本轮未重新推导 RayFlow 全部理论，不把“轨迹绝不相交、保证稳定”写成可直接交付的工程保证。当前少步数方案与测量协议见 [M10](../../algorithms/inference-optimization/README.md)。

## 下一次阅读

- 精读上面标出的章节，补充方法输入/输出、训练数据、损失函数、基线和消融条件。
- 如需实现，先确定可获得的代码、权重、数据权限与计算资源，再建立独立实验目录。
- 新证据改变当前理解时，更新本页，并在 [研究纠错记录](../../research/2026-11-19-seedance/corrections.md) 说明影响。
