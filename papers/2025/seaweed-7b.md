---
status: draft
updated: 2026-11-19
source_ids: ["seaweed-7b"]
topic_ids: ["video-generation"]
---

# Seaweed-7B

**正式标题：** Seaweed-7B: Cost-Effective Training of Video Generation Foundation Model

| 项目 | 记录 |
|---|---|
| 来源 ID | `seaweed-7b` |
| 首次公开 / 阅读版本 | 2025 / `2504.08685v2` |
| 实际保存版本 | arXiv 2504.08685v2 |
| 链接 | [来源页](https://arxiv.org/abs/2504.08685v2) · [PDF URL](https://arxiv.org/pdf/2504.08685v2) · [arXiv 固定版本](https://arxiv.org/abs/2504.08685v2) |
| 页数 / 阅读位置 | 26 页；第 1–2、5、14–19 页 |
| 阅读进度 | 初步阅读；已核对部分原文，尚未完成全文精读和独立复现 |

## 要解决的问题与主要方法

补上 Seaweed 这一条研究路线。7B、665,000 H100 GPU 小时、VAE/DiT、数据管线和下游适配均有公开说明；第 17 页还有端到端推理比较。

## 放在技术演进中怎样理解

主线必读。与其他工作的关系见 [视频生成专题](../../topics/video-generation/README.md)；涉及产品或组织的说法需同时查看 [结论与证据](../../topics/video-generation/claims.json)。

## 能支持的说明与局限

论文明确把 7B 定位为中等规模、兼顾部署成本的研究模型。它不能单独证明 2024 年内部赛马安排、后续组织合并或模型权重开源。

实验数据来自论文作者的设置，本仓库本轮没有重新训练或复测。对于闭源产品，没有披露的实现不能用相邻论文补齐为既定事实。

## 下一次阅读

- 精读上面标出的章节，补充方法输入/输出、训练数据、损失函数、基线和消融条件。
- 如需实现，先确定可获得的代码、权重、数据权限与计算资源，再建立独立实验目录。
- 新证据改变当前理解时，更新本页，并在 [研究纠错记录](../../research/2026-11-19-seedance/corrections.md) 说明影响。
