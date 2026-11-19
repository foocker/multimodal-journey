---
status: draft
updated: 2026-11-19
source_ids: ["long-context-tuning"]
topic_ids: ["video-generation"]
---

# Long Context Tuning

**正式标题：** Long Context Tuning for Video Generation

| 项目 | 记录 |
|---|---|
| 来源 ID | `long-context-tuning` |
| 首次公开 / 阅读版本 | 2025 / `2503.10589v1` |
| 实际保存版本 | arXiv 2503.10589v1 |
| 链接 | [来源页](https://arxiv.org/abs/2503.10589v1) · [PDF URL](https://arxiv.org/pdf/2503.10589v1) · [arXiv 固定版本](https://arxiv.org/abs/2503.10589v1) |
| 页数 / 阅读位置 | 11 页；第 1、4–8 页 |
| 阅读进度 | 初步阅读；已核对部分原文，尚未完成全文精读和独立复现 |

## 要解决的问题与主要方法

把单镜头模型扩展到场景级：场景与分镜数据、交错位置编码、异步加噪，以及 KV-cache 支持的自回归镜头续写。直接回答多镜头故事为何需要训练设计。

## 放在技术演进中怎样理解

主线必读。与其他工作的关系见 [视频生成专题](../../topics/video-generation/README.md)；涉及产品或组织的说法需同时查看 [结论与证据](../../topics/video-generation/claims.json)。

## 能支持的说明与局限

这是 Seaweed 相关研究，且被 Seedance 1.0 的模型设计部分明确引用；不等于独立证明组织合并。

实验数据来自论文作者的设置，本仓库本轮没有重新训练或复测。对于闭源产品，没有披露的实现不能用相邻论文补齐为既定事实。

## 下一次阅读

- 精读上面标出的章节，补充方法输入/输出、训练数据、损失函数、基线和消融条件。
- 如需实现，先确定可获得的代码、权重、数据权限与计算资源，再建立独立实验目录。
- 新证据改变当前理解时，更新本页，并在 [研究纠错记录](../../research/2026-11-19-seedance/corrections.md) 说明影响。
