---
status: draft
updated: 2026-11-19
source_ids: ["video-dit-scaling-laws"]
topic_ids: ["video-generation"]
---

# 视频 DiT 尺度定律

**正式标题：** Towards Precise Scaling Laws for Video Diffusion Transformers

| 项目 | 记录 |
|---|---|
| 来源 ID | `video-dit-scaling-laws` |
| 首次公开 / 阅读版本 | 2024 / `2411.17470v2` |
| 实际保存版本 | arXiv 2411.17470v2 |
| 链接 | [来源页](https://arxiv.org/abs/2411.17470v2) · [PDF URL](https://arxiv.org/pdf/2411.17470v2) · [arXiv 固定版本](https://arxiv.org/abs/2411.17470v2) |
| 页数 / 阅读位置 | 16 页；第 1–8 页，尤其第 5、7 页 |
| 阅读进度 | 初步阅读；已核对部分原文，尚未完成全文精读和独立复现 |

## 要解决的问题与主要方法

Towards Precise Scaling Laws for Video Diffusion Transformers：同时考虑参数量、训练 token、计算预算、学习率和 batch size，而不是只谈“模型越大越好”。

## 放在技术演进中怎样理解

主线必读。与其他工作的关系见 [视频生成专题](../../topics/video-generation/README.md)；涉及产品或组织的说法需同时查看 [结论与证据](../../topics/video-generation/claims.json)。

## 能支持的说明与局限

来自快手等机构，是跨团队的对照研究。文中尺度实验和外推主要到约 1B 级；它不能验证 Seedance 的 200B 传闻。

实验数据来自论文作者的设置，本仓库本轮没有重新训练或复测。对于闭源产品，没有披露的实现不能用相邻论文补齐为既定事实。

## 下一次阅读

- 精读上面标出的章节，补充方法输入/输出、训练数据、损失函数、基线和消融条件。
- 如需实现，先确定可获得的代码、权重、数据权限与计算资源，再建立独立实验目录。
- 新证据改变当前理解时，更新本页，并在 [研究纠错记录](../../research/2026-11-19-seedance/corrections.md) 说明影响。
