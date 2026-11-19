---
status: draft
updated: 2026-11-19
source_ids: ["x-vlm"]
topic_ids: ["video-generation"]
---

# X-VLM

**正式标题：** Multi-Grained Vision Language Pre-Training: Aligning Texts with Visual Concepts

| 项目 | 记录 |
|---|---|
| 来源 ID | `x-vlm` |
| 首次公开 / 阅读版本 | 2021 / `2111.08276v3` |
| 实际保存版本 | ICML 2022 / PMLR 162:25994–26009 |
| 链接 | [来源页](https://proceedings.mlr.press/v162/zeng22c.html) · [PDF URL](https://proceedings.mlr.press/v162/zeng22c/zeng22c.pdf) · [arXiv 固定版本](https://arxiv.org/abs/2111.08276v3) |
| 页数 / 阅读位置 | 16 页；第 1–5 页；方法与实验需继续精读 |
| 阅读进度 | 初步阅读；已核对部分原文，尚未完成全文精读和独立复现 |

## 要解决的问题与主要方法

通过不同粒度的文本与视觉概念定位和对齐，改善图文预训练。可作为视觉语言表征能力的背景，帮助理解文本条件为什么不仅是给视频加一句标题。

## 放在技术演进中怎样理解

主线材料。与其他工作的关系见 [视频生成专题](../../topics/video-generation/README.md)；涉及产品或组织的说法需同时查看 [结论与证据](../../topics/video-generation/claims.json)。

## 能支持的说明与局限

论文任务是视觉语言预训练，不能证明它直接演变为某个视频扩散模块，也不证明报道中的个人经历或管理角色。

实验数据来自论文作者的设置，本仓库本轮没有重新训练或复测。对于闭源产品，没有披露的实现不能用相邻论文补齐为既定事实。

## 下一次阅读

- 精读上面标出的章节，补充方法输入/输出、训练数据、损失函数、基线和消融条件。
- 如需实现，先确定可获得的代码、权重、数据权限与计算资源，再建立独立实验目录。
- 新证据改变当前理解时，更新本页，并在 [研究纠错记录](../../research/2026-11-19-seedance/corrections.md) 说明影响。
