---
status: draft
updated: 2026-11-19
source_ids: ["rewarddance"]
topic_ids: ["video-generation"]
---

# RewardDance

**正式标题：** RewardDance: Reward Scaling in Visual Generation

| 项目 | 记录 |
|---|---|
| 来源 ID | `rewarddance` |
| 首次公开 / 阅读版本 | 2025 / `2509.08826v1` |
| 实际保存版本 | arXiv 2509.08826v1 |
| 链接 | [来源页](https://arxiv.org/abs/2509.08826v1) · [PDF URL](https://arxiv.org/pdf/2509.08826v1) · [arXiv 固定版本](https://arxiv.org/abs/2509.08826v1) |
| 页数 / 阅读位置 | 19 页；第 1、3–9 页 |
| 阅读进度 | 初步阅读；已核对部分原文，尚未完成全文精读和独立复现 |

## 要解决的问题与主要方法

解释反馈闭环中的“谁来判好坏”：生成式奖励建模、奖励模型扩展与 reward hacking。论文直接报告 Seedance-1.0 上的实验，并讨论奖励模型扩展到 26B。

## 放在技术演进中怎样理解

主线必读。与其他工作的关系见 [视频生成专题](../../topics/video-generation/README.md)；涉及产品或组织的说法需同时查看 [结论与证据](../../topics/video-generation/claims.json)。

## 能支持的说明与局限

这里的 26B 是奖励模型规模，不是 Seedance 生成器的参数量。实验中的效果和奖励鲁棒性应保留论文条件。

实验数据来自论文作者的设置，本仓库本轮没有重新训练或复测。对于闭源产品，没有披露的实现不能用相邻论文补齐为既定事实。

## 下一次阅读

- 精读上面标出的章节，补充方法输入/输出、训练数据、损失函数、基线和消融条件。
- 如需实现，先确定可获得的代码、权重、数据权限与计算资源，再建立独立实验目录。
- 新证据改变当前理解时，更新本页，并在 [研究纠错记录](../../research/2026-11-19-seedance/corrections.md) 说明影响。
