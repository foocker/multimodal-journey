---
status: draft
updated: 2026-11-19
source_ids: ["seedance-1.0"]
topic_ids: ["video-generation"]
---

# Seedance 1.0

**正式标题：** Seedance 1.0: Exploring the Boundaries of Video Generation Models

| 项目 | 记录 |
|---|---|
| 来源 ID | `seedance-1.0` |
| 首次公开 / 阅读版本 | 2025 / `2506.09113v2` |
| 实际保存版本 | arXiv 2506.09113v2 |
| 链接 | [来源页](https://arxiv.org/abs/2506.09113v2) · [PDF URL](https://arxiv.org/pdf/2506.09113v2) · [arXiv 固定版本](https://arxiv.org/abs/2506.09113v2) |
| 页数 / 阅读位置 | 26 页；第 4–8、11–13 页 |
| 阅读进度 | 初步阅读；已核对部分原文，尚未完成全文精读和独立复现 |

## 要解决的问题与主要方法

把多镜头能力、数据处理、训练、RLHF、蒸馏与系统优化连起来看。第 4 页明确写位置编码设计 following Seaweed and LCT；第 12 页写量化、稀疏和 RayFlow。

## 放在技术演进中怎样理解

主线必读。与其他工作的关系见 [视频生成专题](../../topics/video-generation/README.md)；涉及产品或组织的说法需同时查看 [结论与证据](../../topics/video-generation/claims.json)。

## 能支持的说明与局限

第 1 页的速度是 NVIDIA L20 上用 41.4 秒生成一段 5 秒、1080p 视频，不能写成 5 秒完成生成。技术引用支持设计承接，不能据此断言两套模型做过权重合并。

实验数据来自论文作者的设置，本仓库本轮没有重新训练或复测。对于闭源产品，没有披露的实现不能用相邻论文补齐为既定事实。

## 下一次阅读

- 精读上面标出的章节，补充方法输入/输出、训练数据、损失函数、基线和消融条件。
- 如需实现，先确定可获得的代码、权重、数据权限与计算资源，再建立独立实验目录。
- 新证据改变当前理解时，更新本页，并在 [研究纠错记录](../../research/2026-11-19-seedance/corrections.md) 说明影响。
