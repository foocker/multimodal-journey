---
status: draft
updated: 2026-11-19
source_ids: ["vincie-next"]
topic_ids: ["video-generation"]
---

# VINCIE-NExT

**正式标题：** VINCIE-NExT: Unlocking Video Editing from Images via In-Context Modeling

| 项目 | 记录 |
|---|---|
| 来源 ID | `vincie-next` |
| 首次公开 / 阅读版本 | 2026 / `2610.12104v1` |
| 实际保存版本 | NeurIPS 2026 (according to the arXiv authors' comment) |
| 链接 | [来源页](https://arxiv.org/abs/2610.12104v1) · [PDF URL](https://arxiv.org/pdf/2610.12104v1) · [arXiv 固定版本](https://arxiv.org/abs/2610.12104v1) |
| 页数 / 阅读位置 | 38 页；第 1–8 页；其余含附录 |
| 阅读进度 | 初步阅读；已核对部分原文，尚未完成全文精读和独立复现 |

## 要解决的问题与主要方法

把图像编辑对作为上下文演示，通过 Video → Image → Image → Video 子任务链、共享位置表示与渐进编辑，减少对昂贵配对视频编辑数据的依赖。

## 放在技术演进中怎样理解

主线材料。与其他工作的关系见 [视频生成专题](../../topics/video-generation/README.md)；涉及产品或组织的说法需同时查看 [结论与证据](../../topics/video-generation/claims.json)。

## 能支持的说明与局限

和 Seedance 2.0 的编辑产品能力相关，但公开论文不自动证明它是该产品内部模块；需区分图像迁移到视频与前作从视频学图像编辑。

实验数据来自论文作者的设置，本仓库本轮没有重新训练或复测。对于闭源产品，没有披露的实现不能用相邻论文补齐为既定事实。

## 下一次阅读

- 精读上面标出的章节，补充方法输入/输出、训练数据、损失函数、基线和消融条件。
- 如需实现，先确定可获得的代码、权重、数据权限与计算资源，再建立独立实验目录。
- 新证据改变当前理解时，更新本页，并在 [研究纠错记录](../../research/2026-11-19-seedance/corrections.md) 说明影响。
