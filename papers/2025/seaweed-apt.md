---
status: draft
updated: 2026-11-19
source_ids: ["seaweed-apt"]
topic_ids: ["video-generation"]
---

# Seaweed-APT

**正式标题：** Diffusion Adversarial Post-Training for One-Step Video Generation

| 项目 | 记录 |
|---|---|
| 来源 ID | `seaweed-apt` |
| 首次公开 / 阅读版本 | 2025 / `2501.08316v3` |
| 实际保存版本 | arXiv 2501.08316v3 |
| 链接 | [来源页](https://arxiv.org/abs/2501.08316v3) · [PDF URL](https://arxiv.org/pdf/2501.08316v3) · [arXiv 固定版本](https://arxiv.org/abs/2501.08316v3) |
| 页数 / 阅读位置 | 16 页；第 1–4 页及第 15 页附录 E |
| 阅读进度 | 初步阅读；已核对部分原文，尚未完成全文精读和独立复现 |

## 要解决的问题与主要方法

正式标题 Diffusion Adversarial Post-Training for One-Step Video Generation。看对抗后训练怎样让视频生成走向单步，理解降低去噪步数与保真之间的取舍。

## 放在技术演进中怎样理解

工程选读。与其他工作的关系见 [视频生成专题](../../topics/video-generation/README.md)；涉及产品或组织的说法需同时查看 [结论与证据](../../topics/video-generation/claims.json)。

## 能支持的说明与局限

“实时”必须带硬件条件：第 15 页报告 1 张 H100 的完整流程为 6.03 秒；8 张 H100 并行才实现该配置下的端到端实时。不能当作 Seedance 线上实际配方。

实验数据来自论文作者的设置，本仓库本轮没有重新训练或复测。对于闭源产品，没有披露的实现不能用相邻论文补齐为既定事实。

## 下一次阅读

- 精读上面标出的章节，补充方法输入/输出、训练数据、损失函数、基线和消融条件。
- 如需实现，先确定可获得的代码、权重、数据权限与计算资源，再建立独立实验目录。
- 新证据改变当前理解时，更新本页，并在 [研究纠错记录](../../research/2026-11-19-seedance/corrections.md) 说明影响。
