---
status: draft
updated: 2026-11-22
source_ids: ["phantom"]
topic_ids: ["video-generation"]
---

# Phantom

**正式标题：** Phantom: Subject-consistent video generation via cross-modal alignment

| 项目 | 记录 |
|---|---|
| 来源 ID | `phantom` |
| 首次公开 / 阅读版本 | 2025 / `2502.11079v2` |
| 实际保存版本 | arXiv 2502.11079v2 |
| 链接 | [来源页](https://arxiv.org/abs/2502.11079v2) · [PDF URL](https://arxiv.org/pdf/2502.11079v2) · [arXiv 固定版本](https://arxiv.org/abs/2502.11079v2) |
| 页数 / 阅读位置 | 16 页；第 1、3–7 页 |
| 阅读进度 | 初步阅读；已核对部分原文，尚未完成全文精读和独立复现 |

## 要解决的问题与主要方法

Subject-consistent video generation via cross-modal alignment：参考图中的人物、服装、物品如何进入生成过程，怎样减少图像内容泄漏和多主体混淆。Seaweed 报告将其列为主体一致性下游研究。

## 放在技术演进中怎样理解

主线必读。与其他工作的关系见 [视频生成专题](../../topics/video-generation/README.md)；涉及产品或组织的说法需同时查看 [结论与证据](../../topics/video-generation/claims.json)。

## 能支持的说明与局限

支持参考图控制与主体保持的技术逻辑；不能直接写成 Seedance 2.0 的具体控制模块。

实验数据来自论文作者的设置，本仓库本轮没有重新训练或复测。对于闭源产品，没有披露的实现不能用相邻论文补齐为既定事实。

## 2026-11-22 定点阅读：可变参考仍有成本

v2 PDF pp.3–5 Figure 3–5：跨片段配对、VAE细节/CLIP语义双路径、动态窗口注入。不能把示意 token 数直接当成其他模型通用的窗口超参，也不能从支持可变参考推导无成本支持50路音视频参考。

本仓库对 Wan 的独立 reference adapter 是候选新方案，和 Phantom 原 MMDiT 动态注入分开，见 [M07](../../algorithms/reference-conditioning/README.md)。未复现原 kernel，未证明进入2.5管线。

## 下一次阅读

- 精读上面标出的章节，补充方法输入/输出、训练数据、损失函数、基线和消融条件。
- 如需实现，先确定可获得的代码、权重、数据权限与计算资源，再建立独立实验目录。
- 新证据改变当前理解时，更新本页，并在 [研究纠错记录](../../research/2026-11-19-seedance/corrections.md) 说明影响。
