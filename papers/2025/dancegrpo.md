---
status: draft
updated: 2026-11-22
source_ids: ["dancegrpo", "seedance-1.0"]
topic_ids: ["video-generation"]
---

# DanceGRPO

**正式标题：** DanceGRPO: Unleashing GRPO on Visual Generation

| 项目 | 记录 |
|---|---|
| 来源 ID | `dancegrpo` |
| 首次公开 / 阅读版本 | 2025 / `2505.07818v4` |
| 实际保存版本 | arXiv 2505.07818v4 |
| 链接 | [来源页](https://arxiv.org/abs/2505.07818v4) · [PDF URL](https://arxiv.org/pdf/2505.07818v4) · [arXiv 固定版本](https://arxiv.org/abs/2505.07818v4) |
| 页数 / 阅读位置 | 30 页；第 1、3–6 页 |
| 阅读进度 | 初步阅读；已核对部分原文，尚未完成全文精读和独立复现 |

## 要解决的问题与主要方法

解释生成模型如何用组内相对奖励做后训练，结合运动、审美和文本对齐等多种奖励；Seedance 1.0、1.5 Pro 和 2.0 报告均列有该研究的引用。

## 放在技术演进中怎样理解

主线必读。与其他工作的关系见 [视频生成专题](../../topics/video-generation/README.md)；涉及产品或组织的说法需同时查看 [结论与证据](../../topics/video-generation/claims.json)。

## 能支持的说明与局限

有研究联系和方法依据；论文没有证明某一产品的点赞、重绘、导出事件具体如何进入训练。

实验数据来自论文作者的设置，本仓库本轮没有重新训练或复测。对于闭源产品，没有披露的实现不能用相邻论文补齐为既定事实。

## 2026-11-22 定点阅读与产品关系修正

v4 PDF pp.3–5 将采样写为 MDP，SDE 提供非退化转移密度，组内相对优势与 clipped surrogate 更新，多个奖励分别标准化优势后聚合。共享组内初始噪声是其实验设计，不是所有视觉 RL 的必要条件。固定噪声的 ODE 确定，但不同初始噪声仍能有不同结果。

Seedance 1.0 v2 p.12 §4.4.3 描述自身直接最大化多奖励的方法，并对比 DPO/PPO/GRPO；因此文献引用不能当成采用 DanceGRPO 的证据。当前摘录“固定核心引擎”的说法收缩为相关方法/候选路线。[M09](../../algorithms/post-training/README.md) 维护目标与训练边界。

## 下一次阅读

- 精读上面标出的章节，补充方法输入/输出、训练数据、损失函数、基线和消融条件。
- 如需实现，先确定可获得的代码、权重、数据权限与计算资源，再建立独立实验目录。
- 新证据改变当前理解时，更新本页，并在 [研究纠错记录](../../research/2026-11-19-seedance/corrections.md) 说明影响。
